from client.OSMNXClient import OSMNXClient
from util.ExceptionUtil import ExceptionUtil
from util.LoggerUtil import LoggerUtil

from geopandas import GeoDataFrame
from networkx import MultiDiGraph
from shapely import Polygon, MultiPolygon

log = LoggerUtil.recuperar_logger()
class OSMNXClientService:

    client = OSMNXClient()

    def obter_feicoes_por_poligono(self, poligono: Polygon | MultiPolygon, tag: dict) -> GeoDataFrame:
        try:
            return self.client.obter_feicoes_por_poligono(poligono, tag)
        except Exception as e:
            log.error(msg=f"Houve um erro ao obter as feições por polígono e tag. {ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e
        
    def obter_grafo_por_poligono(self, poligono: Polygon | MultiPolygon, modalidade_transporte: str) -> MultiDiGraph:
        try:
            return self.client.obter_grafo_por_poligono(poligono, modalidade_transporte)
        except Exception as e:
            log.error(msg=f"Houve um erro ao obter o grafo por polígono e modalidade de transporte. {ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e