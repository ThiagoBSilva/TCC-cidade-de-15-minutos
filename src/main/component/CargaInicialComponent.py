from model.constants.MapeamentosConstantes import MapeamentosConstantes
from model.constants.ParametrosConstantes import ParametrosConstantes
from util.DataFrameUtil import DataFrameUtil
from util.ExceptionUtil import ExceptionUtil
from util.LoggerUtil import LoggerUtil

from geopandas import GeoDataFrame

log = LoggerUtil.recuperar_logger()
class CargaInicialComponent:

    def montar_carga_inicial(self) -> tuple[GeoDataFrame, GeoDataFrame]:
        try:
            gdf_unidade_federativa = DataFrameUtil.shapefile_para_geodataframe(arquivo_shapefile=ParametrosConstantes.CAMINHO_SHAPEFILE_UNIDADES_FEDERATIVAS)
            gdf_municipio = DataFrameUtil.shapefile_para_geodataframe(arquivo_shapefile=ParametrosConstantes.CAMINHO_SHAPEFILE_MUNICIPIOS)

            gdf_unidade_federativa = DataFrameUtil.renomear_colunas_dataframe(df=gdf_unidade_federativa, mapeamento=MapeamentosConstantes.COLUNAS_UNIDADE_FEDERATIVA_SHAPEFILE)
            gdf_municipio = DataFrameUtil.renomear_colunas_dataframe(df=gdf_municipio, mapeamento=MapeamentosConstantes.COLUNAS_MUNICIPIO_SHAPEFILE)

            gdf_unidade_federativa["regiao"] = gdf_unidade_federativa["regiao"].apply(lambda regiao: str(regiao).strip())
            gdf_municipio["codigo_unidade_federativa"] = gdf_municipio["codigo"].apply(lambda codigo: str(codigo)[:2])

            log.info(msg="Os dados para a carga inicial foram obtidos com sucesso.")
            return gdf_unidade_federativa, gdf_municipio
        except Exception as e:
            log.error(msg=f"Houve um erro ao montar a carga inicial. {ExceptionUtil.montar_exception_padrao(e)}")
            raise e