from model.constants.queries.UnidadeFederativaQueriesConstantes import UnidadeFederativaQueriesConstantes
from repository.BaseRepository import BaseRepository

from pandas import DataFrame
from sqlalchemy.engine import Connection

class UnidadeFederativaRepository(BaseRepository):

    SCHEMA = "public"
    ENTIDADE = "t_unidade_federativa"

    def __init__(self) -> None:
        super().__init__(self.SCHEMA, self.ENTIDADE)

    def buscar_qtde_registros_pendentes_calculo_indice_15min(self, conexao_bd: Connection) -> DataFrame:
        return self.buscar_dataframe(sql=UnidadeFederativaQueriesConstantes.BUSCAR_QTDE_REGISTROS_PENDENTES_CALCULO_INDICE_15MIN, conexao_bd=conexao_bd)

    def buscar_registros_pendentes_calculo_indice_15min(self, conexao_bd: Connection) -> DataFrame:
        return self.buscar_dataframe(sql=UnidadeFederativaQueriesConstantes.BUSCAR_REGISTROS_PENDENTES_CALCULO_INDICE_15MIN, conexao_bd=conexao_bd)
    
    def atualizar_flag_calculo_indice_15min(self, conexao_bd: Connection, parametros: dict) -> None:
        self.executar_sql(
            sql=UnidadeFederativaQueriesConstantes.ATUALIZAR_FLAG_CALCULO_INDICE_15MIN, 
            conexao_bd=conexao_bd, 
            flag=parametros.get("flag"), 
            codigo_unidade_federativa=parametros.get("codigo_unidade_federativa")
        )