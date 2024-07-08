from repository.CargaInicialRepository import CargaInicialRepository
from util.ExceptionUtil import ExceptionUtil
from util.LoggerUtil import LoggerUtil

from sqlalchemy.engine import Connection

log = LoggerUtil.recuperar_logger()
class CargaInicialService: 

    repository = CargaInicialRepository()

    def dropar_tabelas_banco(self, conexao_bd: Connection) -> None:
        try:
            self.repository.dropar_tabelas_banco(conexao_bd)
            log.info(msg="As tabelas foram dropadas com sucesso no banco de dados.")

        except Exception as e:
            log.error(msg=f"Houve um erro ao dropar as tabelas do banco de dados. "
                          f"{ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e
        
    def criar_tabelas_banco(self, conexao_bd: Connection) -> None:
        try:
            self.repository.criar_tabelas_banco(conexao_bd)
            log.info(msg="As tabelas foram criadas com sucesso no banco de dados.")

        except Exception as e:
            log.error(msg=f"Houve um erro ao criar as tabelas no banco de dados. "
                          f"{ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e
        
    def popular_tabelas_iniciais(self, conexao_bd: Connection) -> None:
        try:
            self.repository.popular_tabelas_iniciais(conexao_bd)
            log.info(msg="As tabelas iniciais foram populadas com sucesso.")

        except Exception as e:
            log.error(msg=f"Houve um erro ao popular as tabelas iniciais. "
                          f"{ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e