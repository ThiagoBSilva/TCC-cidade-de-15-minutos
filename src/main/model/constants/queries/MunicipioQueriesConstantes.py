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

    BUSCAR_QTDE_REGISTROS_PENDENTES_CALCULO_MATRIZ_TEMPO_VIAGEM = f'''
        SELECT
            COUNT(0) AS quantidade
        FROM t_municipio
        WHERE flag_extracao_amenidades = '{StatusEtapaProcessamentoEnum.CONCLUIDO.value}'
        AND flag_calculo_matriz_tempo_viagem = '{StatusEtapaProcessamentoEnum.PENDENTE.value}';
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

    BUSCAR_REGISTROS_PENDENTES_CALCULO_MATRIZ_TEMPO_VIAGEM = f'''
        SELECT
            codigo,
            nome,
            geometria
        FROM t_municipio
        WHERE flag_extracao_amenidades = '{StatusEtapaProcessamentoEnum.CONCLUIDO.value}'
        AND flag_calculo_matriz_tempo_viagem = '{StatusEtapaProcessamentoEnum.PENDENTE.value}'
        ORDER BY codigo
        LIMIT {ParametrosConstantes.BATCH_QTDE_REGISTROS_ETAPA_CALCULO_MATRIZ_TEMPO_VIAGEM};
    '''

    BUSCAR_ASSOCIACOES_ORIGEM_DESTINO_POR_CODIGO = '''
        SELECT 
            malha.codigo AS codigo_origem,
            ST_ASTEXT(ST_CENTROID(malha.geometria)) AS ponto_origem,
            amenidade.codigo AS codigo_destino,
            ST_ASTEXT(amenidade.geometria) AS ponto_destino
        FROM t_malha_hexagonal_municipio malha, t_amenidade_municipio amenidade
        WHERE 
        ST_CONTAINS(
            ST_BUFFER(ST_CENTROID(ST_TRANSFORM(malha.geometria, 3857)), %(raio_buffer)s), 
            ST_TRANSFORM(amenidade.geometria, 3857)
        )
        AND malha.codigo_municipio = %(codigo_municipio)s
        AND amenidade.codigo_municipio = %(codigo_municipio)s
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

    ATUALIZAR_FLAG_CALCULO_MATRIZ_TEMPO_VIAGEM = '''
        UPDATE t_municipio
        SET flag_calculo_matriz_tempo_viagem = %(flag)s
        WHERE codigo = %(codigo_municipio)s;
    '''