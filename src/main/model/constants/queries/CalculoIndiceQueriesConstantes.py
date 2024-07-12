class CalculoIndiceQueriesConstantes:

    CALCULAR_INDICE_15MIN_HEXAGONO = '''
        DROP TABLE IF EXISTS pg_temp.temp_contagem_categorias_15min;
        DROP TABLE IF EXISTS pg_temp.temp_contagem_amenidades_15min;
        DROP TABLE IF EXISTS pg_temp.temp_dados_hexagono_municipio;
        DROP TABLE IF EXISTS pg_temp.temp_indice_p1;
        DROP TABLE IF EXISTS pg_temp.temp_indice_p2;

        SELECT 
            COUNT(0) AS contagem
        INTO TEMP TABLE temp_contagem_categorias_15min
        FROM t_categoria_amenidade
        WHERE codigo_categoria_pai IS NULL;

        SELECT
            COUNT(DISTINCT feicao.codigo_categoria_amenidade) AS contagem
        INTO TEMP TABLE temp_contagem_amenidades_15min
        FROM t_amenidade_municipio amenidade
        INNER JOIN t_feicao_osm feicao
            ON amenidade.codigo_feicao_osm = feicao.codigo
        WHERE amenidade.codigo_municipio = %(codigo_municipio)s;

        SELECT
            matriz.codigo_hexagono,
            matriz.codigo_modalidade_transporte,
            COUNT(DISTINCT categoria.codigo_categoria_pai) AS contagem_categoria_distinta,
            COUNT(DISTINCT feicao.codigo_categoria_amenidade) AS contagem_amenidade_distinta
        INTO TEMP TABLE temp_dados_hexagono_municipio
        FROM t_matriz_tempo_viagem matriz
        INNER JOIN t_malha_hexagonal_municipio malha
            ON matriz.codigo_hexagono = malha.codigo
        INNER JOIN t_amenidade_municipio amenidade
            ON matriz.codigo_amenidade = amenidade.codigo
        INNER JOIN t_feicao_osm feicao
            ON amenidade.codigo_feicao_osm = feicao.codigo
        INNER JOIN t_categoria_amenidade categoria
            ON categoria.codigo = feicao.codigo_categoria_amenidade
        WHERE malha.codigo_municipio = %(codigo_municipio)s
        AND matriz.tempo_viagem_seg <= 900
        GROUP BY
            matriz.codigo_hexagono,
            matriz.codigo_modalidade_transporte
        ORDER BY
            matriz.codigo_hexagono,
            matriz.codigo_modalidade_transporte;

        SELECT
            dados_hex.codigo_hexagono,
            dados_hex.codigo_modalidade_transporte,
            ROUND(dados_hex.contagem_categoria_distinta::NUMERIC / categ_15min.contagem::NUMERIC * 100, 2) AS valor_indice
        INTO TEMP TABLE temp_indice_p1
        FROM temp_dados_hexagono_municipio dados_hex, temp_contagem_categorias_15min categ_15min;    

        SELECT
            dados_hex.codigo_hexagono,
            dados_hex.codigo_modalidade_transporte,
            ROUND(dados_hex.contagem_amenidade_distinta::NUMERIC / ameni_15min.contagem::NUMERIC * 100, 2) AS valor_indice
        INTO TEMP TABLE temp_indice_p2
        FROM temp_dados_hexagono_municipio dados_hex, temp_contagem_amenidades_15min ameni_15min;

        
        INSERT INTO t_indice_hexagono (codigo_hexagono, codigo_modalidade_transporte, indice)
        SELECT 
            idx_p1.codigo_hexagono,
            idx_p1.codigo_modalidade_transporte,
            ROUND((idx_p1.valor_indice + idx_p2.valor_indice) / 2, 2) AS indice
        FROM temp_indice_p1 idx_p1
        INNER JOIN temp_indice_p2 idx_p2
            ON idx_p1.codigo_hexagono = idx_p2.codigo_hexagono
            AND idx_p1.codigo_modalidade_transporte = idx_p2.codigo_modalidade_transporte;
    '''

    CALCULAR_INDICE_15MIN_MUNICIPIO = '''
        INSERT INTO t_indice_municipio (codigo_municipio, codigo_modalidade_transporte, indice)
        SELECT
            malha.codigo_municipio,
            codigo_modalidade_transporte,
            ROUND(SUM(indice_hex.indice) / COUNT(0), 2) AS indice
        FROM t_indice_hexagono indice_hex
        INNER JOIN t_malha_hexagonal_municipio malha
            ON indice_hex.codigo_hexagono = malha.codigo
        WHERE malha.codigo_municipio = %(codigo_municipio)s
        GROUP BY
            malha.codigo_municipio,
            indice_hex.codigo_modalidade_transporte;
    '''

    CALCULAR_INDICE_15MIN_UNIDADE_FEDERATIVA = '''
        INSERT INTO t_indice_unidade_federativa (codigo_unidade_federativa, codigo_modalidade_transporte, indice)
        SELECT
            municipio.codigo_unidade_federativa,
            codigo_modalidade_transporte,
            ROUND(SUM(indice_mun.indice) / COUNT(0), 2) AS indice
        FROM t_indice_municipio indice_mun
        INNER JOIN t_municipio municipio
            ON indice_mun.codigo_municipio = municipio.codigo
        WHERE municipio.codigo_unidade_federativa = %(codigo_unidade_federativa)s
        GROUP BY
            municipio.codigo_unidade_federativa,
            indice_mun.codigo_modalidade_transporte;
    '''