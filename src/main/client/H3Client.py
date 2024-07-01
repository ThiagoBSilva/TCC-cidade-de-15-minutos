from model.constants.ParametrosConstantes import ParametrosConstantes

from h3 import polyfill_polygon, h3_to_geo_boundary
from retry import retry
from shapely import Polygon

class H3Client:

    @retry(tries=ParametrosConstantes.RETRY_QTDE_MAX_RETENTATIVAS, delay=ParametrosConstantes.RETRY_DELAY_ENTRE_RETENTATIVAS)
    def obter_hexagonos_h3_por_poligono(self, poligono: Polygon) -> list[str]:
        return polyfill_polygon(outer=poligono.exterior.coords, res=ParametrosConstantes.RESOLUCAO_MALHA_HEXAGONAL)
    
    @retry(tries=ParametrosConstantes.RETRY_QTDE_MAX_RETENTATIVAS, delay=ParametrosConstantes.RETRY_DELAY_ENTRE_RETENTATIVAS)
    def obter_bordas_hexagono_h3(self, hexagono_h3: str) -> tuple[tuple[float, float]]:
        return h3_to_geo_boundary(h=hexagono_h3)