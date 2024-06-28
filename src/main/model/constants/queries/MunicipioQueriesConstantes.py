from model.enums.StatusEtapaProcessamentoEnum import StatusEtapaProcessamentoEnum

class MunicipioQueriesConstantes:

    BUSCAR_QTDE_MUNICIPIOS_PENDENTES_GERACAO_MALHA_HEXAGONAL = f'''
        SELECT
            COUNT(0) AS quantidade
        FROM t_municipio
        WHERE flag_geracao_malha_hexagonal = '{StatusEtapaProcessamentoEnum.PENDENTE.value}';
    '''

    BUSCAR_POR_FLAG_GERACAO_MALHA_HEXAGONAL = '''
        SELECT
            codigo,
            nome,
            geometria
        FROM t_municipio
        WHERE flag_geracao_malha_hexagonal = %(flag)s
        ORDER BY codigo
        LIMIT %(limite)s;
    '''

    ATUALIZAR_FLAG_GERACAO_MALHA_HEXAGONAL = '''
        UPDATE t_municipio
        SET flag_geracao_malha_hexagonal = %(flag)s
        WHERE codigo = %(codigo_municipio)s;
    '''