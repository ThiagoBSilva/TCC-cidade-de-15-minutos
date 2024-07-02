class ModalidadeTransporteQueriesConstantes:

    BUSCAR_TODOS_REGISTROS = '''
        SELECT
            codigo,
            nome,
            descricao,
            velocidade_media_kph
        FROM t_modalidade_transporte
        ORDER BY codigo;
    '''