from repository.CalculoIndiceRepository import CalculoIndiceRepository
from util.ExceptionUtil import ExceptionUtil
from util.LoggerUtil import LoggerUtil

from sqlalchemy.engine import Connection

log = LoggerUtil.recuperar_logger()
class CalculoIndiceService:

    repository = CalculoIndiceRepository()

    def calcular_indice_15min_hexagono(self, conexao_bd: Connection, parametros: dict) -> None:
        try:
            self.repository.calcular_indice_15min_hexagono(conexao_bd, parametros)
        except Exception as e:
            log.error(msg=f"Houve um erro ao calcular o índice de 15 minutos dos hexágonos para o município {parametros.get('codigo_municipio')}. "
                      f"{ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e
        
    def calcular_indice_15min_municipio(self, conexao_bd: Connection, parametros: dict) -> None:
        try:
            self.repository.calcular_indice_15min_municipio(conexao_bd, parametros)
        except Exception as e:
            log.error(msg=f"Houve um erro ao calcular o índice de 15 minutos para o município {parametros.get('codigo_municipio')}. "
                      f"{ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e
        
    def calcular_indice_15min_unidade_federativa(self, conexao_bd: Connection, parametros: dict) -> None:
        try:
            self.repository.calcular_indice_15min_unidade_federativa(conexao_bd, parametros)
        except Exception as e:
            log.error(msg=f"Houve um erro ao calcular o índice de 15 minutos para a unidade_federativa {parametros.get('codigo_unidade_federativa')}. "
                      f"{ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e