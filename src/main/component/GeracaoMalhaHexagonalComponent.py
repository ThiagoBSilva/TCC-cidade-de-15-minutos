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
from geopandas import GeoDataFrame
from pandas import DataFrame, Series
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
    
    def __gerar_malha_hexagonal_municipio(self, sr_municipio: Series) -> tuple[DataFrame, DataFrame]:
        codigo_municipio = sr_municipio["codigo"]
        nome_municipio = sr_municipio["nome"]

        df_malha_hexagonal = DataFrame(data=[], columns=["hexagono_h3", "geometria", "codigo_municipio"])
        df_historico_erro = DataFrame(data=[], columns=["entidade_erro", "chave_entidade", "etapa_erro", "mensagem_erro", "data_hora_ocorrencia"])

        try:
            log.info(msg=f"Gerando a malha do município {codigo_municipio} - {nome_municipio}.")
            
            hexagonos_h3 = list()

            for poligono in list(sr_municipio["geometria"].geoms):
                hexagonos_h3 = hexagonos_h3 + list(self.h3_client_service.obter_hexagonos_h3_por_poligono(poligono))

            if not hexagonos_h3:
                raise Exception("Não foi possível obter a malha hexagonal do município, nenhum hexágono encontrado para o polígono e resolução informados")

            for hex_h3 in hexagonos_h3:
                geometria = self.h3_client_service.obter_poligono_hexagono_h3(hexagono_h3=hex_h3)

                df_malha_hexagonal.loc[len(df_malha_hexagonal)] = [
                    hex_h3,
                    geometria,
                    codigo_municipio
                ]
                
            log.info(msg=f"A malha hexagonal para o município {codigo_municipio} - {nome_municipio} foi gerada com sucesso.")
            return df_malha_hexagonal, df_historico_erro

        except Exception as e:
            log.error(msg=f"Houve um erro ao gerar a malha hexagonal para o município {codigo_municipio} - {nome_municipio}. {ExceptionUtil.montar_exception_padrao(e)}")

            df_historico_erro.loc[len(df_historico_erro)] = [
                "t_municipio",
                codigo_municipio,
                EtapaProcessamentoEnum.GERACAO_MALHA_HEXAGONAL.value,
                ExceptionUtil.montar_exception_historico_erro(e),
                datetime.now()
            ]

            return DataFrame(), df_historico_erro
    
    def processar_particao_dask(self, df_municipio: DataFrame) -> DataFrame:
        df_resultado = DataFrame(data=[], columns=["codigo_municipio", "dict_malha_hexagonal", "dict_historico_erro", "status"])

        for _, sr_municipio in df_municipio.iterrows():
            df_malha_hexagonal, df_historico_erro = self.__gerar_malha_hexagonal_municipio(sr_municipio)

            df_resultado.loc[len(df_resultado)] = [
                sr_municipio["codigo"],
                df_malha_hexagonal.to_dict(),
                df_historico_erro.to_dict(),
                StatusEtapaProcessamentoEnum.ERRO.value if df_malha_hexagonal.empty else StatusEtapaProcessamentoEnum.CONCLUIDO.value
            ]

        return df_resultado.set_index(keys="codigo_municipio")
    
    def persistir_resultado(self, df_resultado: DataFrame, conexao_bd: Connection) -> None:
        try:
            for indice, sr_resultado in df_resultado.iterrows():
                if sr_resultado["dict_malha_hexagonal"] != {}:
                    gdf_malha_hexagonal_municipio = DataFrameUtil.dict_para_geodataframe(dict_dados=sr_resultado["dict_malha_hexagonal"])
                    self.malha_hexagonal_service.salvar_geodataframe(gdf=gdf_malha_hexagonal_municipio, conexao_bd=conexao_bd)

                if sr_resultado["dict_historico_erro"] != {}:
                    df_historico_erro = DataFrameUtil.dict_para_dataframe(dict_dados=sr_resultado["dict_historico_erro"])
                    self.historico_erro_service.salvar_dataframe(df=df_historico_erro, conexao_bd=conexao_bd)

                parametros = {
                    "flag": sr_resultado["status"],
                    "codigo_municipio": indice
                }

                self.municipio_service.atualizar_flag_geracao_malha_hexagonal(conexao_bd, parametros)
                log.info(msg="Os dados foram persistidos com sucesso.")
                
        except Exception as e:
            log.error(msg=f"Houve um erro ao persistir o resultado do processamento na base. {ExceptionUtil.montar_exception_padrao(e)}")
            raise e