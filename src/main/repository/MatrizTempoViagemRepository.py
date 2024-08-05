from repository.BaseRepository import BaseRepository

class MatrizTempoViagemRepository(BaseRepository):

    SCHEMA = "public"
    ENTIDADE = "t_matriz_tempo_viagem"

    def __init__(self) -> None:
        super().__init__(schema=self.SCHEMA, entidade=self.ENTIDADE)