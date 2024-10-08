from repository.MunicipioRepository import MunicipioRepository
from util.ExceptionUtil import ExceptionUtil
from util.LoggerUtil import LoggerUtil

from geopandas import GeoDataFrame
from pandas import DataFrame
from sqlalchemy.engine import Connection

log = LoggerUtil.recuperar_logger()
class MunicipioService:

    repository = MunicipioRepository()

    def salvar_geodataframe(self, gdf: GeoDataFrame, conexao_bd: Connection) -> None:
        try:
            self.repository.salvar_geodataframe(gdf, conexao_bd)
            log.info(msg=f"Dados persistidos com sucesso na tabela {self.repository.ENTIDADE}.")
            
        except Exception as e:
            log.error(msg=f"Houve um erro ao persistir os dados do GeoDataFrame na tabela {self.repository.ENTIDADE}. "
                          f"{ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e
        
    def buscar_qtde_registros_pendentes_geracao_malha_hexagonal(self, conexao_bd: Connection) -> DataFrame:
        try:
            return self.repository.buscar_qtde_registros_pendentes_geracao_malha_hexagonal(conexao_bd)
        except Exception as e:
            log.error(msg="Houve um erro ao buscar a quantidade de municípios pendentes de geração da malha hexagonal. "
                         f"{ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e
        
    def buscar_qtde_registros_pendentes_extracao_amenidades(self, conexao_bd: Connection) -> DataFrame:
        try:
            return self.repository.buscar_qtde_registros_pendentes_extracao_amenidades(conexao_bd)
        except Exception as e:
            log.error(msg="Houve um erro ao buscar a quantidade de municípios pendentes de extração de amenidade. "
                         f"{ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e
        
    def buscar_qtde_registros_pendentes_calculo_matriz_tempo_viagem(self, conexao_bd: Connection) -> DataFrame:
        try:
            return self.repository.buscar_qtde_registros_pendentes_calculo_matriz_tempo_viagem(conexao_bd)
        except Exception as e:
            log.error(msg="Houve um erro ao buscar a quantidade de municípios pendentes de cálculo da matriz de tempos de viagem. " 
                         f"{ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e
        
    def buscar_qtde_registros_pendentes_calculo_indice_15min(self, conexao_bd: Connection) -> DataFrame:
        try:
            return self.repository.buscar_qtde_registros_pendentes_calculo_indice_15min(conexao_bd)
        except Exception as e:
            log.error(msg="Houve um erro ao buscar a quantidade de municípios pendentes de cálculo do índice de 15 minutos. " 
                         f"{ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e
        
    def buscar_registros_pendentes_geracao_malha_hexagonal(self, conexao_bd: Connection) -> GeoDataFrame:
        try:
            return self.repository.buscar_registros_pendentes_geracao_malha_hexagonal(conexao_bd)
        except Exception as e:
            log.error(msg="Houve um erro ao buscar os municípios pendentes de geração da malha hexagonal. "
                         f"{ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e
        
    def buscar_registros_pendentes_extracao_amenidades(self, conexao_bd: Connection) -> GeoDataFrame:
        try:
            return self.repository.buscar_registros_pendentes_extracao_amenidades(conexao_bd)
        except Exception as e:
            log.error(msg="Houve um erro ao buscar os municípios pendentes de extração das amenidades. "
                         f"{ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e
        
    def buscar_registros_pendentes_calculo_matriz_tempo_viagem(self, conexao_bd: Connection) -> GeoDataFrame:
        try:
            return self.repository.buscar_registros_pendentes_calculo_matriz_tempo_viagem(conexao_bd)
        except Exception as e:
            log.error(msg="Houve um erro ao buscar os municípios pendentes de cálculo da matriz de tempos de viagem. "
                         f"{ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e
        
    def buscar_registros_pendentes_calculo_indice_15min(self, conexao_bd: Connection) -> DataFrame:
        try:
            return self.repository.buscar_registros_pendentes_calculo_indice_15min(conexao_bd)
        except Exception as e:
            log.error(msg="Houve um erro ao buscar os municípios pendentes de cálculo do índice de 15 minutos. "
                         f"{ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e
        
    def buscar_associacoes_origem_destino_por_codigo(self, conexao_bd: Connection, parametros: dict) -> GeoDataFrame:
        try:
            return self.repository.buscar_associacoes_origem_destino_por_codigo(conexao_bd, parametros)
        except Exception as e:
            log.error(msg=f"Houve um erro ao buscar as associações de origens e destinos com os parâmetros {parametros}. "
                          f"{ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e
        
    def atualizar_flag_geracao_malha_hexagonal(self, conexao_bd: Connection, parametros: dict) -> None:
        try:
            self.repository.atualizar_flag_geracao_malha_hexagonal(conexao_bd, parametros)
        except Exception as e:
            log.error(msg=f"Houve um erro ao atualizar a flag de geração da malha hexagonal com os parâmetros {parametros}. "
                          f"{ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e
        
    def atualizar_flag_extracao_amenidades(self, conexao_bd: Connection, parametros: dict) -> None:
        try:
            self.repository.atualizar_flag_extracao_amenidades(conexao_bd, parametros)
        except Exception as e:
            log.error(msg=f"Houve um erro ao atualizar a flag de extração das amenidades com os parâmetros {parametros}. "
                          f"{ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e
        
    def atualizar_flag_calculo_matriz_tempo_viagem(self, conexao_bd: Connection, parametros: dict) -> None:
        try:
            self.repository.atualizar_flag_calculo_matriz_tempo_viagem(conexao_bd, parametros)
        except Exception as e:
            log.error(msg=f"Houve um erro ao atualizar a flag de cálculo da matriz de tempos de viagem com os parâmetros {parametros}. "
                          f"{ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e
        
    def atualizar_flag_calculo_indice_15min(self, conexao_bd: Connection, parametros: dict) -> None:
        try:
            self.repository.atualizar_flag_calculo_indice_15min(conexao_bd, parametros)
        except Exception as e:
            log.error(msg=f"Houve um erro ao atualizar a flag de cálculo do índice de 15 minutos com os parâmetros {parametros}. "
                          f"{ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e