from repository.BaseRepository import BaseRepository

class MalhaHexagonalMunicipioRepository(BaseRepository):

    SCHEMA = "public"
    ENTIDADE = "t_malha_hexagonal_municipio"

    def __init__(self) -> None:
        super().__init__(schema=self.SCHEMA, entidade=self.ENTIDADE)