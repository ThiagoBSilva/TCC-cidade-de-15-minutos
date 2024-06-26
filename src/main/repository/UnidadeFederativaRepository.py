from repository.BaseRepository import BaseRepository

class UnidadeFederativaRepository(BaseRepository):

    SCHEMA = "public"
    ENTIDADE = "t_unidade_federativa"

    def __init__(self) -> None:
        super().__init__(self.SCHEMA, self.ENTIDADE)