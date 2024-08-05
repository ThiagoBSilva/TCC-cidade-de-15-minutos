from repository.MalhaHexagonalMunicipioRepository import MalhaHexagonalMunicipioRepository
from util.ExceptionUtil import ExceptionUtil
from util.LoggerUtil import LoggerUtil

from geopandas import GeoDataFrame
from sqlalchemy.engine import Connection

log = LoggerUtil.recuperar_logger()
class MalhaHexagonalMunicipioService:
    
    repository = MalhaHexagonalMunicipioRepository()

    def salvar_geodataframe(self, gdf: GeoDataFrame, conexao_bd: Connection) -> None:
        try:
            self.repository.salvar_geodataframe(gdf, conexao_bd)
        except Exception as e:
            log.error(msg=f"Houve um erro ao persistir os dados do GeoDataFrame na tabela {self.repository.ENTIDADE}. "
                          f"{ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e
        
    def buscar_por_codigo_municipio(self, conexao_bd: Connection, parametros: dict) -> GeoDataFrame:
        try:
            return self.repository.buscar_por_codigo_municipio(conexao_bd, parametros)
        except Exception as e:
            log.error(msg=f"Houve um erro ao buscar a malha hexagonal pelo código do município. "
                          f"{ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e