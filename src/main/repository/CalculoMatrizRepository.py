from model.constants.queries.CalculoMatrizQueriesConstantes import CalculoMatrizQueriesConstantes

from geopandas import GeoDataFrame
from pandas import DataFrame, read_sql
from sqlalchemy.engine import Connection

class CalculoMatrizRepository:

    def dropar_tabela_temporaria_grafo(self, conexao_bd: Connection, parametros: dict) -> None:
        conexao_bd.execute(statement=CalculoMatrizQueriesConstantes.DROPAR_TABELA_TEMPORARIA_GRAFO, codigo_municipio=parametros.get("codigo_municipio"))

    def salvar_geodataframe(self, gdf: GeoDataFrame, conexao_bd: Connection, tabela: str, schema: str) -> None:
        gdf.to_postgis(name=tabela, con=conexao_bd, schema=schema, if_exists="append", index=False)

    def buscar_associacoes_origem_destino_por_codigo_municipio(self, conexao_bd: Connection, parametros) -> DataFrame:
        return read_sql(sql=CalculoMatrizQueriesConstantes.BUSCAR_ASSOCIACOES_ORIGEM_DESTINO_POR_CODIGO, con=conexao_bd, params=parametros)