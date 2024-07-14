from model.constants.ParametrosConstantes import ParametrosConstantes
from util.ExceptionUtil import ExceptionUtil
from util.LoggerUtil import LoggerUtil
from util.YamlUtil import YAMLUtil

from geopandas import GeoDataFrame
from networkx import MultiDiGraph, set_edge_attributes
from numpy import NaN
from osmnx import settings, add_edge_travel_times, shortest_path, graph_to_gdfs
from osmnx.utils_graph import remove_isolated_nodes, route_to_gdf

log = LoggerUtil.recuperar_logger()
class OSMNXUtil:

    @staticmethod
    def configurar_osmnx() -> None:
        parametros_aplicacao = YAMLUtil.converter_yaml_para_dict(arquivo_yaml=ParametrosConstantes.CAMINHO_APPLICATION_YAML)
        
        settings.use_cache = ParametrosConstantes.OSMXN_USAR_CACHE

        if parametros_aplicacao.get("overpass-api").get("local").get("enabled"):
            settings.overpass_endpoint = parametros_aplicacao.get("overpass-api").get("local").get("url")
            settings.overpass_rate_limit = False
            settings.max_query_area_size = settings.max_query_area_size * 1000
        
    @staticmethod
    def tratar_grafo_rede_transporte(gph: MultiDiGraph, velocidade_kph: float) -> MultiDiGraph:
        try:
            gph = remove_isolated_nodes(G=gph)
            set_edge_attributes(G=gph, values=velocidade_kph, name="speed_kph")

            return add_edge_travel_times(G=gph)
        except Exception as e:
            log.error(msg=f"Houve um erro ao tratar o grafo da rede de transporte. {ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e

    @staticmethod
    def grafo_para_geodataframe(gph: MultiDiGraph, converter_nos: bool = True, converter_arestas: bool = False) -> GeoDataFrame:
        try:
            return graph_to_gdfs(G=gph, nodes=converter_nos, edges=converter_arestas)
        except Exception as e:
            log.error(msg=f"Houve um erro ao converter o grafo para um GeoDataFrame.")
            raise e
        
    @staticmethod  
    def obter_menor_caminho_entre_nos(gph: MultiDiGraph, nos_origem: list[int], nos_destino: list[int], peso: str = "travel_time", cpus: int | None = 2) -> list[list]:
        try:
            return shortest_path(G=gph, orig=nos_origem, dest=nos_destino, weight=peso, cpus=cpus)
        except Exception as e:
            log.error(msg=f"Houve um erro ao obter o menor caminho entre os nós. {ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e

    @staticmethod  
    def calcular_tempo_viagem_rota(gph: MultiDiGraph, rota: list, peso: str = "travel_time") -> float:
        try:
            if not rota:
                return NaN
            
            if len(rota) == 1:
                return 0

            gdf_rota = route_to_gdf(G=gph, route=rota, weight=peso)
            return round(gdf_rota["travel_time"].sum(), 2)
        except Exception as e:
            log.error(msg=f"Houve um erro ao calcular o tempo de viagem da rota informada. {ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e