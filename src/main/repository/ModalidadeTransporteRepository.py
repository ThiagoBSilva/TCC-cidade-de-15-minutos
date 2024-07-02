from model.constants.queries.ModalidadeTransporteQueriesConstantes import ModalidadeTransporteQueriesConstantes
from repository.BaseRepository import BaseRepository

from pandas import DataFrame
from sqlalchemy.engine import Connection

class ModalidadeTransporteRepository(BaseRepository):

    SCHEMA = "public"
    ENTIDADE = "t_modalidade_transporte"
    
    def __init__(self) -> None:
        super().__init__(schema=self.SCHEMA, entidade=self.ENTIDADE)

    def buscar_todos_registros(self, conexao_bd: Connection) -> DataFrame:
        return self.buscar_dataframe(sql=ModalidadeTransporteQueriesConstantes.BUSCAR_TODOS_REGISTROS, conexao_bd=conexao_bd)