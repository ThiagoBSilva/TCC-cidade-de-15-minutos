from model.constants.MapeamentosConstantes import MapeamentosConstantes
from model.constants.ParametrosConstantes import ParametrosConstantes
from util.DataFrameUtil import DataFrameUtil
from util.ExceptionUtil import ExceptionUtil
from util.LoggerUtil import LoggerUtil

from numpy import ndarray, array
from geopandas import GeoDataFrame

log = LoggerUtil.recuperar_logger()
class CargaInicialComponent:

    def __tratar_coluna_regiao(self, gdf_unidade_federativa: GeoDataFrame) -> ndarray:
        try:
            array_regiao = gdf_unidade_federativa["regiao"].to_numpy()
            array_regiao = array(str(regiao).strip() for regiao in array_regiao)

            return array_regiao
        
        except Exception as e:
            log.error(msg=f"Houve um erro ao tratar a coluna 'regiao' para o GeoDataFrame de unidades federativas. {ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e

    def __adicionar_coluna_codigo_unidade_federativa(self, gdf_municipio: GeoDataFrame) -> ndarray:
        try:
            array_codigo = gdf_municipio["codigo"].to_numpy()
            array_codigo = array(str(codigo)[:2] for codigo in array_codigo)

            return array_codigo
        
        except Exception as e:
            log.error(msg=f"Houve um erro ao montar a coluna 'codigo_unidade_federativa' para o GeoDataFrame dos municípios. {ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e

    def montar_carga_inicial(self) -> tuple[GeoDataFrame, GeoDataFrame]:
        try:
            gdf_unidade_federativa = DataFrameUtil.shapefile_para_geodataframe(arquivo_shapefile=ParametrosConstantes.CAMINHO_SHAPEFILE_UNIDADES_FEDERATIVAS)
            gdf_unidade_federativa = DataFrameUtil.renomear_colunas_dataframe(df=gdf_unidade_federativa, mapeamento=MapeamentosConstantes.COLUNAS_UNIDADE_FEDERATIVA_SHAPEFILE)
            gdf_unidade_federativa["regiao"] = self.__tratar_coluna_regiao(gdf_unidade_federativa)

            gdf_municipio = DataFrameUtil.shapefile_para_geodataframe(arquivo_shapefile=ParametrosConstantes.CAMINHO_SHAPEFILE_MUNICIPIOS)
            gdf_municipio = DataFrameUtil.renomear_colunas_dataframe(df=gdf_municipio, mapeamento=MapeamentosConstantes.COLUNAS_MUNICIPIO_SHAPEFILE)
            gdf_municipio["codigo_unidade_federativa"] = self.__adicionar_coluna_codigo_unidade_federativa(gdf_municipio)

            log.info(msg="Os dados para a carga inicial foram obtidos com sucesso.")

            return gdf_unidade_federativa, gdf_municipio
        
        except Exception as e:
            log.error(msg=f"Houve um erro ao montar a carga inicial. {ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e