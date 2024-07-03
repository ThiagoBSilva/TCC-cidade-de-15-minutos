from client.IBGEClient import IBGEClient
from model.constants.ParametrosConstantes import ParametrosConstantes
from util.ExceptionUtil import ExceptionUtil
from util.LoggerUtil import LoggerUtil
from util.OSUtil import OSUtil

log = LoggerUtil.recuperar_logger()
class IBGEClientService:

    client = IBGEClient()

    def obter_shapefile_unidades_federativas(self) -> None:
        try:
            if OSUtil.verificar_arquivo_existente(arquivo=ParametrosConstantes.CAMINHO_SHAPEFILE_UNIDADES_FEDERATIVAS):
                log.info(msg="O shapefile das unidades federativas já se encontra no diretório de dados.")
                return
            
            self.client.obter_shapefile_unidades_federativas()
            log.info(msg="O shapefile das unidades federativas foi obtido com sucesso.")
        except Exception as e:
            log.error(msg=f"Houve um erro ao buscar o shapefile das unidades federativas. {ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e
        
    def obter_shapefile_municipios(self) -> None:
        try:
            if OSUtil.verificar_arquivo_existente(arquivo=ParametrosConstantes.CAMINHO_SHAPEFILE_MUNICIPIOS):
                log.info(msg="O shapefile dos municípios já se encontra no diretório de dados.")
                return
            
            self.client.obter_shapefile_municipios()
            log.info(msg="O shapefile dos municípios foi obtido com sucesso.")
        except Exception as e:
            log.error(msg=f"Houve um erro ao buscar o shapefile dos municípios. {ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e
        