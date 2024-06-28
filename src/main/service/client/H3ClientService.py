from client.H3Client import H3Client
from util.ExceptionUtil import ExceptionUtil
from util.LoggerUtil import LoggerUtil

from shapely import Polygon

log = LoggerUtil.recuperar_logger()
class H3ClientService:

    client = H3Client()

    def obter_hexagonos_h3_por_poligono(self, poligono: Polygon) -> list[str]:
        try:
            return self.client.obter_hexagonos_h3_por_poligono(poligono)
        except Exception as e:
            log.error(msg=f"Houve um erro ao obter os hexágonos H3 a partir do polígono. {ExceptionUtil.montar_exception_padrao(e)}")
            raise e
    
    def obter_poligono_hexagono_h3(self, hexagono_h3: str) -> Polygon:
        try:
            return Polygon(shell=self.client.obter_bordas_hexagono_h3(hexagono_h3))
        except Exception as e:
            log.error(msg=f"Houve um erro ao obter o polígono do hexágono H3 {hexagono_h3}. {ExceptionUtil.montar_exception_padrao(e)}")
            raise e