from model.constants.ParametrosConstantes import ParametrosConstantes
from util.ExceptionUtil import ExceptionUtil
from util.LoggerUtil import LoggerUtil

from geopandas import GeoDataFrame, read_file
from pandas import DataFrame, Series

from numpy import ndarray
import dask.dataframe as dd

log = LoggerUtil.recuperar_logger()
class DataFrameUtil:

    @staticmethod
    def shapefile_para_geodataframe(arquivo_shapefile: str) -> GeoDataFrame:
        try:
            return read_file(filename=arquivo_shapefile)
        except Exception as e:
            log.error(msg=f"Houve um erro ao obter o GeoDataFrame a partir do shapefile especificado no caminho {arquivo_shapefile}. {ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e

    @staticmethod
    def renomear_colunas_dataframe(df: DataFrame | GeoDataFrame, mapeamento: dict) -> DataFrame | GeoDataFrame:
        try:
            colunas_a_remover = list(set(df.columns) - set(mapeamento.keys()))
            df = df.drop(columns=colunas_a_remover).rename(columns=mapeamento)

            return df if type(df) == DataFrame else df.set_geometry(col=ParametrosConstantes.GEOMETRIA_COLUNA_DEFAULT)
        except Exception as e:
            log.error(msg=f"Houve um erro ao renomar as colunas do {type(df).__name__}. {ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e
    
    @staticmethod
    def alterar_crs_geodataframe(gdf: GeoDataFrame, crs: str) -> GeoDataFrame:
        try:
            log.info(msg=f"Alterando o CRS do GeoDataFrame de {gdf.crs.__name__} para {crs}.")
            return gdf.to_crs(crs)
        except Exception as e:
            log.error(msg=f"Houve um erro ao alterar o CRS do GeoDataFrame de {gdf.crs.__name__} para {crs}. {ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e
    
    @staticmethod
    def processar_dataframe_dask(df: DataFrame | GeoDataFrame, funcao: any, meta: DataFrame | Series, qtde_particoes: int, **kwargs) -> DataFrame | Series:
        try:
            dask_dataframe = dd.from_pandas(data=df, npartitions=qtde_particoes)
            return dask_dataframe.map_partitions(func=funcao, meta=meta, **kwargs).compute()
        except Exception as e:
            log.error(msg=f"Houve um erro ao processar o {type(df).__name__} com o Dask. {ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e
    
    @staticmethod
    def dict_para_dataframe(dict_dados: dict) -> DataFrame:
        try:
            return DataFrame.from_dict(data=dict_dados)
        except Exception as e:
            log.error(msg=f"Houve um erro ao gerar o DataFrame a partir do dict. {ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e

    @staticmethod
    def dict_para_geodataframe(dict_dados: dict, coluna_geometria: str = ParametrosConstantes.GEOMETRIA_COLUNA_DEFAULT, crs: str = ParametrosConstantes.GEOMETRIA_CRS_DEFAULT) -> GeoDataFrame:
        try:
            return GeoDataFrame.from_dict(data=dict_dados, geometry=coluna_geometria, crs=crs)
        except Exception as e:
            log.error(msg=f"Houve um erro ao gerar o GeoDataFrame a partir do dict. {ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e