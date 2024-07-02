from model.constants.queries.AmenidadeMunicipioQueriesConstantes import AmenidadeMunicipioQueriesConstantes
from repository.BaseRepository import BaseRepository

from geopandas import GeoDataFrame
from sqlalchemy.engine import Connection

class AmenidadeMunicipioRepository(BaseRepository):

    SCHEMA = "public"
    ENTIDADE = "t_amenidade_municipio"

    def __init__(self) -> None:
        super().__init__(schema=self.SCHEMA, entidade=self.ENTIDADE)

    def buscar_por_codigo_municipio(self, conexao_bd: Connection, parametros: dict) -> GeoDataFrame:
        return self.buscar_geodataframe(sql=AmenidadeMunicipioQueriesConstantes.BUSCAR_POR_CODIGO_MUNICIPIO, conexao_bd=conexao_bd, parametros=parametros)