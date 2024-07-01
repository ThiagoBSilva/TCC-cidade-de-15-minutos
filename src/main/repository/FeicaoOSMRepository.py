from model.constants.queries.FeicaoOSMQueriesConstantes import FeicaoOSMQueriesConstantes
from repository.BaseRepository import BaseRepository

from pandas import DataFrame
from sqlalchemy.engine import Connection

class FeicaoOSMRepository(BaseRepository):

    SCHEMA = "public"
    ENTIDADE = "t_feicao_osm"

    def __init__(self) -> None:
        super().__init__(schema=self.SCHEMA, entidade=self.ENTIDADE)

    def buscar_tags_osm(self, conexao_bd: Connection) -> DataFrame:
        return self.buscar_dataframe(sql=FeicaoOSMQueriesConstantes.BUSCAR_TAGS_OSM, conexao_bd=conexao_bd)