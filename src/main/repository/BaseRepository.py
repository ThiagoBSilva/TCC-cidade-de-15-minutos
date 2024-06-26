from geopandas import GeoDataFrame
from pandas import DataFrame
from sqlalchemy.engine import Connection

class BaseRepository:

    def __init__(self, schema: str, entidade: str) -> None:
        self.schema = schema
        self.entidade = entidade

    def salvar_dataframe(self, df: DataFrame, conexao_bd: Connection) -> None:
        df.to_sql(name=self.entidade, con=conexao_bd, schema=self.schema, if_exists="append")

    def salvar_geodataframe(self, gdf: GeoDataFrame, conexao_bd: Connection) -> None:
        gdf.to_postgis(name=self.entidade, con=conexao_bd, schema=self.schema, if_exists="append")