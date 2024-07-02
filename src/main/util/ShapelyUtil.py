from util.ExceptionUtil import ExceptionUtil
from util.LoggerUtil import LoggerUtil

from pyproj import Transformer, CRS
from shapely import Point, Polygon
from shapely.ops import transform

log = LoggerUtil.recuperar_logger()
class ShapelyUtil:

    @staticmethod
    def transformar_projecao_geometria(geometria: Point | Polygon, crs_origem: str, crs_destino: str) -> Point | Polygon:
        try:
            projetor = Transformer.from_crs(
                crs_from=CRS(crs_origem), 
                crs_to=CRS(crs_destino)
            )

            return transform(func=projetor.transform, geom=geometria)
        except Exception as e:
            log.error(msg=f"Houve um erro ao transformar a geometria para outra projeção. {ExceptionUtil.montar_exception_padrao(e)}")
            raise e