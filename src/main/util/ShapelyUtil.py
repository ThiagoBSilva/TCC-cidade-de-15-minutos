from util.ExceptionUtil import ExceptionUtil
from util.LoggerUtil import LoggerUtil

from pyproj import Transformer, CRS
from shapely import from_wkt
from shapely.ops import transform

log = LoggerUtil.recuperar_logger()
class ShapelyUtil:

    @staticmethod
    def wkt_para_geometria(geometria_wkt: str) -> any:
        try:
            return from_wkt(geometry=geometria_wkt)
        except Exception as e:
            log.error(msg=f"Houve um erro ao transformar o valor WKT {geometria_wkt} para uma geometria Shapely. {ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e