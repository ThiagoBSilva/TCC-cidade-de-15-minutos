from model.enums.EtapaProcessamentoEnum import EtapaProcessamentoEnum
from model.enums.StatusEtapaProcessamentoEnum import StatusEtapaProcessamentoEnum
from service.CalculoIndiceService import CalculoIndiceService
from service.HistoricoErroService import HistoricoErroService
from service.MunicipioService import MunicipioService
from util.DataFrameUtil import DataFrameUtil
from util.ExceptionUtil import ExceptionUtil
from util.LoggerUtil import LoggerUtil

from datetime import datetime
from pandas import DataFrame
from sqlalchemy.engine import Connection

log = LoggerUtil.recuperar_logger()
class CalculoIndiceMunicipioComponent:

    calculo_indice_service = CalculoIndiceService()
    historico_service = HistoricoErroService()
    municipio_service = MunicipioService()

    def verificar_nao_existencia_registros_pendentes(self, conexao_bd: Connection) -> bool:
        df_qtde_registros_pendentes = self.municipio_service.buscar_qtde_registros_pendentes_calculo_indice_15min(conexao_bd)
        qtde_registros_pedentes = df_qtde_registros_pendentes["quantidade"][0]

        log.info(msg=f"Há um total de {qtde_registros_pedentes} municípios a serem processados.")

        return qtde_registros_pedentes == 0



    def __calcular_indice_15min_municipio(self, municipio: list, conexao_bd: Connection) -> list[dict]:
        lista_dict_historico_erro = list()

        try:
            log.info(msg=f"Calculando índice de 15 minutos para o município {municipio[0]} - {municipio[1]}.")

            parametros = {
                "codigo_municipio": municipio[0]
            }

            self.calculo_indice_service.calcular_indice_15min_hexagono(conexao_bd, parametros)
            self.calculo_indice_service.calcular_indice_15min_municipio(conexao_bd, parametros)

            log.info(msg=f"O índice de 15 minutos foi calculado com sucesso para o município {municipio[0]} - {municipio[1]}.")
            return lista_dict_historico_erro

        except Exception as e:
            log.error(msg=f"Houve um erro ao calcular o índice de 15 minutos para o município {municipio[0]} - {municipio[1]}. "
                      f"{ExceptionUtil.montar_erro_exception_padrao(e)}")
            
            lista_dict_historico_erro.append({
                "entidade_erro": "t_municipio", 
                "chave_entidade": municipio[0], 
                "etapa_erro": EtapaProcessamentoEnum.CALCULO_INDICE_MUNICIPIO.value, 
                "mensagem_erro": ExceptionUtil.montar_erro_exception_historico_erro(), 
                "data_hora_ocorrencia":  datetime.now()
            })

            return lista_dict_historico_erro



    def processar_particao_dask(self, df_municipio: DataFrame, conexao_bd: Connection) -> DataFrame:
        lista_dict_resultado = list()

        for municipio in df_municipio.to_numpy():
            lista_dict_historico_erro = self.__calcular_indice_15min_municipio(municipio, conexao_bd)
            
            lista_dict_resultado.append({
                    "codigo_municipio": municipio[0], 
                    "lista_dict_historico_erro": lista_dict_historico_erro, 
                    "status": StatusEtapaProcessamentoEnum.CONCLUIDO.value if not lista_dict_historico_erro else StatusEtapaProcessamentoEnum.ERRO.value    
            })

        return DataFrame(data=lista_dict_resultado)
    


    def persistir_resultado(self, df_resultado: DataFrame, conexao_bd: Connection) -> None:
        try:
            log.info(msg="Persistindo os dados processados na base.")
            
            for resultado in df_resultado.to_numpy():
                if resultado[1]:
                    df_historico_erro = DataFrameUtil.dict_para_dataframe(dict_dados=resultado[1])
                    self.historico_service.salvar_dataframe(df=df_historico_erro, conexao_bd=conexao_bd)

                parametros = {
                    "flag": resultado[2],
                    "codigo_municipio": resultado[0]
                }

                self.municipio_service.atualizar_flag_calculo_indice_15min(conexao_bd, parametros)

            log.info(msg="Os dados foram persistidos com sucesso.")

        except Exception as e:
            log.error(msg=f"Houve um erro ao persistir o resultado do processamento na base. {ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e