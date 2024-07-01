from model.constants.ParametrosConstantes import ParametrosConstantes

from geopandas import GeoDataFrame
from osmnx import features_from_polygon
from osmnx._errors import InsufficientResponseError
from retry import retry
from shapely import Polygon, MultiPolygon

class OSMNXClient:

    @retry(tries=ParametrosConstantes.RETRY_QTDE_MAX_RETENTATIVAS, delay=ParametrosConstantes.RETRY_DELAY_ENTRE_RETENTATIVAS)
    def obter_feicoes_por_poligono_e_tag(self, poligono: Polygon | MultiPolygon, tag: dict) -> GeoDataFrame:
        try:
            return features_from_polygon(polygon=poligono, tags=tag)
        except InsufficientResponseError:
            return GeoDataFrame()