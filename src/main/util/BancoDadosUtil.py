from model.constants.ParametrosConstantes import ParametrosConstantes
from util.ExceptionUtil import ExceptionUtil
from util.LoggerUtil import LoggerUtil
from util.YamlUtil import YAMLUtil

from sqlalchemy import create_engine
from sqlalchemy.engine import Connection

log = LoggerUtil.recuperar_logger()
class BancoDadosUtil:
    
    @staticmethod
    def __recuperar_configuracao_banco() -> dict:
        try:
            parametros_aplicacao = YAMLUtil.converter_yaml_para_dict(arquivo_yaml=ParametrosConstantes.CAMINHO_APPLICATION_YAML)
            env = parametros_aplicacao.get("application").get("env")
            
            return parametros_aplicacao.get("database").get(env)
        
        except Exception as e:
            log.error(msg=f"Houve um erro ao recuperar as configurações do banco. {ExceptionUtil.montar_exception_padrao(e)}")
            raise e
        
    @staticmethod
    def estabelecer_conexao_banco() -> Connection:
        try:
            config = BancoDadosUtil.__recuperar_configuracao_banco()
            url_conexao = f"postgresql://{config.get('username')}:{config.get('password')}@{config.get('host')}:{config.get('port')}/{config.get('name')}"

            engine = create_engine(url=url_conexao)
            conexao_bd = engine.connect()

            log.info(msg=f"A conexão com o banco de dados {config.get('name')} foi estabelecida com sucesso.")
            return conexao_bd
        
        except Exception as e:
            log.error(msg=f"Houve um erro ao tentar estabelecer uma conexão o banco de dados. {ExceptionUtil.montar_exception_padrao(e)}")
            raise e
    
    @staticmethod
    def encerrar_conexao_banco(conexao_bd: Connection) -> None:
        try:
            conexao_bd.close()
            conexao_bd.engine.dispose()

            log.info(msg="A conexão com o banco de dados foi encerrada com sucesso.")
        except Exception as e:
            log.error(msg=f"Houve um erro ao tentar encerrar a conexão com o banco de dados. {ExceptionUtil.montar_exception_padrao(e)}")
            raise e