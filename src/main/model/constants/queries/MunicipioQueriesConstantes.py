from model.constants.ParametrosConstantes import ParametrosConstantes
from model.enums.StatusEtapaProcessamentoEnum import StatusEtapaProcessamentoEnum

class MunicipioQueriesConstantes:

    BUSCAR_QTDE_REGISTROS_PENDENTES_GERACAO_MALHA_HEXAGONAL = f'''
        SELECT
            COUNT(0) AS quantidade
        FROM t_municipio
        WHERE flag_geracao_malha_hexagonal = '{StatusEtapaProcessamentoEnum.PENDENTE.value}';
    '''

    BUSCAR_QTDE_REGISTROS_PENDENTES_EXTRACAO_AMENIDADES = f'''
        SELECT
            COUNT(0) AS quantidade
        FROM t_municipio
        WHERE flag_geracao_malha_hexagonal = '{StatusEtapaProcessamentoEnum.CONCLUIDO.value}'
        AND flag_extracao_amenidades = '{StatusEtapaProcessamentoEnum.PENDENTE.value}';
    '''

    BUSCAR_REGISTROS_PENDENTES_GERACAO_MALHA_HEXAGONAL = f'''
        SELECT
            codigo,
            nome,
            geometria
        FROM t_municipio
        WHERE flag_geracao_malha_hexagonal = '{StatusEtapaProcessamentoEnum.PENDENTE.value}'
        ORDER BY codigo
        LIMIT {ParametrosConstantes.BATCH_QTDE_REGISTROS_ETAPA_GERACAO_MALHA};
    '''

    BUSCAR_REGISTROS_PENDENTES_EXTRACAO_AMENIDADES = f'''
        SELECT
            codigo,
            nome,
            geometria
        FROM t_municipio
        WHERE flag_geracao_malha_hexagonal = '{StatusEtapaProcessamentoEnum.CONCLUIDO.value}'
        AND flag_extracao_amenidades = '{StatusEtapaProcessamentoEnum.PENDENTE.value}'
        ORDER BY codigo
        LIMIT {ParametrosConstantes.BATCH_QTDE_REGISTROS_ETAPA_EXTRACAO_AMENIDADES};
    '''

    ATUALIZAR_FLAG_GERACAO_MALHA_HEXAGONAL = '''
        UPDATE t_municipio
        SET flag_geracao_malha_hexagonal = %(flag)s
        WHERE codigo = %(codigo_municipio)s;
    '''

    ATUALIZAR_FLAG_EXTRACAO_AMENIDADES = '''
        UPDATE t_municipio
        SET flag_extracao_amenidades = %(flag)s
        WHERE codigo = %(codigo_municipio)s;
    '''