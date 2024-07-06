from repository.CalculoMatrizRepository import CalculoMatrizRepository
from util.ExceptionUtil import ExceptionUtil
from util.LoggerUtil import LoggerUtil

from geopandas import GeoDataFrame
from pandas import DataFrame
from sqlalchemy.engine import Connection
from time import sleep

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

    def salvar_grafo_municipio(self, gdf: GeoDataFrame, conexao_bd: Connection, parametros: dict, qtde_retentativas: int = 5) -> None:
        tentativa = 0
        while tentativa < qtde_retentativas:
            try:
                self.repository.salvar_geodataframe(gdf, conexao_bd, tabela="t_no_grafo_{0}".format(parametros.get("codigo_municipio")), schema="pg_temp")
                return
            
            except Exception as e:
                tentativa += 1
                log.error(msg=f"Houve um erro do tipo {type(e).__name__} ao salvar o grafo do município {parametros.get('codigo_municipio')}. Tentativa {tentativa}. "
                        f"{ExceptionUtil.montar_erro_exception_padrao(e)}")
                sleep(2 ** tentativa)
                
        raise Exception(f"Não foi possível gravar os dados do grafo do município {parametros.get('codigo_municipio')}, após {qtde_retentativas} tentativas.")

    def buscar_associacoes_origem_destino_por_codigo_municipio(self, conexao_bd: Connection, parametros: dict) -> DataFrame:
        try:
            return self.repository.buscar_associacoes_origem_destino_por_codigo_municipio(conexao_bd, parametros)
        except Exception as e:
            log.error(msg=f"Houve um erro ao buscar as associações de origens e destinos do município {parametros.get('codigo_municipio')}. "
                      f"{ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e