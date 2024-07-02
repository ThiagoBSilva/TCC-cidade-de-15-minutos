class MalhaHexagonalMunicipioQueriesConstantes:

    BUSCAR_POR_CODIGO_MUNICIPIO = '''
        SELECT
            codigo,
            geometria
        FROM t_malha_hexagonal_municipio
        WHERE codigo_municipio = %(codigo_municipio)s
        ORDER BY codigo;
    '''