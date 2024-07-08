from model.constants.ParametrosConstantes import ParametrosConstantes
from repository.UnidadeFederativaRepository import UnidadeFederativaRepository
from util.ExceptionUtil import ExceptionUtil
from util.LoggerUtil import LoggerUtil

from geopandas import GeoDataFrame
from pandas import DataFrame
from sqlalchemy.engine import Connection

log = LoggerUtil.recuperar_logger()
class UnidadeFederativaService:

    repository = UnidadeFederativaRepository()

    def salvar_geodataframe(self, gdf: GeoDataFrame, conexao_bd: Connection) -> None:
        try:
            self.repository.salvar_geodataframe(gdf, conexao_bd)
            log.info(msg=f"Dados persistidos com sucesso na tabela {self.repository.ENTIDADE}.")
        except Exception as e:
            log.error(msg=f"Houve um erro ao persistir os dados do GeoDataFrame na tabela {self.repository.ENTIDADE}. {ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e
        
    def buscar_qtde_registros_pendentes_calculo_indice_15min(self, conexao_bd: Connection) -> DataFrame:
        try:
            return self.repository.buscar_qtde_registros_pendentes_calculo_indice_15min(conexao_bd)
        except Exception as e:
            log.error(msg="Houve um erro ao buscar a quantidade de unidades federativas pendentes de cálculo do índice de 15 minutos. " 
                      f"{ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e
        
    def buscar_registros_pendentes_calculo_indice_15min(self, conexao_bd: Connection) -> DataFrame:
        try:
            return self.repository.buscar_registros_pendentes_calculo_indice_15min(conexao_bd)
        except Exception as e:
            log.error(msg=f"Houve um erro ao buscar as unidades federativas pendentes de cálculo do índice de 15 minutos. {ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e
        
    def atualizar_flag_calculo_indice_15min(self, conexao_bd: Connection, parametros: dict) -> None:
        try:
            self.repository.atualizar_flag_calculo_indice_15min(conexao_bd, parametros)
        except Exception as e:
            log.error(msg=f"Houve um erro ao atualizar a flag de cálculo do índice de 15 minutos com os parâmetros {parametros}. "
                      f"{ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e