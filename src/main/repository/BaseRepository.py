from model.constants.ParametrosConstantes import ParametrosConstantes

from geopandas import GeoDataFrame, read_postgis
from pandas import DataFrame, read_sql
from sqlalchemy.engine import Connection

class BaseRepository:

    def __init__(self, schema: str, entidade: str) -> None:
        self.schema = schema
        self.entidade = entidade

    def salvar_dataframe(self, df: DataFrame, conexao_bd: Connection) -> None:
        df.to_sql(name=self.entidade, con=conexao_bd, schema=self.schema, if_exists="append", index=False)

    def salvar_geodataframe(self, gdf: GeoDataFrame, conexao_bd: Connection, crs: str = ParametrosConstantes.CRS_DEFAULT) -> None:
        gdf.to_crs(crs).to_postgis(name=self.entidade, con=conexao_bd, schema=self.schema, if_exists="append", index=False)

    def buscar_dataframe(self, sql: str, conexao_bd: Connection, parametros: dict = None) -> DataFrame:
        return read_sql(sql=sql, con=conexao_bd, params=parametros)
    
    def buscar_geodataframe(self, sql: str, conexao_bd: Connection, coluna_geometria: str = ParametrosConstantes.COLUNA_GEOMETRIA_DEFAULT, parametros: dict = None) -> GeoDataFrame:
        return read_postgis(sql=sql, con=conexao_bd, geom_col=coluna_geometria, params=parametros)
    
    def executar_sql(self, sql: str, conexao_bd: Connection, **kwargs) -> None:
        conexao_bd.execute(statement=sql, **kwargs)
