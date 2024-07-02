from model.constants.ParametrosConstantes import ParametrosConstantes
from model.enums.EtapaProcessamentoEnum import EtapaProcessamentoEnum
from model.enums.StatusEtapaProcessamentoEnum import StatusEtapaProcessamentoEnum
from service.AmenidadeMunicipioService import AmenidadeMunicipioService
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
from numpy import NaN
from pandas import DataFrame, Series
from sqlalchemy.engine import Connection

log = LoggerUtil.recuperar_logger()
class CalculoMatrizTempoViagemComponent:
    
    amenidade_municipio_service = AmenidadeMunicipioService()
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

    def __montar_associacoes_origem_destino(self, codigo_municipio: int, gdf_malha_hexagonal_municipio: GeoDataFrame, 
                                            gdf_amenidade_municipio: GeoDataFrame, sr_modalidade_transporte: Series) -> DataFrame:
        
        descricao_modalidade_transporte = sr_modalidade_transporte["descricao"]

        df_origem_destino = DataFrame(data=[], columns=["codigo_origem", "ponto_origem", "codigo_destino", "ponto_destino"])

        try:
            log.info(msg=f"Montando as associações de origens e destinos para o município na modalidade {descricao_modalidade_transporte}.")

            raio_area_analise = self.__calcular_raio_area_analise(velocidade_kph=sr_modalidade_transporte["velocidade_media_kph"])

            for _, gsr_hexagono in gdf_malha_hexagonal_municipio.iterrows():
                ponto_origem = ShapelyUtil.transformar_projecao_geometria(
                    geometria=gsr_hexagono["geometria"],
                    crs_origem=ParametrosConstantes.GEOMETRIA_CRS_DEFAULT,
                    crs_destino=ParametrosConstantes.GEOMETRIA_CRS_METRICO_DEFAULT
                )

                geometria_area_analise = ShapelyUtil.transformar_projecao_geometria(
                    geometria=ponto_origem.centroid.buffer(raio_area_analise),
                    crs_origem=ParametrosConstantes.GEOMETRIA_CRS_METRICO_DEFAULT,
                    crs_destino=ParametrosConstantes.GEOMETRIA_CRS_DEFAULT
                )
                
                gdf_amenidades_internas = gdf_amenidade_municipio[gdf_amenidade_municipio.within(other=geometria_area_analise)]

                if gdf_amenidades_internas.empty:
                    continue

                for _, gsr_amenidade in gdf_amenidades_internas.iterrows():
                    df_origem_destino.loc[len(df_origem_destino)] = [
                        gsr_hexagono["codigo"],
                        gsr_hexagono["geometria"].centroid,
                        gsr_amenidade["codigo"],
                        gsr_amenidade["geometria"]
                    ]

            if df_origem_destino.empty:
                raise Exception("Não foi possível realizar nenhuma associação entre origens e destinos.")
            
            return df_origem_destino
        
        except Exception as e:
            log.error(msg=f"Houve um erro ao montar as associações de origem e destino. {ExceptionUtil.montar_exception_padrao(e)}")
            raise e
        
    def __obter_grafo_rede_transporte(self, sr_municipio: Series, sr_modalidade_transporte: Series) -> MultiDiGraph:
        try:
            log.info(msg=f"Obtendo o grafo da rede de transporte.")
            
            gph_rede_transporte = self.osmnx_client_service.obter_grafo_por_poligono(
                poligono=sr_municipio["geometria"], 
                modalidade_transporte=sr_modalidade_transporte["nome"]
            )
            
            return OSMNXUtil.tratar_grafo_rede_transporte(gph=gph_rede_transporte, velocidade_kph=sr_modalidade_transporte["velocidade_media_kph"])
        except Exception as e:
            log.error(msg=f"Houve um erro ao obter o grafo tratado da rede de transporte. {ExceptionUtil.montar_exception_padrao(e)}")
            raise e

    def __gerar_equivalencias_grafo(self, gph_rede_transporte: MultiDiGraph, df_origem_destino: DataFrame) -> DataFrame:
        try:
            log.info(msg=f"Gerando as equivalências dos pontos de origens e destinos para nós do grafo.")

            df_origem_destino["no_origem"] = df_origem_destino["ponto_origem"].apply(func=OSMNXUtil.encontrar_equivalencia_ponto_grafo, gph=gph_rede_transporte)
            df_origem_destino["no_destino"] = df_origem_destino["ponto_destino"].apply(func=OSMNXUtil.encontrar_equivalencia_ponto_grafo, gph=gph_rede_transporte)

            return df_origem_destino
        except Exception as e:
            log.error(msg=f"Houve um erro ao gerar as equivalências dos pontos de origem e destino para nós do grafo. {ExceptionUtil.montar_exception_padrao(e)}")
            raise e
        
    def __obter_menor_tempo_origem_destino(self, sr_origem_destino: Series, gph_rede_transporte: MultiDiGraph,) -> float:
        codigo_origem = sr_origem_destino["codigo_origem"]
        codigo_destino = sr_origem_destino["codigo_destino"]
        no_origem = sr_origem_destino["no_origem"]
        no_destino = sr_origem_destino["no_destino"]

        try:
            if no_origem == no_destino:
                return 0
            
            rota = OSMNXUtil.obter_menor_caminho_entre_nos(gph=gph_rede_transporte, no_origem=no_origem, no_destino=no_destino)
            return OSMNXUtil.calcular_tempo_viagem_rota(gph=gph_rede_transporte, rota=rota)

        except Exception as e:
            log.error(msg=f"Houve um erro ao obter o menor tempo entre a origem {codigo_origem} e destino {codigo_destino}. {ExceptionUtil.montar_exception_padrao(e)}")
            return NaN
        
    def __calcular_tempos_viagem(self, gph_rede_transporte: MultiDiGraph, df_origem_destino: DataFrame) -> DataFrame:
        try:
            log.info(msg="Calculando os tempos de viagem.")

            df_origem_destino["tempo_viagem"] = df_origem_destino.apply(
                func=self.__obter_menor_tempo_origem_destino, 
                axis=1, 
                result_type="reduce", 
                gph_rede_transporte=gph_rede_transporte
            )

            return df_origem_destino
        except Exception as e:
            log.error(msg=f"Houve um erro ao calcular os tempos de viagem. {ExceptionUtil.montar_exception_padrao(e)}")
            raise e

    def __calcular_matriz_tempo_viagem(self, sr_municipio: Series, df_modalidade_transporte: DataFrame, conexao_bd: Connection) -> tuple[DataFrame, DataFrame]:
        codigo_municipio = sr_municipio["codigo"]
        nome_municipio = sr_municipio["nome"]

        df_matriz_tempo_viagem = DataFrame(data=[], columns=["codigo_hexagono", "codigo_amenidade", "codigo_modalidade_transporte", "tempo_viagem_seg"])
        df_historico_erro = DataFrame(data=[], columns=["entidade_erro", "chave_entidade", "etapa_erro", "mensagem_erro", "data_hora_ocorrencia"])

        try:
            log.info(msg=f"Calculando a matriz de tempos de viagem para o município {codigo_municipio} - {nome_municipio}.")

            parametros = {"codigo_municipio": codigo_municipio}

            gdf_malha_hexagonal_municipio = self.malha_hexagonal_municipio_service.buscar_por_codigo_municipio(conexao_bd, parametros)
            gdf_amenidade_municipio = self.amenidade_municipio_service.buscar_por_codigo_municipio(conexao_bd, parametros)

            for _, sr_modalidade_transporte in df_modalidade_transporte.iterrows():
                df_origem_destino = self.__montar_associacoes_origem_destino(codigo_municipio, gdf_malha_hexagonal_municipio, gdf_amenidade_municipio, sr_modalidade_transporte)
                gph_rede_transporte = self.__obter_grafo_rede_transporte(sr_municipio, sr_modalidade_transporte)
                df_origem_destino = self.__gerar_equivalencias_grafo(gph_rede_transporte=gph_rede_transporte, df_origem_destino=df_origem_destino)
                df_origem_destino = self.__calcular_tempos_viagem(gph_rede_transporte=gph_rede_transporte, df_origem_destino=df_origem_destino)

                for _, sr_origem_destino in df_origem_destino.iterrows():
                    df_matriz_tempo_viagem.loc[len(df_matriz_tempo_viagem)] = [
                        sr_origem_destino["codigo_origem"],
                        sr_origem_destino["codigo_destino"],
                        sr_modalidade_transporte["codigo"],
                        sr_origem_destino["tempo_viagem"]
                    ]

            log.info(msg=f"A matriz de tempos de viagem foi calculada com sucesso para o município {codigo_municipio} - {nome_municipio}.")
            return df_matriz_tempo_viagem, df_historico_erro

        except Exception as e:
            log.error(msg=f"Houve um erro ao calcular a matriz de tempos de viagem para o município {codigo_municipio} - {nome_municipio}. "
                      f"{ExceptionUtil.montar_exception_padrao(e)}")
            
            df_historico_erro.loc[len(df_historico_erro)] = [
                "t_municipio",
                codigo_municipio,
                EtapaProcessamentoEnum.CALCULO_MATRIZ_TEMPO_VIAGEM.value,
                ExceptionUtil.montar_exception_historico_erro(e),
                datetime.now()
            ]

            return DataFrame(), df_historico_erro

    def processar_particao_dask(self, df_municipio: DataFrame, df_modalidade_transporte: DataFrame, conexao_bd: Connection) -> DataFrame:
        df_resultado = DataFrame(data=[], columns=["codigo_municipio", "dict_matriz_tempo_viagem", "dict_historico_erro", "status"])

        for _, sr_municipio in df_municipio.iterrows():
            df_matriz_tempo_viagem, df_historico_erro = self.__calcular_matriz_tempo_viagem(sr_municipio, df_modalidade_transporte, conexao_bd)

            df_resultado.loc[len(df_resultado)] = [
                sr_municipio["codigo"],
                df_matriz_tempo_viagem.to_dict(),
                df_historico_erro.to_dict(),
                StatusEtapaProcessamentoEnum.ERRO.value if df_matriz_tempo_viagem.empty else StatusEtapaProcessamentoEnum.CONCLUIDO.value
            ]

        return df_resultado.set_index(keys="codigo_municipio")
    
    def persistir_resultado(self, df_resultado: DataFrame, conexao_bd: Connection) -> None:
        try:
            for indice, sr_resultado in df_resultado.iterrows():
                if sr_resultado["dict_matriz_tempo_viagem"] != {}:
                    df_matriz_tempo_viagem = DataFrameUtil.dict_para_dataframe(dict_dados=sr_resultado["dict_matriz_tempo_viagem"])
                    self.matriz_tempo_viagem_service.salvar_dataframe(df=df_matriz_tempo_viagem, conexao_bd=conexao_bd)

                if sr_resultado["dict_historico_erro"] != {}:
                    df_historico_erro = DataFrameUtil.dict_para_dataframe(dict_dados=sr_resultado["dict_historico_erro"])
                    self.historico_erro_service.salvar_dataframe(df=df_historico_erro, conexao_bd=conexao_bd)

                parametros = {
                    "flag": sr_resultado["status"],
                    "codigo_municipio": indice
                }

                self.municipio_service.atualizar_flag_calculo_matriz_tempo_viagem(conexao_bd, parametros)
                log.info(msg="Os dados foram persistidos com sucesso.")

        except Exception as e:
            log.error(msg=f"Houve um erro ao persistir o resultado do processamento na base. {ExceptionUtil.montar_exception_padrao(e)}")
            raise e