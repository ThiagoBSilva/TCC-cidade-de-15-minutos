class CargaInicialQueriesConstantes:

    DROPAR_TABELAS_BANCO = '''
        DROP TABLE IF EXISTS t_indice_unidade_federativa;
        DROP TABLE IF EXISTS t_indice_municipio;
        DROP TABLE IF EXISTS t_indice_hexagono;
        DROP TABLE IF EXISTS t_matriz_tempo_viagem;
        DROP TABLE IF EXISTS t_amenidade_municipio;
        DROP TABLE IF EXISTS t_malha_hexagonal_municipio;
        DROP TABLE IF EXISTS t_municipio;
        DROP TABLE IF EXISTS t_unidade_federativa;
        DROP TABLE IF EXISTS t_modalidade_transporte;
        DROP TABLE IF EXISTS t_feicao_osm;
        DROP TABLE IF EXISTS t_categoria_amenidade;
        DROP TABLE IF EXISTS t_historico_erro;

        DROP TABLE IF EXISTS t_no_grafo_municipio;
    '''

    CRIAR_TABELAS_BANCO = '''
        CREATE TABLE t_historico_erro (
            codigo INT NOT NULL GENERATED ALWAYS AS IDENTITY,
            entidade_erro VARCHAR(30) NOT NULL,
            chave_entidade INT NOT NULL,
            etapa_erro SMALLINT NOT NULL,
            mensagem_erro TEXT NOT NULL,
            data_hora_ocorrencia TIMESTAMP NOT NULL
        );
        ALTER TABLE t_historico_erro
            ADD PRIMARY KEY (codigo);

        CREATE TABLE t_categoria_amenidade (
            codigo SMALLINT NOT NULL GENERATED BY DEFAULT AS IDENTITY,
            nome VARCHAR(50) NOT NULL,
            codigo_categoria_pai SMALLINT NULL
        );
        ALTER TABLE t_categoria_amenidade
            ADD PRIMARY KEY (codigo),
            ADD FOREIGN KEY (codigo_categoria_pai) REFERENCES t_categoria_amenidade (codigo);

        CREATE TABLE t_feicao_osm (
            codigo SMALLINT NOT NULL GENERATED ALWAYS AS IDENTITY,
            tag_osm VARCHAR(40) NOT NULL,
            descricao TEXT NOT NULL,
            flag_tag_ativa BOOLEAN NOT NULL DEFAULT TRUE,
            codigo_categoria_amenidade SMALLINT NOT NULL
        );
        ALTER TABLE t_feicao_osm
            ADD PRIMARY KEY (codigo),
            ADD FOREIGN KEY (codigo_categoria_amenidade) REFERENCES t_categoria_amenidade (codigo);

        CREATE TABLE t_modalidade_transporte (
            codigo SMALLINT NOT NULL GENERATED ALWAYS AS IDENTITY,
            nome VARCHAR(5) NOT NULL,
            descricao VARCHAR (15) NOT NULL,
            velocidade_media_kph NUMERIC(4, 2) NOT NULL
        );
        ALTER TABLE t_modalidade_transporte
            ADD PRIMARY KEY (codigo);

        CREATE TABLE t_unidade_federativa (
            codigo SMALLINT NOT NULL,
            nome VARCHAR(20) NOT NULL,
            sigla CHAR(2) NOT NULL,
            regiao VARCHAR(15) NOT NULL,
            area_km2 NUMERIC(12, 3) NOT NULL,
            geometria GEOMETRY(MULTIPOLYGON, 4326) NOT NULL,
            flag_calculo_indice_15min CHAR(1) NOT NULL DEFAULT 'P'
        );
        ALTER TABLE t_unidade_federativa
            ADD PRIMARY KEY (codigo),
            ADD CONSTRAINT CCKUFE001
                CHECK (flag_calculo_indice_15min IN ('P', 'C', 'E'));;

        CREATE TABLE t_municipio (
            codigo INT NOT NULL,
            nome VARCHAR(50) NOT NULL,
            area_km2 NUMERIC(12, 3) NOT NULL,
            geometria GEOMETRY(MULTIPOLYGON, 4326) NOT NULL,
            flag_geracao_malha_hexagonal CHAR(1) NOT NULL DEFAULT 'P',
            flag_extracao_amenidades CHAR(1) NOT NULL DEFAULT 'P',
            flag_calculo_matriz_tempo_viagem CHAR(1) NOT NULL DEFAULT 'P',
            flag_calculo_indice_15min CHAR(1) NOT NULL DEFAULT 'P',
            codigo_unidade_federativa INT NOT NULL
        );
        ALTER TABLE t_municipio
            ADD PRIMARY KEY (codigo),
            ADD FOREIGN KEY (codigo_unidade_federativa) REFERENCES t_unidade_federativa (codigo),
            ADD CONSTRAINT CCKMUN01
                CHECK (flag_geracao_malha_hexagonal IN ('P', 'C', 'E')),
            ADD CONSTRAINT CCKMUN02
                CHECK (flag_extracao_amenidades IN ('P', 'C', 'E')),
            ADD CONSTRAINT CCKMUN03
                CHECK (flag_calculo_matriz_tempo_viagem IN ('P', 'C', 'E')),
            ADD CONSTRAINT CCKMUN04
                CHECK (flag_calculo_indice_15min IN ('P', 'C', 'E'));

        CREATE TABLE t_malha_hexagonal_municipio (
            codigo INT NOT NULL GENERATED ALWAYS AS IDENTITY,
            hexagono_h3 VARCHAR(20) NOT NULL,
            geometria GEOMETRY(POLYGON, 4326) NOT NULL,
            codigo_municipio INT NOT NULL
        );
        ALTER TABLE t_malha_hexagonal_municipio
            ADD PRIMARY KEY (codigo),
            ADD FOREIGN KEY (codigo_municipio) REFERENCES t_municipio (codigo);
        
        CREATE TABLE t_amenidade_municipio (
            codigo INT NOT NULL GENERATED ALWAYS AS IDENTITY,
            geometria GEOMETRY(POINT, 4326) NOT NULL,
            codigo_feicao_osm SMALLINT NOT NULL,
            codigo_municipio INT NOT NULL
        );
        ALTER TABLE t_amenidade_municipio
            ADD PRIMARY KEY (codigo),
            ADD FOREIGN KEY (codigo_feicao_osm) REFERENCES t_feicao_osm (codigo),
            ADD FOREIGN KEY (codigo_municipio) REFERENCES t_municipio (codigo);

        CREATE TABLE t_matriz_tempo_viagem (
            codigo BIGINT NOT NULL GENERATED ALWAYS AS IDENTITY,
            codigo_hexagono INT NOT NULL,
            codigo_amenidade INT NOT NULL,
            codigo_modalidade_transporte SMALLINT NOT NULL,
            tempo_viagem_seg NUMERIC(8, 2) NULL
        );
        ALTER TABLE t_matriz_tempo_viagem
            ADD PRIMARY KEY (codigo),
            ADD FOREIGN KEY (codigo_hexagono) REFERENCES t_malha_hexagonal_municipio (codigo),
            ADD FOREIGN KEY (codigo_amenidade) REFERENCES t_amenidade_municipio (codigo),
            ADD FOREIGN KEY (codigo_modalidade_transporte) REFERENCES t_modalidade_transporte (codigo);

        CREATE TABLE t_indice_hexagono (
            codigo_hexagono INT NOT NULL,
            codigo_modalidade_transporte SMALLINT NOT NULL,
            indice_p1 NUMERIC(5, 2) NOT NULL,
            indice_p2 NUMERIC(5, 2) NOT NULL
        );
        ALTER TABLE t_indice_hexagono
            ADD PRIMARY KEY (codigo_hexagono, codigo_modalidade_transporte),
            ADD FOREIGN KEY (codigo_hexagono) REFERENCES t_malha_hexagonal_municipio (codigo),
            ADD FOREIGN KEY (codigo_modalidade_transporte) REFERENCES t_modalidade_transporte (codigo);

        CREATE TABLE t_indice_municipio (
            codigo_municipio INT NOT NULL,
            codigo_modalidade_transporte SMALLINT NOT NULL,
            indice_p1 NUMERIC(5, 2) NOT NULL,
            indice_p2 NUMERIC(5, 2) NOT NULL
        );
        ALTER TABLE t_indice_municipio
            ADD PRIMARY KEY (codigo_municipio, codigo_modalidade_transporte),
            ADD FOREIGN KEY (codigo_municipio) REFERENCES t_municipio (codigo),
            ADD FOREIGN KEY (codigo_modalidade_transporte) REFERENCES t_modalidade_transporte (codigo);

        CREATE TABLE t_indice_unidade_federativa (
            codigo_unidade_federativa SMALLINT NOT NULL,
            codigo_modalidade_transporte SMALLINT NOT NULL,
            indice_p1 NUMERIC(5, 2) NOT NULL,
            indice_p2 NUMERIC(5, 2) NOT NULL
        );
        ALTER TABLE t_indice_unidade_federativa
            ADD PRIMARY KEY (codigo_unidade_federativa, codigo_modalidade_transporte),
            ADD FOREIGN KEY (codigo_unidade_federativa) REFERENCES t_unidade_federativa (codigo),
            ADD FOREIGN KEY (codigo_modalidade_transporte) REFERENCES t_modalidade_transporte (codigo);

            

        CREATE TABLE t_no_grafo_municipio (
            codigo BIGINT NOT NULL,
            geometria GEOMETRY(POINT, 4326) NOT NULL
        );

        CREATE INDEX idx_t_no_grafo_municipio_codigo ON t_no_grafo_municipio(codigo);
        CREATE INDEX idx_t_no_grafo_municipio_geometria ON t_no_grafo_municipio USING GIST(geometria);
    '''

    POPULAR_TABELAS_INICIAIS = '''
        INSERT INTO t_modalidade_transporte (nome, descricao, velocidade_media_kph) VALUES
        ('walk', 'Caminhada', 3.6),
        ('bike', 'Bicicleta', 13.0);

        INSERT INTO t_categoria_amenidade (codigo, nome) VALUES
        (1, 'Alimentação'),
        (2, 'Compras e Serviços'),
        (3, 'Cultura, Esportes e Lazer'),
        (4, 'Educação'),
        (5, 'Saúde'),
        (6, 'Trabalho'),
        (7, 'Transporte');

        INSERT INTO t_categoria_amenidade (codigo, nome, codigo_categoria_pai) VALUES
        (8, 'Bar', 1),
        (9, 'Lanchonete', 1),
        (10, 'Local para compra de bebidas', 1),
        (11, 'Local para compra de alimentos prontos', 1),
        (12, 'Local para compra de ingredientes', 1),
        (13, 'Mercado geral de alimentos', 1),
        (14, 'Praça de alimentação', 1),
        (15, 'Restaurante', 1);

        INSERT INTO t_categoria_amenidade (codigo, nome, codigo_categoria_pai) VALUES
        (16, 'Agência de correios', 2),
        (17, 'Banco', 2),
        (18, 'Caixa eletrônico', 2),
        (19, 'Corpo de bombeiros', 2),
        (20, 'Estação de polícia', 2),
        (21, 'LAN house', 2),
        (22, 'Local de culto', 2),
        (23, 'Lotérica', 2),
        (24, 'Mercado geral', 2),
        (25, 'Serviço administrativo', 2);

        INSERT INTO t_categoria_amenidade (codigo, nome, codigo_categoria_pai) VALUES
        (26, 'Academia', 3),
        (27, 'Centro de artes', 3),
        (28, 'Centro de eventos', 3),
        (29, 'Centro esportivo', 3),
        (30, 'Centro social', 3),
        (31, 'Cinema', 3),
        (32, 'Espaço comum', 3),
        (33, 'Local natural', 3),
        (34, 'Local para natação', 3),
        (35, 'Museu', 3),
        (36, 'Parque', 3),
        (37, 'Playground', 3),
        (38, 'Teatro', 3);

        INSERT INTO t_categoria_amenidade (codigo, nome, codigo_categoria_pai) VALUES
        (39, 'Creche', 4),
        (40, 'Educação complementar', 4),
        (41, 'Escola', 4),
        (42, 'Local para estudo', 4),
        (43, 'Universidade', 4);

        INSERT INTO t_categoria_amenidade (codigo, nome, codigo_categoria_pai) VALUES
        (44, 'Casa de cuidados', 5),
        (45, 'Clínica', 5),
        (46, 'Farmácia', 5),
        (47, 'Hospital', 5),
        (48, 'Laboratório', 5),
        (49, 'Veterinário', 5);

        INSERT INTO t_categoria_amenidade (codigo, nome, codigo_categoria_pai) VALUES
        (50, 'Local para trabalho', 6);

        INSERT INTO t_categoria_amenidade (codigo, nome, codigo_categoria_pai) VALUES
        (51, 'Aluguel de bicicleta', 7),
        (52, 'Estacionamento para bicicleta', 7),
        (53, 'Estação de bonde', 7),
        (54, 'Estação de metrô', 7),
        (55, 'Manutenção de bicicleta', 7),
        (56, 'Parada de ônibus', 7),
        (57, 'Parada de taxi', 7);

        INSERT INTO t_feicao_osm (tag_osm, descricao, codigo_categoria_amenidade) VALUES
        ('amenity=bar', 'Bar', 8),
        ('amenity=biergarten', 'Jardim de cerveja', 8),
        ('amenity=pub', 'Pub', 8),
        ('amenity=cafe', 'Café', 9),
        ('amenity=fast_food', 'Restaurante fast-food', 9),
        ('shop=alcohol', 'Loja de bebidas alcoólicas', 10),
        ('shop=beverages', 'Loja de bebidas', 10),
        ('shop=bakery', 'Padaria', 11),
        ('shop=confectionery', 'Confeitaria', 11),
        ('shop=food', 'Loja de alimentos', 11),
        ('shop=ice_cream', 'Sorveteria', 11),
        ('shop=pastry', 'Pastelaria', 11),
        ('shop=butcher', 'Açougue', 12),
        ('shop=greengrocer', 'Hortifruti', 12),
        ('building=supermarket', 'Supermercado', 13),
        ('shop=convenience', 'Loja de conveniência', 13),
        ('amenity=food_court', 'Praça de alimentação', 14),
        ('amenity=restaurant', 'Restaurante', 15);

        INSERT INTO t_feicao_osm (tag_osm, descricao, codigo_categoria_amenidade) VALUES
        ('amenity=post_office', 'Agência de correios', 16),
        ('office=courier', 'Agência de entregas', 16),
        ('amenity=bank', 'Banco', 17),
        ('amenity=atm', 'Caixa eletrônico', 18),
        ('amenity=payment_terminal', 'Terminal de pagamento', 18),
        ('amenity=fire_station', 'Corpo de bombeiros', 19),
        ('building=fire_station', 'Edifício dos bombeiros', 19),
        ('amenity=police', 'Estação de polícia', 20),
        ('amenity=place_of_worship', 'Lugar de culto', 21),
        ('building=church', 'Igreja', 21),
        ('amenity=internet_cafe', 'LAN house', 22),
        ('amenity=payment_centre', 'Lotérica', 23),
        ('amenity=marketplace', 'Mercado', 24),
        ('building=supermarket', 'Supermercado', 24),
        ('building=retail', 'Varejo', 24),
        ('shop=department_store', 'Loja de departamento', 24),
        ('shop=general', 'Loja geral', 24),
        ('shop=mall', 'Shopping', 24),
        ('shop=supermarket', 'Supermercado', 24),
        ('shop=wholesale', 'Atacadista', 24),
        ('shop=variety_store', 'Loja de variedades', 24),
        ('amenity=courthouse', 'Tribunal', 25),
        ('amenity=townhall', 'Prefeitura', 25),
        ('building=government', 'Edifício governamental', 25),
        ('office=government', 'Escritório governamental', 25);

        INSERT INTO t_feicao_osm (tag_osm, descricao, codigo_categoria_amenidade) VALUES
        ('leisure=fitness_centre', 'Centro de atividades fitness', 26),
        ('leisure=fitness_station', 'Estação de atividades fitness', 26),
        ('sport=fitness', 'Atividades fitness', 26),
        ('amenity=arts_centre', 'Centro de artes', 27),
        ('tourism=gallery', 'Galeria', 27),
        ('building=sports_centre', 'Centro esportivo', 28),
        ('leisure=sports_centre', 'Centro esportivo', 28),
        ('sport=multi', 'Esportes múltiplos', 28),
        ('amenity=community_centre', 'Centro comunitário', 29),
        ('amenity=conference_centre', 'Centro de conferências', 29),
        ('amenity=events_venue', 'Local de eventos', 29),
        ('amenity=exhibition_centre', 'Centro de exposições', 29),
        ('amenity=music_venue', 'Local de música', 29),
        ('amenity=social_centre', 'Centro social', 30),
        ('amenity=cinema', 'Cinema', 31),
        ('leasure=common', 'Espaço comum', 32),
        ('leisure=swimming_area', 'Área de natação', 33),
        ('leisure=swimming_pool', 'Piscina', 33),
        ('leisure=water_park', 'Parque aquático', 33),
        ('building=museum', 'Museu', 34),
        ('tourism=museum', 'Museu', 34),
        ('leisure=garden', 'Jardim', 35),
        ('leisure=nature_reserve', 'Reserva natural', 35),
        ('leisure=park', 'Parque', 36),
        ('leisure=playground', 'Playground', 37),
        ('amenity=theatre', 'Teatro', 38);

        INSERT INTO t_feicao_osm (tag_osm, descricao, codigo_categoria_amenidade) VALUES
        ('amenity=kindergarten', 'Creche', 39),
        ('building=kindergarten', 'Edifício da creche', 39),
        ('amenity=language_school', 'Escola de idiomas', 40),
        ('amenity=driving_school', 'Autoescola', 40),
        ('amenity=school', 'Escola', 41),
        ('building=school', 'Edifício escolar', 41),
        ('amenity=library', 'Biblioteca', 42),
        ('amenity=college', 'Faculdade', 43),
        ('amenity=university', 'Universidade', 43),
        ('building=college', 'Edifício de faculdade', 43),
        ('building=university', 'Edifício de universidade', 43);

        INSERT INTO t_feicao_osm (tag_osm, descricao, codigo_categoria_amenidade) VALUES
        ('amenity=nursing_home', 'Casa de repouso', 44),
        ('amenity=social_facility', 'Instalação social', 44),
        ('amenity=doctors', 'Consultório médico', 45),
        ('amenity=clinic', 'Clínica', 45),
        ('amenity=pharmacy', 'Farmácia', 46),
        ('shop=medical_supply', 'Loja de suprimentos médicos', 46),
        ('amenity=hospital', 'Hospital', 47),
        ('building=hospital', 'Edifício hospitalar', 47),
        ('healthcare=laboratory', 'Laboratório', 48),
        ('amenity=veterinary', 'Veterinário', 49);

        INSERT INTO t_feicao_osm (tag_osm, descricao, codigo_categoria_amenidade) VALUES
        ('building=commercial', 'Edifício comercial', 50),
        ('building=industrial', 'Edifício industrial', 50),
        ('building=office', 'Edifício de escritórios', 50),
        ('building=retail', 'Edifício de varejo', 50),
        ('office=*', 'Escritório', 50);

        INSERT INTO t_feicao_osm (tag_osm, descricao, codigo_categoria_amenidade) VALUES
        ('amenity=bicycle_rental', 'Aluguel de bicicleta', 51),
        ('amenity=bicycle_parking', 'Estacionamento para bicicleta', 52),
        ('railway=tram_stop', 'Estação de bonde', 53),
        ('railway=platform', 'Plataforma ferroviária', 54),
        ('railway=subway_entrance', 'Entrada de metrô', 54),
        ('amenity=bicycle_repair_station', 'Estação de reparo de bicicletas', 55),
        ('amenity=bicycle_wash', 'Lavagem de bicicletas', 55),
        ('amenity=bus_station', 'Estação de ônibus', 56),
        ('highway=bus_stop', 'Parada de ônibus', 56),
        ('highway=platform', 'Plataforma de ônibus', 56),
        ('amenity=taxi', 'Parada de táxi', 57);
    '''