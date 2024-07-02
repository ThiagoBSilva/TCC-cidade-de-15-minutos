from model.constants.ParametrosConstantes import ParametrosConstantes
from util.ExceptionUtil import ExceptionUtil
from util.LoggerUtil import LoggerUtil
from util.YamlUtil import YAMLUtil

from networkx import MultiDiGraph, set_edge_attributes
from osmnx import settings, add_edge_travel_times, nearest_nodes, shortest_path
from osmnx.utils_graph import remove_isolated_nodes, route_to_gdf
from shapely import Point

log = LoggerUtil.recuperar_logger()
class OSMNXUtil:

    @staticmethod
    def configurar_osmnx() -> None:
        parametros_aplicacao = YAMLUtil.converter_yaml_para_dict(arquivo_yaml=ParametrosConstantes.CAMINHO_APPLICATION_YAML)
        
        settings.use_cache = ParametrosConstantes.OSMXN_USAR_CACHE

        if parametros_aplicacao.get("nominatim-api").get("local").get("enabled"):
            settings.nominatim_endpoint = ParametrosConstantes.OSMNX_URL_NOMINATIM_LOCAL
            settings.nominatim_key = 123456

        if parametros_aplicacao.get("overpass-api").get("local").get("enabled"):
            settings.overpass_endpoint = ParametrosConstantes.OSMNX_URL_OVERPASS_LOCAL
            settings.overpass_rate_limit = False
        
    @staticmethod
    def tratar_grafo_rede_transporte(gph: MultiDiGraph, velocidade_kph: float) -> MultiDiGraph:
        try:
            gph = remove_isolated_nodes(G=gph)
            set_edge_attributes(G=gph, values=velocidade_kph, name="speed_kph")
            return add_edge_travel_times(G=gph)
        except Exception as e:
            log.error(msg=f"Houve um erro ao tratar o grafo da rede de transporte. {ExceptionUtil.montar_exception_padrao(e)}")
            raise e

    @staticmethod  
    def encontrar_equivalencia_ponto_grafo(ponto: Point, gph: MultiDiGraph) -> None:
        try:
            return nearest_nodes(G=gph, X=ponto.x, Y=ponto.y)
        except Exception as e:
            log.error(msg=f"Houve um erro ao encontrar uma equivalência no grafo para o ponto informado. {ExceptionUtil.montar_exception_padrao(e)}")
            raise e
        
    @staticmethod  
    def obter_menor_caminho_entre_nos(gph: MultiDiGraph, no_origem: int, no_destino: int, peso: str = "travel_time", cpus: int | None = None) -> None:
        try:
            return shortest_path(G=gph, orig=no_origem, dest=no_destino, weight=peso, cpus=cpus)
        except Exception as e:
            log.error(msg=f"Houve um erro ao obter o menor caminho entre os nós. {ExceptionUtil.montar_exception_padrao(e)}")
            raise e

    @staticmethod  
    def calcular_tempo_viagem_rota(gph: MultiDiGraph, rota: list, peso: str = "travel_time"):
        try:
            gdf_rota = route_to_gdf(G=gph, route=rota, weight=peso)
            return round(gdf_rota["travel_time"].sum(), 2)
        except Exception as e:
            log.error(msg=f"Houve um erro ao calcular o tempo de viagem da rota informada. {ExceptionUtil.montar_exception_padrao(e)}")
            raise e