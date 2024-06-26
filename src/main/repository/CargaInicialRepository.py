from model.constants.queries.CargaInicialQueriesConstantes import CargaInicialQueriesConstantes

from sqlalchemy.engine import Connection

class CargaInicialRepository:

    def dropar_tabelas_banco(self, conexao_bd: Connection) -> None:
        conexao_bd.execute(statement=CargaInicialQueriesConstantes.DROPAR_TABELAS_BANCO)

    def criar_tabelas_banco(self, conexao_bd: Connection) -> None:
        conexao_bd.execute(statement=CargaInicialQueriesConstantes.CRIAR_TABELAS_BANCO)

    def popular_tabelas_iniciais(self, conexao_bd: Connection) -> None:
        conexao_bd.execute(statement=CargaInicialQueriesConstantes.POPULAR_TABELAS_INICIAIS)