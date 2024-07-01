from model.constants.ParametrosConstantes import ParametrosConstantes

from osmnx import settings

class OSMNXUtil:

    @staticmethod
    def configurar_osmnx() -> None:
        settings.use_cache = ParametrosConstantes.OSMXN_USAR_CACHE