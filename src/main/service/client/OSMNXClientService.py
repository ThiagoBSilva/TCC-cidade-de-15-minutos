from client.OSMNXClient import OSMNXClient
from util.ExceptionUtil import ExceptionUtil
from util.LoggerUtil import LoggerUtil

from geopandas import GeoDataFrame
from shapely import Polygon, MultiPolygon

log = LoggerUtil.recuperar_logger()
class OSMNXClientService:

    client = OSMNXClient()

    def obter_feicoes_por_poligono_e_tag(self, poligono: Polygon | MultiPolygon, tag: dict) -> GeoDataFrame:
        try:
            return self.client.obter_feicoes_por_poligono_e_tag(poligono, tag)
        except Exception as e:
            log.error(msg=f"Houve um erro ao obter as feições por polígono e tag. {ExceptionUtil.montar_exception_padrao(e)}")
            raise e