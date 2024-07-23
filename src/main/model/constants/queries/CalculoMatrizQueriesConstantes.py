from model.constants.ParametrosConstantes import ParametrosConstantes

class CalculoMatrizQueriesConstantes:

    CRIAR_TABELA_NO_GRAFO = '''
        DROP TABLE IF EXISTS t_no_grafo_municipio;

        CREATE TABLE t_no_grafo_municipio (
            codigo BIGINT NOT NULL,
            geometria GEOMETRY(POINT, 4326) NOT NULL
        );

        CREATE INDEX idx_t_no_grafo_municipio_codigo ON t_no_grafo_municipio(codigo);
        CREATE INDEX idx_t_no_grafo_municipio_geometria ON t_no_grafo_municipio USING GIST(geometria);
    '''

    BUSCAR_ASSOCIACOES_ORIGEM_DESTINO_POR_CODIGO = '''
        DROP TABLE IF EXISTS pg_temp.temp_area_analise;
        DROP TABLE IF EXISTS pg_temp.temp_amenidade_municipio;
        DROP TABLE IF EXISTS pg_temp.temp_associacao_origem_destino;
        DROP TABLE IF EXISTS pg_temp.temp_no_grafo_municipio;
        DROP TABLE IF EXISTS pg_temp.temp_origem;
        DROP TABLE IF EXISTS pg_temp.temp_distancia_origem_no_grafo;
        DROP TABLE IF EXISTS pg_temp.temp_equivalencia_origem;
        DROP TABLE IF EXISTS pg_temp.temp_destino;
        DROP TABLE IF EXISTS pg_temp.temp_distancia_destino_no_grafo;
        DROP TABLE IF EXISTS pg_temp.temp_equivalencia_destino;

        SELECT 
            codigo,
            ST_BUFFER(ST_CENTROID(ST_TRANSFORM(geometria, 3857)), %(raio_buffer)s) AS geometria
        INTO TEMP TABLE temp_area_analise
        FROM t_malha_hexagonal_municipio
        WHERE codigo_municipio = %(codigo_municipio)s;

        CREATE INDEX idx_temp_area_analise_codigo ON pg_temp.temp_area_analise(codigo);
        CREATE INDEX idx_temp_area_analise_geometria ON pg_temp.temp_area_analise USING GIST(geometria);

        SELECT
            codigo,
            ST_TRANSFORM(geometria, 3857) AS geometria
        INTO TEMP TABLE temp_amenidade_municipio
        FROM t_amenidade_municipio
        WHERE codigo_municipio = %(codigo_municipio)s;

        CREATE INDEX idx_temp_amenidade_municipio_codigo ON pg_temp.temp_amenidade_municipio(codigo);
        CREATE INDEX idx_temp_amenidade_municipio_geometria ON pg_temp.temp_amenidade_municipio USING GIST(geometria);

        SELECT 
            area_analise.codigo AS codigo_origem,
            ST_CENTROID(area_analise.geometria) AS ponto_origem,
            amenidade.codigo AS codigo_destino,
            amenidade.geometria AS ponto_destino
        INTO TEMP TABLE temp_associacao_origem_destino
        FROM temp_area_analise area_analise, temp_amenidade_municipio amenidade
        WHERE ST_CONTAINS(area_analise.geometria, amenidade.geometria);

        CREATE INDEX idx_temp_associacao_origem_destino_codigo_origem ON pg_temp.temp_associacao_origem_destino(codigo_origem);
        CREATE INDEX idx_temp_associacao_origem_destino_codigo_destino ON pg_temp.temp_associacao_origem_destino(codigo_destino);
        CREATE INDEX idx_temp_associacao_origem_destino_ponto_origem ON pg_temp.temp_associacao_origem_destino USING GIST(ponto_origem);
        CREATE INDEX idx_temp_associacao_origem_destino_ponto_destino ON pg_temp.temp_associacao_origem_destino USING GIST(ponto_destino);

        SELECT 
            codigo,
            ST_TRANSFORM(geometria, 3857) AS geometria
        INTO TEMP TABLE temp_no_grafo_municipio
        FROM t_no_grafo_municipio;

        CREATE INDEX idx_temp_no_grafo_municipio_codigo ON pg_temp.temp_no_grafo_municipio(codigo);
        CREATE INDEX idx_temp_no_grafo_municipio_geometria ON pg_temp.temp_no_grafo_municipio USING GIST(geometria);

        SELECT DISTINCT
            codigo_origem,
            ponto_origem
        INTO TEMP TABLE temp_origem
        FROM temp_associacao_origem_destino
        ORDER BY
            codigo_origem;
        
        CREATE INDEX idx_temp_origem_codigo_origem ON pg_temp.temp_origem(codigo_origem);
        CREATE INDEX idx_temp_origem_ponto_origem ON pg_temp.temp_origem USING GIST(ponto_origem);


        SELECT 
            origem.codigo_origem,
            no_grafo.codigo AS codigo_no_grafo,
            ST_DISTANCE(origem.ponto_origem, no_grafo.geometria) AS distancia
        INTO TEMP TABLE temp_distancia_origem_no_grafo
        FROM temp_origem origem, temp_no_grafo_municipio no_grafo
        WHERE ST_CONTAINS(ST_BUFFER(origem.ponto_origem, %(raio_equivalencia_origem)s), no_grafo.geometria);

        CREATE INDEX idx_temp_distancia_origem_no_grafo_codigo_origem ON pg_temp.temp_distancia_origem_no_grafo(codigo_origem);
        CREATE INDEX idx_temp_distancia_origem_no_grafo_codigo_no_grafo ON pg_temp.temp_distancia_origem_no_grafo(codigo_no_grafo);
        CREATE INDEX idx_temp_distancia_origem_no_grafo_distancia ON pg_temp.temp_distancia_origem_no_grafo(distancia);

        SELECT
            codigo_origem,
            codigo_no_grafo
        INTO TEMP TABLE temp_equivalencia_origem
        FROM temp_distancia_origem_no_grafo
        WHERE (codigo_origem, distancia) IN (
            SELECT
                codigo_origem,
                MIN(distancia)
            FROM temp_distancia_origem_no_grafo
            GROUP BY codigo_origem
        );

        CREATE INDEX idx_temp_equivalencia_origem_codigo_origem ON pg_temp.temp_equivalencia_origem(codigo_origem);
        CREATE INDEX idx_temp_equivalencia_origem_codigo_no_grafo ON pg_temp.temp_equivalencia_origem(codigo_no_grafo);

        SELECT DISTINCT
            codigo_destino,
            ponto_destino
        INTO TEMP TABLE temp_destino
        FROM temp_associacao_origem_destino
        ORDER BY
            codigo_destino;

        CREATE INDEX idx_temp_destino_codigo_destino ON pg_temp.temp_destino(codigo_destino);
        CREATE INDEX idx_temp_destino_ponto_destino ON pg_temp.temp_destino USING GIST(ponto_destino);
        
        SELECT 
            destino.codigo_destino,
            no_grafo.codigo AS codigo_no_grafo,
            ST_DISTANCE(destino.ponto_destino, no_grafo.geometria) AS distancia
        INTO TEMP TABLE temp_distancia_destino_no_grafo
        FROM temp_destino destino, temp_no_grafo_municipio no_grafo
        WHERE ST_CONTAINS(ST_BUFFER(destino.ponto_destino, %(raio_equivalencia_destino)s), no_grafo.geometria);

        CREATE INDEX idx_temp_distancia_destino_no_grafo_codigo_destino ON pg_temp.temp_distancia_destino_no_grafo(codigo_destino);
        CREATE INDEX idx_temp_distancia_destino_no_grafo_codigo_no_grafo ON pg_temp.temp_distancia_destino_no_grafo(codigo_no_grafo);
        CREATE INDEX idx_temp_distancia_destino_no_grafo_distancia ON pg_temp.temp_distancia_destino_no_grafo(distancia);

        SELECT
            codigo_destino,
            codigo_no_grafo
        INTO TEMP TABLE temp_equivalencia_destino
        FROM temp_distancia_destino_no_grafo
        WHERE (codigo_destino, distancia) IN (
            SELECT
                codigo_destino,
                MIN(distancia)
            FROM temp_distancia_destino_no_grafo
            GROUP BY codigo_destino
        );

        CREATE INDEX idx_temp_equivalencia_destino_codigo_destino ON pg_temp.temp_equivalencia_destino(codigo_destino);
        CREATE INDEX idx_temp_equivalencia_destino_codigo_no_grafo ON pg_temp.temp_equivalencia_destino(codigo_no_grafo);

        SELECT 
            associacao.codigo_origem,
            equivalencia_origem.codigo_no_grafo AS no_origem,
            associacao.codigo_destino,
            equivalencia_destino.codigo_no_grafo AS no_destino
        FROM temp_associacao_origem_destino associacao
        INNER JOIN temp_equivalencia_origem equivalencia_origem
            ON associacao.codigo_origem = equivalencia_origem.codigo_origem
        INNER JOIN temp_equivalencia_destino equivalencia_destino
            ON associacao.codigo_destino = equivalencia_destino.codigo_destino
        ORDER BY
            associacao.codigo_origem,
            associacao.codigo_destino;
    '''