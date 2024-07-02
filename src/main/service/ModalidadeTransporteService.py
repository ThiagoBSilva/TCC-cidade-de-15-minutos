from repository.ModalidadeTransporteRepository import ModalidadeTransporteRepository
from util.ExceptionUtil import ExceptionUtil
from util.LoggerUtil import LoggerUtil

from pandas import DataFrame
from sqlalchemy.engine import Connection

log = LoggerUtil.recuperar_logger()
class ModalidadeTransporteService():

    repository = ModalidadeTransporteRepository()

    def buscar_todos_registros(self, conexao_bd: Connection) -> DataFrame:
        try:
            return self.repository.buscar_todos_registros(conexao_bd)
        except Exception as e:
            log.error(msg=f"Houve um erro ao buscar os registros da tabela {self.repository.ENTIDADE}. {ExceptionUtil.montar_exception_padrao(e)}")
            raise e