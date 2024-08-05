from model.constants.ParametrosConstantes import ParametrosConstantes

from geopandas import GeoDataFrame
from networkx import MultiDiGraph
from osmnx import features_from_polygon, graph_from_polygon
from osmnx._errors import InsufficientResponseError
from retry import retry
from shapely import Polygon, MultiPolygon

class OSMNXClient:

    @retry(tries=ParametrosConstantes.RETRY_QTDE_MAX_RETENTATIVAS, delay=ParametrosConstantes.RETRY_DELAY_ENTRE_RETENTATIVAS)
    def obter_feicoes_por_poligono(self, poligono: Polygon | MultiPolygon, tag: dict) -> GeoDataFrame:
        try:
            return features_from_polygon(polygon=poligono, tags=tag)
        except InsufficientResponseError:
            return GeoDataFrame()
    
    @retry(tries=ParametrosConstantes.RETRY_QTDE_MAX_RETENTATIVAS, delay=ParametrosConstantes.RETRY_DELAY_ENTRE_RETENTATIVAS)
    def obter_grafo_por_poligono(self, poligono: Polygon | MultiPolygon, modalidade_transporte: str) -> MultiDiGraph:
        return graph_from_polygon(polygon=poligono, network_type=modalidade_transporte, simplify=True)