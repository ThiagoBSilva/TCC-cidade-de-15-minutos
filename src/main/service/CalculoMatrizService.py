from repository.CalculoMatrizRepository import CalculoMatrizRepository
from util.ExceptionUtil import ExceptionUtil
from util.LoggerUtil import LoggerUtil

from geopandas import GeoDataFrame
from pandas import DataFrame
from sqlalchemy.engine import Connection

log = LoggerUtil.recuperar_logger()
class CalculoMatrizService:

    repository = CalculoMatrizRepository()

    def dropar_tabela_temporaria_grafo(self, conexao_bd: Connection, parametros: dict) -> None:
        try:
            self.repository.dropar_tabela_temporaria_grafo(conexao_bd, parametros)
        except Exception as e:
            log.error(msg=f"Houve um erro ao dropar a tabela temporária para o grafo do município {parametros.get('codigo_municipio')}. "
                      f"{ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e

    def salvar_grafo_municipio(self, gdf: GeoDataFrame, conexao_bd: Connection, parametros: dict) -> None:
        try:
            self.repository.salvar_geodataframe(gdf, conexao_bd, tabela="t_no_grafo_{0}".format(parametros.get("codigo_municipio")), schema="pg_temp")
        except Exception as e:
            log.error(msg=f"Houve um erro ao salvar o grafo do município {parametros.get('codigo_municipio')} no banco. "
                      f"{ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e

    def buscar_associacoes_origem_destino_por_codigo_municipio(self, conexao_bd: Connection, parametros: dict) -> DataFrame:
        try:
            return self.repository.buscar_associacoes_origem_destino_por_codigo_municipio(conexao_bd, parametros)
        except Exception as e:
            log.error(msg=f"Houve um erro ao buscar as associações de origens e destinos do município {parametros.get('codigo_municipio')}. "
                      f"{ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e