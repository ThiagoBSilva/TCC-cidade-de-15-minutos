class CalculoMatrizQueriesConstantes:

    DROPAR_TABELA_TEMPORARIA_GRAFO = '''
        DROP TABLE IF EXISTS pg_temp.t_no_grafo_%(codigo_municipio)s;
    '''

    BUSCAR_ASSOCIACOES_ORIGEM_DESTINO_POR_CODIGO = '''
        WITH t_area_analise AS (
            SELECT 
                codigo,
                ST_BUFFER(ST_CENTROID(ST_TRANSFORM(geometria, 3857)), %(raio_buffer)s) AS geometria
            FROM t_malha_hexagonal_municipio
            WHERE codigo_municipio = %(codigo_municipio)s
        ),
        t_amenidade AS (
            SELECT
                codigo,
                ST_TRANSFORM(geometria, 3857) AS geometria
            FROM t_amenidade_municipio
            WHERE codigo_municipio = %(codigo_municipio)s
        ),
        t_associacao_origem_destino AS (
            SELECT 
                area_analise.codigo AS codigo_origem,
                ST_CENTROID(area_analise.geometria) AS ponto_origem,
                amenidade.codigo AS codigo_destino,
                amenidade.geometria AS ponto_destino
            FROM t_area_analise area_analise, t_amenidade amenidade
            WHERE ST_CONTAINS(area_analise.geometria, amenidade.geometria)
        ),
        t_grafo_municipio AS (
            SELECT
                codigo,
                ST_TRANSFORM(geometria, 3857) AS geometria
            FROM pg_temp.t_no_grafo_%(codigo_municipio)s
        ),
        t_origem AS (
            SELECT DISTINCT
                codigo_origem AS codigo,
                ponto_origem AS ponto
            FROM t_associacao_origem_destino
        ),
        t_distancia_origem AS (
            SELECT
                origem.codigo AS codigo_origem,
                grafo.codigo AS no_origem,
                ST_DISTANCE(origem.ponto, grafo.geometria) AS distancia
            FROM t_origem origem, t_grafo_municipio grafo
        ),
        t_equivalencia_origem AS (
            SELECT 
                codigo_origem,
                no_origem
            FROM t_distancia_origem
            WHERE (codigo_origem, distancia) IN (
                SELECT 
                    codigo_origem,
                    MIN(distancia)
                FROM t_distancia_origem 
                GROUP BY codigo_origem
            )
        ),
        t_destino AS (
            SELECT DISTINCT
                codigo_destino AS codigo,
                ponto_destino AS ponto
            FROM t_associacao_origem_destino
        ),
        t_distancia_destino AS (
            SELECT
                destino.codigo AS codigo_destino,
                grafo.codigo AS no_destino,
                ST_DISTANCE(destino.ponto, grafo.geometria) AS distancia
            FROM t_destino destino, t_grafo_municipio grafo
        ),
        t_equivalencia_destino AS (
            SELECT 
                codigo_destino,
                no_destino
            FROM t_distancia_destino
            WHERE (codigo_destino, distancia) IN (
                SELECT 
                    codigo_destino,
                    MIN(distancia)
                FROM t_distancia_destino
                GROUP BY codigo_destino
            )
        )
        SELECT 
            associacao.codigo_origem,
            equivalencia_origem.no_origem,
            associacao.codigo_destino,
            equivalencia_destino.no_destino
        FROM t_associacao_origem_destino associacao
        INNER JOIN t_equivalencia_origem equivalencia_origem
            ON associacao.codigo_origem = equivalencia_origem.codigo_origem
        INNER JOIN t_equivalencia_destino equivalencia_destino
            ON associacao.codigo_destino = equivalencia_destino.codigo_destino
        ORDER BY
            associacao.codigo_origem,
            associacao.codigo_destino;
    '''