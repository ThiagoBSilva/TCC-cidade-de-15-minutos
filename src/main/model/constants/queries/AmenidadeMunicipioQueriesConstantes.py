class AmenidadeMunicipioQueriesConstantes:

    BUSCAR_POR_CODIGO_MUNICIPIO = '''
        SELECT
            codigo,
            geometria
        FROM t_amenidade_municipio
        WHERE codigo_municipio = %(codigo_municipio)s
        ORDER BY codigo;
    '''