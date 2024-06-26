from repository.BaseRepository import BaseRepository

class MunicipioRepository(BaseRepository):

    SCHEMA = "public"
    ENTIDADE = "t_municipio"

    def __init__(self) -> None:
        super().__init__(schema=self.SCHEMA, entidade=self.ENTIDADE)