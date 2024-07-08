from model.enums.EtapaProcessamentoEnum import EtapaProcessamentoEnum
from model.enums.StatusEtapaProcessamentoEnum import StatusEtapaProcessamentoEnum
from service.CalculoIndiceService import CalculoIndiceService
from service.HistoricoErroService import HistoricoErroService
from service.UnidadeFederativaService import UnidadeFederativaService
from util.DataFrameUtil import DataFrameUtil
from util.ExceptionUtil import ExceptionUtil
from util.LoggerUtil import LoggerUtil

from datetime import datetime
from pandas import DataFrame
from sqlalchemy.engine import Connection

log = LoggerUtil.recuperar_logger()
class CalculoIndiceUnidadeFederativaComponent:

    calculo_indice_service = CalculoIndiceService()
    historico_service = HistoricoErroService()
    unidade_federativa_service = UnidadeFederativaService()

    def verificar_nao_existencia_registros_pendentes(self, conexao_bd: Connection) -> bool:
        df_qtde_registros_pendentes = self.unidade_federativa_service.buscar_qtde_registros_pendentes_calculo_indice_15min(conexao_bd)
        qtde_registros_pedentes = df_qtde_registros_pendentes["quantidade"][0]

        log.info(msg=f"Há um total de {qtde_registros_pedentes} unidades federativas a serem processadas.")

        return qtde_registros_pedentes == 0
    


    def __calcular_indice_15min_unidade_federativa(self, unidade_federativa: list, conexao_bd: Connection) -> list[dict]:
        lista_dict_historico_erro = list()

        try:
            log.info(msg=f"Calculando índice de 15 minutos para a unidade federativa {unidade_federativa[0]} - {unidade_federativa[1]}.")

            parametros = {
                "codigo_unidade_federativa": unidade_federativa[0]
            }

            self.calculo_indice_service.calcular_indice_15min_unidade_federativa(conexao_bd, parametros)

            log.info(msg=f"O índice de 15 minutos foi calculado com sucesso para a unidade federativa {unidade_federativa[0]} - {unidade_federativa[1]}.")
            return lista_dict_historico_erro

        except Exception as e:
            log.error(msg=f"Houve um erro ao calcular o índice de 15 minutos para a unidade federativa {unidade_federativa[0]} - {unidade_federativa[1]}. "
                      f"{ExceptionUtil.montar_erro_exception_padrao(e)}")
            
            lista_dict_historico_erro.append({
                "entidade_erro": "t_unidade_federativa", 
                "chave_entidade": unidade_federativa[0], 
                "etapa_erro": EtapaProcessamentoEnum.CALCULO_INDICE_UNIDADE_FEDERATIVA.value, 
                "mensagem_erro": ExceptionUtil.montar_erro_exception_historico_erro(), 
                "data_hora_ocorrencia":  datetime.now()
            })

            return lista_dict_historico_erro



    def processar_particao_dask(self, df_unidade_federativa: DataFrame, conexao_bd: Connection) -> DataFrame:
        lista_dict_resultado = list()

        for unidade_federativa in df_unidade_federativa.to_numpy():
            lista_dict_historico_erro = self.__calcular_indice_15min_unidade_federativa(unidade_federativa, conexao_bd)
            
            lista_dict_resultado.append({
                    "codigo_unidade_federativa": unidade_federativa[0], 
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
                    "codigo_unidade_federativa": resultado[0]
                }

                self.unidade_federativa_service.atualizar_flag_calculo_indice_15min(conexao_bd, parametros)

            log.info(msg="Os dados foram persistidos com sucesso.")

        except Exception as e:
            log.error(msg=f"Houve um erro ao persistir o resultado do processamento na base. {ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e