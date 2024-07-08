from model.constants.queries.CalculoIndiceQueriesConstantes import CalculoIndiceQueriesConstantes

from sqlalchemy.engine import Connection

class CalculoIndiceRepository:

    def calcular_indice_15min_hexagono(self, conexao_bd: Connection, parametros: dict) -> None:
        conexao_bd.execute(
            statement=CalculoIndiceQueriesConstantes.CALCULAR_INDICE_15MIN_HEXAGONO,
            codigo_municipio = parametros.get("codigo_municipio")
        )

    def calcular_indice_15min_municipio(self, conexao_bd: Connection, parametros: dict) -> None:
        conexao_bd.execute(
            statement=CalculoIndiceQueriesConstantes.CALCULAR_INDICE_15MIN_MUNICIPIO,
            codigo_municipio = parametros.get("codigo_municipio")
        )

    def calcular_indice_15min_unidade_federativa(self, conexao_bd: Connection, parametros: dict) -> None:
        conexao_bd.execute(
            statement=CalculoIndiceQueriesConstantes.CALCULAR_INDICE_15MIN_UNIDADE_FEDERATIVA,
            codigo_unidade_federativa = parametros.get("codigo_unidade_federativa")
        )