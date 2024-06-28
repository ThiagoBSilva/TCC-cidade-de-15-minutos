from repository.BaseRepository import BaseRepository

class HistoricoErroRepository(BaseRepository):

    SCHEMA = "public"
    ENTIDADE = "t_historico_erro"

    def __init__(self) -> None:
        super().__init__(schema=self.SCHEMA, entidade=self.ENTIDADE)