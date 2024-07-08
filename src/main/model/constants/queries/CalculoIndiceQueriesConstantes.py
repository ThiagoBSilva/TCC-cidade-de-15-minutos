class CalculoIndiceQueriesConstantes:

    CALCULAR_INDICE_15MIN_HEXAGONO = '''
        WITH contagem_categoria_15min AS (
            SELECT
                COUNT(0) AS contagem
            FROM t_categoria_amenidade
            WHERE codigo_categoria_pai IS NULL
        ),
        contagem_amenidade_15min_municipio AS (
            SELECT
                COUNT(DISTINCT codigo_feicao_osm) AS contagem
            FROM t_amenidade_municipio
            WHERE codigo_municipio = %(codigo_municipio)s
        ),
        informacoes_hexagono_municipio AS (
            SELECT 
                matriz.codigo_hexagono,
                matriz.codigo_modalidade_transporte,
                COUNT(DISTINCT categoria.codigo_categoria_pai) AS contagem_categoria_distinta,
                COUNT(DISTINCT feicao.codigo) AS contagem_feicao_distinta
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
                matriz.codigo_modalidade_transporte
        ),
        indice_p1 AS (
            SELECT 
                info_hex.codigo_hexagono,
                info_hex.codigo_modalidade_transporte,
                ROUND(info_hex.contagem_categoria_distinta::NUMERIC / cat_15min.contagem::NUMERIC * 100, 2) AS indice_p1
            FROM informacoes_hexagono_municipio info_hex, contagem_categoria_15min cat_15min
        ),
        indice_p2 AS (
            SELECT
                info_hex.codigo_hexagono,
                info_hex.codigo_modalidade_transporte,
                ROUND(info_hex.contagem_feicao_distinta::NUMERIC / amenidade_15min.contagem::NUMERIC * 100, 2) AS indice_p2
            FROM informacoes_hexagono_municipio info_hex, contagem_amenidade_15min_municipio amenidade_15min
        )
        INSERT INTO t_indice_hexagono (codigo_hexagono, codigo_modalidade_transporte, indice)
        SELECT 
            i_p1.codigo_hexagono,
            i_p2.codigo_modalidade_transporte,
            ROUND((i_p1.indice_p1 + i_p2.indice_p2) / 2, 2) AS indice
        FROM indice_p1 i_p1
        INNER JOIN indice_p2 i_p2
            ON i_p1.codigo_hexagono = i_p2.codigo_hexagono
            AND i_p1.codigo_modalidade_transporte = i_p2.codigo_modalidade_transporte;
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