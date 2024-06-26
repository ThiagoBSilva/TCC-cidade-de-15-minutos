from model.constants.ParametrosConstantes import ParametrosConstantes
from util.ExceptionUtil import ExceptionUtil
from util.LoggerUtil import LoggerUtil

from geopandas import GeoDataFrame, read_file
from pandas import DataFrame

log = LoggerUtil.recuperar_logger()
class DataFrameUtil:

    @staticmethod
    def shapefile_para_geodataframe(arquivo_shapefile: str) -> GeoDataFrame:
        try:
            return read_file(filename=arquivo_shapefile)
        except Exception as e:
            log.error(msg=f"Houve um erro ao obter o GeoDataFrame a partir do shapefile especificado no caminho {arquivo_shapefile}. {ExceptionUtil.montar_exception_padrao(e)}")
            raise e
    
    @staticmethod
    def renomear_colunas_dataframe(df: DataFrame | GeoDataFrame, mapeamento: dict) -> DataFrame | GeoDataFrame:
        try:
            colunas_a_remover = list(set(df.columns) - set(mapeamento.keys()))
            df = df.drop(columns=colunas_a_remover).rename(columns=mapeamento)

            return df if type(df) == DataFrame else df.set_geometry(col=ParametrosConstantes.COLUNA_GEOMETRIA_DEFAULT)
        except Exception as e:
            log.error(msg=f"Houve um erro ao renomar as colunas do {type(df).__name__}. {ExceptionUtil.montar_exception_padrao(e)}")
            raise e
    
    @staticmethod
    def alterar_crs_geodataframe(gdf: GeoDataFrame, crs: str) -> GeoDataFrame:
        try:
            log.info(msg=f"Alterando o CRS do GeoDataFrame de {gdf.crs.__name__} para {crs}.")
            return gdf.to_crs(crs)
        except Exception as e:
            log.error(msg=f"Houve um erro ao alterar o CRS do GeoDataFrame de {gdf.crs.__name__} para {crs}. {ExceptionUtil.montar_exception_padrao(e)}")
            raise e