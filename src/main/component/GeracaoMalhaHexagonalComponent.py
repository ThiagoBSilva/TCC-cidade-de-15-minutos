from model.constants.ParametrosConstantes import ParametrosConstantes
from model.enums.EtapaProcessamentoEnum import EtapaProcessamentoEnum
from model.enums.StatusEtapaProcessamentoEnum import StatusEtapaProcessamentoEnum
from service.HistoricoErroService import HistoricoErroService
from service.MalhaHexagonalMunicipioService import MalhaHexagonalMunicipioService
from service.MunicipioService import MunicipioService
from service.client.H3ClientService import H3ClientService
from util.DataFrameUtil import DataFrameUtil
from util.ExceptionUtil import ExceptionUtil
from util.LoggerUtil import LoggerUtil

from datetime import datetime
from pandas import DataFrame
from sqlalchemy.engine import Connection

log = LoggerUtil.recuperar_logger()
class GeracaoMalhaHexagonalComponent:

    h3_client_service = H3ClientService()
    historico_erro_service = HistoricoErroService()
    malha_hexagonal_service = MalhaHexagonalMunicipioService()
    municipio_service = MunicipioService()

    def verificar_nao_existencia_registros_pendentes(self, conexao_bd: Connection) -> bool:
        df_qtde_registros_pendentes = self.municipio_service.buscar_qtde_registros_pendentes_geracao_malha_hexagonal(conexao_bd)
        qtde_registros_pendentes = df_qtde_registros_pendentes["quantidade"][0]

        log.info(msg=f"Há um total de {qtde_registros_pendentes} municípios a serem processados.")

        return qtde_registros_pendentes == 0
    


    def __gerar_malha_hexagonal_municipio(self, municipio: list) -> tuple[list[dict], list[dict]]:
        lista_dict_malha_hexagonal = list()
        lista_dict_historico_erro = list()

        try:
            log.info(msg=f"Gerando a malha do município {municipio[0]} - {municipio[1]}.")
            
            hexagonos_h3 = list()

            for poligono in list(municipio[2].geoms):
                hexagonos_h3 = hexagonos_h3 + list(self.h3_client_service.obter_hexagonos_h3_por_poligono(poligono))

            if not hexagonos_h3:
                raise Exception("Não foi possível obter a malha hexagonal do município, nenhum hexágono encontrado para o polígono e resolução informados")

            for hex_h3 in hexagonos_h3:
                geometria = self.h3_client_service.obter_poligono_hexagono_h3(hexagono_h3=hex_h3)

                lista_dict_malha_hexagonal.append({
                    "hexagono_h3": hex_h3,
                    "geometria": geometria,
                    "codigo_municipio": municipio[0]
                })
                
            log.info(msg=f"A malha hexagonal para o município {municipio[0]} - {municipio[1]} foi gerada com sucesso.")
            return lista_dict_malha_hexagonal, lista_dict_historico_erro

        except Exception as e:
            log.error(msg=f"Houve um erro ao gerar a malha hexagonal para o município {municipio[0]} - {municipio[1]}. {ExceptionUtil.montar_erro_exception_padrao(e)}")

            lista_dict_historico_erro.append({
                "entidade_erro": "t_municipio",
                "chave_entidade": municipio[0],
                "etapa_erro": EtapaProcessamentoEnum.GERACAO_MALHA_HEXAGONAL.value,
                "mensagem_erro": ExceptionUtil.montar_erro_exception_historico_erro(e),
                "data_hora_ocorrencia": datetime.now()
            })

            return list(), lista_dict_historico_erro
    


    def processar_particao_dask(self, df_municipio: DataFrame) -> DataFrame:
        lista_dict_resultado = list()

        for municipio in df_municipio.to_numpy():
            lista_dict_malha_hexagonal, lista_dict_historico_erro = self.__gerar_malha_hexagonal_municipio(municipio)

            lista_dict_resultado.append({
                "codigo_municipio": municipio[0], 
                "lista_dict_malha_hexagonal": lista_dict_malha_hexagonal, 
                "lista_dict_historico_erro": lista_dict_historico_erro, 
                "status": StatusEtapaProcessamentoEnum.CONCLUIDO.value if lista_dict_malha_hexagonal else StatusEtapaProcessamentoEnum.ERRO.value
            })

        return DataFrame(data=lista_dict_resultado)
    

    
    def persistir_resultado(self, df_resultado: DataFrame, conexao_bd: Connection) -> None:
        try:
            log.info(msg="Persistindo os dados processados na base.")

            for resultado in df_resultado.to_numpy():
                if resultado[1]:
                    gdf_malha_hexagonal_municipio = DataFrameUtil.dict_para_geodataframe(dict_dados=resultado[1])
                    self.malha_hexagonal_service.salvar_geodataframe(gdf=gdf_malha_hexagonal_municipio, conexao_bd=conexao_bd)

                if resultado[2]:
                    df_historico_erro = DataFrameUtil.dict_para_dataframe(dict_dados=resultado[2])
                    self.historico_erro_service.salvar_dataframe(df=df_historico_erro, conexao_bd=conexao_bd)

                parametros = {
                    "flag": resultado[3],
                    "codigo_municipio": resultado[0]
                }

                self.municipio_service.atualizar_flag_geracao_malha_hexagonal(conexao_bd, parametros)

            log.info(msg="Os dados foram persistidos com sucesso.")
                
        except Exception as e:
            log.error(msg=f"Houve um erro ao persistir o resultado do processamento na base. {ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e