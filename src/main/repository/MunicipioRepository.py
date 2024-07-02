from model.constants.queries.MunicipioQueriesConstantes import MunicipioQueriesConstantes
from repository.BaseRepository import BaseRepository

from geopandas import GeoDataFrame
from pandas import DataFrame
from sqlalchemy.engine import Connection

class MunicipioRepository(BaseRepository):

    SCHEMA = "public"
    ENTIDADE = "t_municipio"

    def __init__(self) -> None:
        super().__init__(schema=self.SCHEMA, entidade=self.ENTIDADE)

    def buscar_qtde_registros_pendentes_geracao_malha_hexagonal(self, conexao_bd: Connection) -> DataFrame:
        return self.buscar_dataframe(sql=MunicipioQueriesConstantes.BUSCAR_QTDE_REGISTROS_PENDENTES_GERACAO_MALHA_HEXAGONAL, conexao_bd=conexao_bd)
    
    def buscar_qtde_registros_pendentes_extracao_amenidades(self, conexao_bd: Connection) -> DataFrame:
        return self.buscar_dataframe(sql=MunicipioQueriesConstantes.BUSCAR_QTDE_REGISTROS_PENDENTES_EXTRACAO_AMENIDADES, conexao_bd=conexao_bd)
    
    def buscar_qtde_registros_pendentes_calculo_matriz_tempo_viagem(self, conexao_bd: Connection) -> DataFrame:
        return self.buscar_dataframe(sql=MunicipioQueriesConstantes.BUSCAR_QTDE_REGISTROS_PENDENTES_CALCULO_MATRIZ_TEMPO_VIAGEM, conexao_bd=conexao_bd)
    
    def buscar_registros_pendentes_geracao_malha_hexagonal(self, conexao_bd: Connection) -> GeoDataFrame:
        return self.buscar_geodataframe(sql=MunicipioQueriesConstantes.BUSCAR_REGISTROS_PENDENTES_GERACAO_MALHA_HEXAGONAL, conexao_bd=conexao_bd)
    
    def buscar_registros_pendentes_extracao_amenidades(self, conexao_bd: Connection) -> GeoDataFrame:
        return self.buscar_geodataframe(sql=MunicipioQueriesConstantes.BUSCAR_REGISTROS_PENDENTES_EXTRACAO_AMENIDADES, conexao_bd=conexao_bd)

    def buscar_registros_pendentes_calculo_matriz_tempo_viagem(self, conexao_bd: Connection) -> GeoDataFrame:
        return self.buscar_geodataframe(sql=MunicipioQueriesConstantes.BUSCAR_REGISTROS_PENDENTES_CALCULO_MATRIZ_TEMPO_VIAGEM, conexao_bd=conexao_bd)

    def atualizar_flag_geracao_malha_hexagonal(self, conexao_bd: Connection, parametros: dict) -> None:
        self.executar_sql(
            sql=MunicipioQueriesConstantes.ATUALIZAR_FLAG_GERACAO_MALHA_HEXAGONAL, 
            conexao_bd=conexao_bd, 
            flag=parametros.get("flag"), 
            codigo_municipio=parametros.get("codigo_municipio")
        )

    def atualizar_flag_extracao_amenidades(self, conexao_bd: Connection, parametros: dict) -> None:
        self.executar_sql(
            sql=MunicipioQueriesConstantes.ATUALIZAR_FLAG_EXTRACAO_AMENIDADES, 
            conexao_bd=conexao_bd, 
            flag=parametros.get("flag"), 
            codigo_municipio=parametros.get("codigo_municipio")
        )

    def atualizar_flag_calculo_matriz_tempo_viagem(self, conexao_bd: Connection, parametros: dict) -> None:
        self.executar_sql(
            sql=MunicipioQueriesConstantes.ATUALIZAR_FLAG_CALCULO_MATRIZ_TEMPO_VIAGEM, 
            conexao_bd=conexao_bd, 
            flag=parametros.get("flag"), 
            codigo_municipio=parametros.get("codigo_municipio")
        )