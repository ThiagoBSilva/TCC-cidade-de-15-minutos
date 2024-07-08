from model.enums.StatusEtapaProcessamentoEnum import StatusEtapaProcessamentoEnum

class UnidadeFederativaQueriesConstantes:

    BUSCAR_QTDE_REGISTROS_PENDENTES_CALCULO_INDICE_15MIN = f'''
        SELECT
            COUNT(0) AS quantidade
        FROM t_unidade_federativa
        WHERE flag_calculo_indice_15min = '{StatusEtapaProcessamentoEnum.PENDENTE.value}';
    '''

    BUSCAR_REGISTROS_PENDENTES_CALCULO_INDICE_15MIN = f'''
        SELECT
            codigo,
            nome
        FROM t_unidade_federativa
        WHERE flag_calculo_indice_15min = '{StatusEtapaProcessamentoEnum.PENDENTE.value}'
        ORDER BY codigo;
    '''

    ATUALIZAR_FLAG_CALCULO_INDICE_15MIN = '''
        UPDATE t_unidade_federativa
        SET flag_calculo_indice_15min = %(flag)s
        WHERE codigo = %(codigo_unidade_federativa)s;
    '''