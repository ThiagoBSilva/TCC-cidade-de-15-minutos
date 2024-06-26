from model.constants.ParametrosConstantes import ParametrosConstantes
from repository.MunicipioRepository import MunicipioRepository
from util.ExceptionUtil import ExceptionUtil
from util.LoggerUtil import LoggerUtil

from geopandas import GeoDataFrame
from sqlalchemy.engine import Connection

log = LoggerUtil.recuperar_logger()
class MunicipioService:

    repository = MunicipioRepository()

    def salvar_geodataframe(self, gdf: GeoDataFrame, conexao_bd: Connection) -> None:
        try:
            self.repository.salvar_geodataframe(gdf.to_crs(crs=ParametrosConstantes.CRS_DEFAULT), conexao_bd)
            log.info(msg=f"Dados persistidos com sucesso na tabela {self.repository.ENTIDADE}.")
        except Exception as e:
            log.error(msg=f"Houve um erro ao persistir os dados do GeoDataFrame na tabela {self.repository.ENTIDADE}. {ExceptionUtil.montar_exception_padrao(e)}")
            raise e