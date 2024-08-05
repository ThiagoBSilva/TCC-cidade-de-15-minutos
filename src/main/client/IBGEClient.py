from model.constants.ParametrosConstantes import ParametrosConstantes
from util.LoggerUtil import LoggerUtil

from retry import retry
from urllib.request import urlretrieve

log = LoggerUtil.recuperar_logger()
class IBGEClient:

    @retry(tries=ParametrosConstantes.RETRY_QTDE_MAX_RETENTATIVAS, delay=ParametrosConstantes.RETRY_DELAY_ENTRE_RETENTATIVAS, logger=log)
    def obter_shapefile_unidades_federativas(self) -> None:
        urlretrieve(url=ParametrosConstantes.URL_IBGE_SHAPEFILE_UNIDADES_FEDERATIVAS, filename=ParametrosConstantes.CAMINHO_SHAPEFILE_UNIDADES_FEDERATIVAS)
    
    @retry(tries=ParametrosConstantes.RETRY_QTDE_MAX_RETENTATIVAS, delay=ParametrosConstantes.RETRY_DELAY_ENTRE_RETENTATIVAS, logger=log)
    def obter_shapefile_municipios(self) -> None:
        urlretrieve(url=ParametrosConstantes.URL_IBGE_SHAPEFILE_MUNICIPIOS, filename=ParametrosConstantes.CAMINHO_SHAPEFILE_MUNICIPIOS)