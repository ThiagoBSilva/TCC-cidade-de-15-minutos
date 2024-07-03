from repository.HistoricoErroRepository import HistoricoErroRepository
from util.ExceptionUtil import ExceptionUtil
from util.LoggerUtil import LoggerUtil

from pandas import DataFrame
from sqlalchemy.engine import Connection

log = LoggerUtil.recuperar_logger()
class HistoricoErroService:

    repository = HistoricoErroRepository()

    def salvar_dataframe(self, df: DataFrame, conexao_bd: Connection) -> None:
        try:
            self.repository.salvar_dataframe(df, conexao_bd)
        except Exception as e:
            log.error(msg=f"Houve um erro ao persistir os dados do GeoDataFrame na tabela {self.repository.ENTIDADE}. {ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e