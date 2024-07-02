from repository.MatrizTempoViagemRepository import MatrizTempoViagemRepository
from util.ExceptionUtil import ExceptionUtil
from util.LoggerUtil import LoggerUtil

from pandas import DataFrame
from sqlalchemy.engine import Connection

log = LoggerUtil.recuperar_logger()
class MatrizTempoViagemService():

    repository = MatrizTempoViagemRepository()

    def salvar_dataframe(self, df: DataFrame, conexao_bd: Connection):
        try:
            self.repository.salvar_dataframe(df, conexao_bd)
        except Exception as e:
            log.error(msg=f"Houve um erro a persistir os dados do DataFrame na tabela {self.repository.ENTIDADE}. {ExceptionUtil.montar_exception_padrao(e)}")
            raise e