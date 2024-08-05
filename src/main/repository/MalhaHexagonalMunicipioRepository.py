from model.constants.queries.MalhaHexagonalMunicipioQueriesConstantes import MalhaHexagonalMunicipioQueriesConstantes
from repository.BaseRepository import BaseRepository

from geopandas import GeoDataFrame
from sqlalchemy.engine import Connection

class MalhaHexagonalMunicipioRepository(BaseRepository):

    SCHEMA = "public"
    ENTIDADE = "t_malha_hexagonal_municipio"

    def __init__(self) -> None:
        super().__init__(schema=self.SCHEMA, entidade=self.ENTIDADE)

    def buscar_por_codigo_municipio(self, conexao_bd: Connection, parametros: dict) -> GeoDataFrame:
        return self.buscar_geodataframe(sql=MalhaHexagonalMunicipioQueriesConstantes.BUSCAR_POR_CODIGO_MUNICIPIO, conexao_bd=conexao_bd, parametros=parametros)