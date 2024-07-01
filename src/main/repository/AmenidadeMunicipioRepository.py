from repository.BaseRepository import BaseRepository

class AmenidadeMunicipioRepository(BaseRepository):

    SCHEMA = "public"
    ENTIDADE = "t_amenidade_municipio"

    def __init__(self) -> None:
        super().__init__(schema=self.SCHEMA, entidade=self.ENTIDADE)