# DDL

CREATE_TABELA_UF = '''
    DROP TABLE IF EXISTS t_unidade_federativa CASCADE;
    CREATE TABLE t_unidade_federativa (
        codigo INT NOT NULL,
        nome VARCHAR(20) NOT NULL
    );
    ALTER TABLE t_unidade_federativa
        ADD PRIMARY KEY (codigo);
'''

CREATE_TABELA_MUNICIPIO = '''
    DROP TABLE IF EXISTS t_municipio CASCADE;
    CREATE TABLE t_municipio (
        codigo INT NOT NULL,
        nome VARCHAR(50) NOT NULL,
        flag_analisado BOOLEAN NULL DEFAULT FALSE,
        codigo_uf INT NOT NULL
    );
    ALTER TABLE t_municipio
        ADD PRIMARY KEY (codigo),
        ADD FOREIGN KEY (codigo_uf) REFERENCES t_unidade_federativa (codigo);
'''

CREATE_TABELA_MODALIDADE_TRANSPORTE = '''
    DROP TABLE IF EXISTS t_modalidade_transporte CASCADE;
    CREATE TABLE t_modalidade_transporte (
        codigo INT NOT NULL GENERATED ALWAYS AS IDENTITY,
        nome VARCHAR(5) NOT NULL,
        velocidade_media_kph NUMERIC NOT NULL
    );
    ALTER TABLE t_modalidade_transporte
        ADD PRIMARY KEY (codigo);
'''

CREATE_TABELA_GEOMETRIA_MUNICIPIO = '''   
    DROP TABLE IF EXISTS t_geometria_municipio;
    CREATE TABLE t_geometria_municipio (
        codigo INT NOT NULL GENERATED ALWAYS AS IDENTITY,
        geometria GEOMETRY(MULTIPOLYGON, 4326) NOT NULL,
        codigo_municipio INT NOT NULL
    );
    ALTER TABLE t_geometria_municipio
        ADD PRIMARY KEY (codigo),
        ADD FOREIGN KEY (codigo_municipio) REFERENCES t_municipio (codigo);
'''

CREATE_TABELA_PONTO_INTERESSE = '''
    DROP TABLE IF EXISTS t_ponto_interesse CASCADE;
    CREATE TABLE t_ponto_interesse (
        codigo BIGINT NOT NULL GENERATED ALWAYS AS IDENTITY,
        tipo VARCHAR(30) NOT NULL,
        geometria GEOMETRY(POINT, 4326) NOT NULL,
        codigo_municipio INT NOT NULL
    );
    ALTER TABLE t_ponto_interesse
        ADD PRIMARY KEY (codigo),
        ADD FOREIGN KEY (codigo_municipio) REFERENCES t_municipio (codigo);
'''

CREATE_TABELA_MALHA_HEXAGONAL = '''
    DROP TABLE IF EXISTS t_malha_hexagonal CASCADE;
    CREATE TABLE t_malha_hexagonal (
        codigo VARCHAR(20) NOT NULL,
        geometria GEOMETRY(POLYGON, 4326) NOT NULL,
        codigo_municipio INT NOT NULL
    );
    ALTER TABLE t_malha_hexagonal
        ADD PRIMARY KEY (codigo),
        ADD FOREIGN KEY (codigo_municipio) REFERENCES t_municipio (codigo);
'''

CREATE_TABELA_AREA_ANALISE = '''
    DROP TABLE IF EXISTS t_area_analise;
    CREATE TABLE t_area_analise (
        codigo BIGINT NOT NULL GENERATED ALWAYS AS IDENTITY,
        geometria GEOMETRY(POLYGON, 4326) NOT NULL,
        codigo_hexagono VARCHAR(20) NOT NULL,
        codigo_municipio INT NOT NULL,
        codigo_modalidade_transporte INT NOT NULL
    );
    ALTER TABLE t_area_analise
        ADD PRIMARY KEY (codigo),
        ADD FOREIGN KEY (codigo_hexagono) REFERENCES t_malha_hexagonal (codigo),
        ADD FOREIGN KEY (codigo_municipio) REFERENCES t_municipio (codigo),
        ADD FOREIGN KEY (codigo_modalidade_transporte) REFERENCES t_modalidade_transporte (codigo);
'''

CREATE_TABELA_GRAFO_NOS = '''
    DROP TABLE IF EXISTS t_grafo_no CASCADE;
    CREATE TABLE t_grafo_no (
        codigo_osm BIGINT NOT NULL,
        geometria GEOMETRY(POINT, 4326) NOT NULL,
        codigo_municipio INT NOT NULL,
        codigo_modalidade_transporte INT NOT NULL
    );
    ALTER TABLE t_grafo_no
        ADD PRIMARY KEY (codigo_osm, codigo_modalidade_transporte),
        ADD FOREIGN KEY (codigo_municipio) REFERENCES t_municipio (codigo),
        ADD FOREIGN KEY (codigo_modalidade_transporte) REFERENCES t_modalidade_transporte (codigo);
'''

CREATE_TABELA_GRAFO_ARESTAS = '''
    DROP TABLE IF EXISTS t_grafo_aresta;
    CREATE TABLE t_grafo_aresta (
        no_u BIGINT NOT NULL,
        no_v BIGINT NOT NULL,
        chave INT NOT NULL,
        mao_unica BOOLEAN NOT NULL,
        comprimento_m NUMERIC NOT NULL,
        velocidade_kph NUMERIC NOT NULL,
        tempo_viagem_seg NUMERIC NOT NULL,
        geometria GEOMETRY(LINESTRING, 4326) NOT NULL,
        codigo_municipio INT NOT NULL,
        codigo_modalidade_transporte INT NOT NULL
    );
    ALTER TABLE t_grafo_aresta
        ADD PRIMARY KEY (no_u, no_v, chave, codigo_modalidade_transporte),
        ADD FOREIGN KEY (no_u, codigo_modalidade_transporte) REFERENCES t_grafo_no (codigo_osm, codigo_modalidade_transporte),
        ADD FOREIGN KEY (no_v, codigo_modalidade_transporte) REFERENCES t_grafo_no (codigo_osm, codigo_modalidade_transporte),
        ADD FOREIGN KEY (codigo_municipio) REFERENCES t_municipio (codigo),
        ADD FOREIGN KEY (codigo_modalidade_transporte) REFERENCES t_modalidade_transporte (codigo);
'''

CREATE_TABELA_MATRIZ_TEMPO_VIAGEM = '''
    DROP TABLE IF EXISTS t_matriz_tempo_viagem;
    CREATE TABLE t_matriz_tempo_viagem (
        codigo BIGINT NOT NULL GENERATED ALWAYS AS IDENTITY,
        codigo_origem VARCHAR(20) NOT NULL,
        no_origem BIGINT NOT NULL,
        origem GEOMETRY(POINT, 4326) NOT NULL,
        codigo_destino BIGINT NOT NULL,
        no_destino BIGINT NOT NULL,
        destino GEOMETRY(POINT, 4326) NOT NULL,
        tempo_viagem_seg NUMERIC NOT NULL,
        distancia_m NUMERIC NOT NULL,
        rota TEXT NOT NULL,
        codigo_municipio INT NOT NULL,
        codigo_modalidade_transporte INT NOT NULL
    );
    ALTER TABLE t_matriz_tempo_viagem
        ADD PRIMARY KEY (codigo),
        ADD FOREIGN KEY (codigo_origem) REFERENCES t_malha_hexagonal (codigo),
        ADD FOREIGN KEY (no_origem, codigo_modalidade_transporte) REFERENCES t_grafo_no (codigo_osm, codigo_modalidade_transporte),
        ADD FOREIGN KEY (codigo_destino) REFERENCES t_ponto_interesse (codigo),
        ADD FOREIGN KEY (no_destino, codigo_modalidade_transporte) REFERENCES t_grafo_no (codigo_osm, codigo_modalidade_transporte),
        ADD FOREIGN KEY (codigo_municipio) REFERENCES t_municipio (codigo),
        ADD FOREIGN KEY (codigo_modalidade_transporte) REFERENCES t_modalidade_transporte (codigo);
'''

# DML

SELECT_MUNICIPIOS = '''
    SELECT 
        m.codigo,
        m.nome,
        uf.nome AS "nome_uf"
    FROM t_municipio m
    INNER JOIN t_unidade_federativa uf
        ON m.codigo_uf = uf.codigo
    ORDER BY m.codigo;
'''

SELECT_GEOMETRIA_MUNICIPIOS = '''
    SELECT 
        codigo,
        geometria,
        codigo_municipio
    FROM t_geometria_municipio
    WHERE codigo_municipio IN (
        SELECT DISTINCT
            codigo_municipio
        FROM t_ponto_interesse
    )
    ORDER BY codigo_municipio;
'''

SELECT_MUNICIPIOS_COM_MALHA = '''
    SELECT 
        m.codigo,
        m.nome,
        uf.nome AS "nome_uf"
    FROM t_municipio m
    INNER JOIN t_unidade_federativa uf
        ON m.codigo_uf = uf.codigo
    WHERE m.codigo IN (
        SELECT DISTINCT
            codigo_municipio
        FROM t_malha_hexagonal
    )
    ORDER BY codigo;
'''

SELECT_MODALIDADES_TRANSPORTE = '''
    SELECT 
        codigo,
        nome,
        velocidade_media_kph
    FROM t_modalidade_transporte
    ORDER BY codigo;
'''

SELECT_MALHA_MUNICIPIO = '''
    SELECT 
        codigo,
        geometria,
        codigo_municipio
    FROM t_malha_hexagonal
    WHERE codigo_municipio = :codigo_municipio;
'''

SELECT_PONTOS_INTERESSE_MUNICIPIO = '''
    SELECT
        codigo,
        tipo,
        geometria,
        codigo_municipio
    FROM t_ponto_interesse
    WHERE codigo_municipio = :codigo_municipio
    ORDER BY codigo;
'''

SELECT_AREAS_ANALISE_MUNICIPIO = '''
    SELECT 
        codigo,
        geometria,
        codigo_hexagono,
        codigo_municipio,
        codigo_modalidade_transporte
    FROM t_area_analise
    WHERE codigo_municipio = :codigo_municipio
    AND codigo_modalidade_transporte = :codigo_modalidade_transporte
    ORDER BY codigo;
'''

SELECT_GRAFO_NOS = '''
    SELECT 
        codigo_osm AS osmid,
        geometria AS geometry,
        st_x(geometria) AS x,
        st_y(geometria) AS y
    FROM t_grafo_no
    WHERE codigo_municipio = :codigo_municipio
    AND codigo_modalidade_transporte = :codigo_modalidade_transporte;
'''

SELECT_GRAFO_ARESTAS = '''
    SELECT 
        no_u AS u,
        no_v AS v,
        chave AS key,
        mao_unica AS oneway,
        comprimento_m AS length,
        velocidade_kph AS speed_kph,
        tempo_viagem_seg AS travel_time,
        geometria AS geometry
    FROM t_grafo_aresta
    WHERE codigo_municipio = :codigo_municipio
    AND codigo_modalidade_transporte = :codigo_modalidade_transporte;
'''

SELECT_MUNICIPIOS_APTOS_ANALISE = '''
    SELECT 
        codigo,
        nome
    FROM t_municipio
    WHERE codigo IN (
        SELECT codigo_municipio FROM t_area_analise
    )
    AND codigo IN (
        SELECT codigo_municipio FROM t_grafo_no
    )
    AND codigo IN (
        SELECT codigo_municipio FROM t_grafo_aresta
    )
    AND flag_analisado = FALSE;
'''

SELECT_HEXAGONOS_COM_AREA_ANALISE = '''
    SELECT 
        mh.codigo,
        mh.geometria AS "geometria_hexagono",
        aa.geometria AS "geometria_area_analise"
    FROM t_malha_hexagonal mh
    INNER JOIN t_area_analise aa
        ON mh.codigo = aa.codigo_hexagono
    WHERE mh.codigo_municipio = :codigo_municipio
    AND aa.codigo_modalidade_transporte = :codigo_modalidade_transporte
'''