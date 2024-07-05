from model.constants.ParametrosConstantes import ParametrosConstantes
from model.constants.MapeamentosConstantes import MapeamentosConstantes
from model.enums.EtapaProcessamentoEnum import EtapaProcessamentoEnum
from model.enums.StatusEtapaProcessamentoEnum import StatusEtapaProcessamentoEnum
from service.AmenidadeMunicipioService import AmenidadeMunicipioService
from service.CalculoMatrizService import CalculoMatrizService
from service.HistoricoErroService import HistoricoErroService
from service.MalhaHexagonalMunicipioService import MalhaHexagonalMunicipioService
from service.MatrizTempoViagemService import MatrizTempoViagemService
from service.MunicipioService import MunicipioService
from service.client.OSMNXClientService import OSMNXClientService
from util.DataFrameUtil import DataFrameUtil
from util.ExceptionUtil import ExceptionUtil
from util.LoggerUtil import LoggerUtil
from util.OSMNXUtil import OSMNXUtil
from util.ShapelyUtil import ShapelyUtil

from datetime import datetime
from geopandas import GeoDataFrame
from networkx import MultiDiGraph
from numpy import NaN, array
from pandas import DataFrame
from sqlalchemy.engine import Connection

log = LoggerUtil.recuperar_logger()
class CalculoMatrizTempoViagemComponent:
    
    amenidade_municipio_service = AmenidadeMunicipioService()
    calculo_matriz_service = CalculoMatrizService()
    historico_erro_service = HistoricoErroService()
    malha_hexagonal_municipio_service = MalhaHexagonalMunicipioService()
    matriz_tempo_viagem_service = MatrizTempoViagemService()
    municipio_service = MunicipioService()
    osmnx_client_service = OSMNXClientService()

    def verificar_nao_existencia_registros_pendentes(self, conexao_bd: Connection) -> bool:
        df_qtde_registros_pendentes = self.municipio_service.buscar_qtde_registros_pendentes_calculo_matriz_tempo_viagem(conexao_bd)
        qtde_registros_pedentes = df_qtde_registros_pendentes["quantidade"][0]

        log.info(msg=f"Há um total de {qtde_registros_pedentes} municípios a serem processados.")

        return qtde_registros_pedentes == 0
    


    def __calcular_raio_area_analise(self, velocidade_kph: float) -> float:
        return velocidade_kph * 15/60 * 1000 * ParametrosConstantes.MULTIPLICADOR_AREA_ANALISE_HEXAGONO

    def __obter_geodataframe_grafo(self, gph: MultiDiGraph) -> GeoDataFrame:
        gdf_no_grafo = OSMNXUtil.grafo_para_geodataframe(gph)
        gdf_no_grafo["osmid"] = gdf_no_grafo.index
        gdf_no_grafo = DataFrameUtil.renomear_colunas_dataframe(df=gdf_no_grafo, mapeamento=MapeamentosConstantes.COLUNAS_NO_GRAFO)

        return gdf_no_grafo.loc[:, ["codigo", "geometria"]]

    def __montar_associacoes_origem_destino(self, codigo_municipio: int, modalidade_transporte: list, 
                                            gph_rede_transporte: MultiDiGraph, conexao_bd: Connection) -> DataFrame:
        try:
            log.info(msg=f"Montando as associações de origens e destinos para o município na modalidade {modalidade_transporte[2]}.")

            parametros = {
                "codigo_municipio": codigo_municipio,
                "raio_buffer": self.__calcular_raio_area_analise(velocidade_kph=modalidade_transporte[3]),
            }

            self.calculo_matriz_service.dropar_tabela_temporaria_grafo(conexao_bd, parametros)
            gdf_grafo = self.__obter_geodataframe_grafo(gph=gph_rede_transporte)
            self.calculo_matriz_service.salvar_grafo_municipio(gdf=gdf_grafo, conexao_bd=conexao_bd, parametros=parametros)

            df_origem_destino = self.calculo_matriz_service.buscar_associacoes_origem_destino_por_codigo_municipio(conexao_bd, parametros)

            if df_origem_destino.empty:
                raise Exception("Não foi possível realizar nenhuma associação entre origens e destinos.")
            
            return df_origem_destino
        
        except Exception as e:
            log.error(msg=f"Houve um erro ao montar as associações de origem e destino. {ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e



    def __obter_grafo_rede_transporte(self, municipio: list, modalidade_transporte: list) -> MultiDiGraph:
        try:
            log.info(msg=f"Obtendo o grafo da rede de transporte.")
            
            gph_rede_transporte = self.osmnx_client_service.obter_grafo_por_poligono(
                poligono=municipio[2], 
                modalidade_transporte=modalidade_transporte[1]
            )
            
            return OSMNXUtil.tratar_grafo_rede_transporte(gph=gph_rede_transporte, velocidade_kph=modalidade_transporte[3])
        except Exception as e:
            log.error(msg=f"Houve um erro ao obter o grafo tratado da rede de transporte. {ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e



    def __obter_menor_tempo_origem_destino(self, gph_rede_transporte: MultiDiGraph, origem_destino: list) -> float:
        try:
            if origem_destino[1] == origem_destino[3]:
                return 0
            
            rota = OSMNXUtil.obter_menor_caminho_entre_nos(gph=gph_rede_transporte, no_origem=origem_destino[1], no_destino=origem_destino[3])
            return OSMNXUtil.calcular_tempo_viagem_rota(gph=gph_rede_transporte, rota=rota)

        except Exception as e:
            log.error(msg=f"Houve um erro ao obter o menor tempo entre a origem {origem_destino[0]} e destino {origem_destino[2]}. {ExceptionUtil.montar_erro_exception_padrao(e)}")
            return NaN



    def __calcular_tempos_viagem(self, gph_rede_transporte: MultiDiGraph, df_origem_destino: DataFrame) -> DataFrame:
        try:
            log.info(msg="Calculando os tempos de viagem.")

            df_origem_destino["tempo_viagem"] = array(self.__obter_menor_tempo_origem_destino(gph_rede_transporte, origem_destino) for origem_destino in df_origem_destino.to_numpy())
            
            return df_origem_destino
        except Exception as e:
            log.error(msg=f"Houve um erro ao calcular os tempos de viagem. {ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e



    def __calcular_matriz_tempo_viagem(self, municipio: list, df_modalidade_transporte: DataFrame, conexao_bd: Connection) -> tuple[list[dict], list[dict]]:
        lista_dict_matriz_tempo_viagem = list()
        lista_dict_historico_erro = list()

        try:
            log.info(msg=f"Calculando a matriz de tempos de viagem para o município {municipio[0]} - {municipio[1]}.")

            for modalidade_transporte in df_modalidade_transporte.to_numpy():
                gph_rede_transporte = self.__obter_grafo_rede_transporte(municipio, modalidade_transporte)
                df_origem_destino = self.__montar_associacoes_origem_destino(municipio[0], modalidade_transporte, gph_rede_transporte, conexao_bd)
                df_origem_destino = self.__calcular_tempos_viagem(gph_rede_transporte, df_origem_destino)

                for origem_destino in df_origem_destino.to_numpy():
                    lista_dict_matriz_tempo_viagem.append({
                        "codigo_hexagono": origem_destino[0], 
                        "codigo_amenidade": origem_destino[2], 
                        "codigo_modalidade_transporte": modalidade_transporte[0], 
                        "tempo_viagem_seg": origem_destino[4]
                    })

            log.info(msg=f"A matriz de tempos de viagem foi calculada com sucesso para o município {municipio[0]} - {municipio[1]}.")
            return lista_dict_matriz_tempo_viagem, lista_dict_historico_erro

        except Exception as e:
            log.error(msg=f"Houve um erro ao calcular a matriz de tempos de viagem para o município {municipio[0]} - {municipio[1]}. "
                      f"{ExceptionUtil.montar_erro_exception_padrao(e)}")
            
            lista_dict_historico_erro.append({
                "entidade_erro": "t_municipio", 
                "chave_entidade": municipio[0], 
                "etapa_erro": EtapaProcessamentoEnum.CALCULO_MATRIZ_TEMPO_VIAGEM.value, 
                "mensagem_erro": ExceptionUtil.montar_erro_exception_historico_erro(), 
                "data_hora_ocorrencia":  datetime.now()
            })

            return list(), lista_dict_historico_erro



    def processar_particao_dask(self, df_municipio: DataFrame, df_modalidade_transporte: DataFrame, conexao_bd: Connection) -> DataFrame:
        lista_dict_resultado = list()

        for municipio in df_municipio.to_numpy():
            lista_dict_matriz_tempo_viagem, lista_dict_historico_erro = self.__calcular_matriz_tempo_viagem(municipio, df_modalidade_transporte, conexao_bd)
            
            lista_dict_resultado.append({
                    "codigo_municipio": municipio[0], 
                    "lista_dict_matriz_tempo_viagem": lista_dict_matriz_tempo_viagem, 
                    "lista_dict_historico_erro": lista_dict_historico_erro, 
                    "status": StatusEtapaProcessamentoEnum.CONCLUIDO.value if lista_dict_matriz_tempo_viagem else StatusEtapaProcessamentoEnum.ERRO.value    
            })

        return DataFrame(data=lista_dict_resultado)
    


    def persistir_resultado(self, df_resultado: DataFrame, conexao_bd: Connection) -> None:
        try:
            log.info(msg="Persistindo os dados processados na base.")
            
            for resultado in df_resultado.to_numpy():
                if resultado[1]:
                    df_matriz_tempo_viagem = DataFrameUtil.dict_para_dataframe(dict_dados=resultado[1])
                    self.matriz_tempo_viagem_service.salvar_dataframe(df=df_matriz_tempo_viagem, conexao_bd=conexao_bd)

                if resultado[2]:
                    df_historico_erro = DataFrameUtil.dict_para_dataframe(dict_dados=resultado[2])
                    self.historico_erro_service.salvar_dataframe(df=df_historico_erro, conexao_bd=conexao_bd)

                parametros = {
                    "flag": resultado[3],
                    "codigo_municipio": resultado[0]
                }

                self.municipio_service.atualizar_flag_calculo_matriz_tempo_viagem(conexao_bd, parametros)

            log.info(msg="Os dados foram persistidos com sucesso.")

        except Exception as e:
            log.error(msg=f"Houve um erro ao persistir o resultado do processamento na base. {ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e