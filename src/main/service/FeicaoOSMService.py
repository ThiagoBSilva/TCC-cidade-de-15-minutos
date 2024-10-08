from repository.FeicaoOSMRepository import FeicaoOSMRepository
from util.ExceptionUtil import ExceptionUtil
from util.LoggerUtil import LoggerUtil

from pandas import DataFrame
from sqlalchemy.engine import Connection

log = LoggerUtil.recuperar_logger()
class FeicaoOSMService:

    repository = FeicaoOSMRepository()

    def buscar_tags_osm_ativas(self, conexao_bd: Connection) -> DataFrame:
        try:
            return self.repository.buscar_tags_osm_ativas(conexao_bd=conexao_bd)
        except Exception as e:
            log.error(msg=f"Houve um erro ao buscar as tags OSM. "
                          f"{ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e