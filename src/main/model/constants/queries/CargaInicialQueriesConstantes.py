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
            codigo SMALLINT NOT NULL GENERATED ALWAYS AS IDENTITY,
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
            flag_tag_ativa BOOLEAN NOT NULL DEFAULT FALSE,
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
            geometria GEOMETRY(MULTIPOLYGON, 4326) NOT NULL
        );
        ALTER TABLE t_unidade_federativa
            ADD PRIMARY KEY (codigo);

        CREATE TABLE t_municipio (
            codigo INT NOT NULL,
            nome VARCHAR(50) NOT NULL,
            area_km2 NUMERIC(12, 3) NOT NULL,
            geometria GEOMETRY(MULTIPOLYGON, 4326) NOT NULL,
            flag_geracao_malha_hexagonal CHAR(1) NOT NULL DEFAULT 'P',
            flag_extracao_amenidades CHAR(1) NOT NULL DEFAULT 'P',
            flag_calculo_matriz_tempo_viagem CHAR(1) NOT NULL DEFAULT 'P',
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
                CHECK (flag_calculo_matriz_tempo_viagem IN ('P', 'C', 'E'));

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
            tempo_viagem_seg NUMERIC(10, 2) NOT NULL
        );
        ALTER TABLE t_matriz_tempo_viagem
            ADD PRIMARY KEY (codigo),
            ADD FOREIGN KEY (codigo_hexagono) REFERENCES t_malha_hexagonal_municipio (codigo),
            ADD FOREIGN KEY (codigo_amenidade) REFERENCES t_amenidade_municipio (codigo),
            ADD FOREIGN KEY (codigo_modalidade_transporte) REFERENCES t_modalidade_transporte (codigo);

        CREATE TABLE t_indice_hexagono (
            codigo_hexagono INT NOT NULL,
            codigo_modalidade_transporte SMALLINT NOT NULL,
            indice NUMERIC(4, 2) NOT NULL
        );
        ALTER TABLE t_indice_hexagono
            ADD PRIMARY KEY (codigo_hexagono, codigo_modalidade_transporte),
            ADD FOREIGN KEY (codigo_hexagono) REFERENCES t_malha_hexagonal_municipio (codigo),
            ADD FOREIGN KEY (codigo_modalidade_transporte) REFERENCES t_modalidade_transporte (codigo);

        CREATE TABLE t_indice_municipio (
            codigo_municipio INT NOT NULL,
            codigo_modalidade_transporte SMALLINT NOT NULL,
            indice NUMERIC(4, 2) NOT NULL
        );
        ALTER TABLE t_indice_municipio
            ADD PRIMARY KEY (codigo_municipio, codigo_modalidade_transporte),
            ADD FOREIGN KEY (codigo_municipio) REFERENCES t_municipio (codigo),
            ADD FOREIGN KEY (codigo_modalidade_transporte) REFERENCES t_modalidade_transporte (codigo);

        CREATE TABLE t_indice_unidade_federativa (
            codigo_unidade_federativa SMALLINT NOT NULL,
            codigo_modalidade_transporte SMALLINT NOT NULL,
            indice NUMERIC(4, 2) NOT NULL
        );
        ALTER TABLE t_indice_unidade_federativa
            ADD PRIMARY KEY (codigo_unidade_federativa, codigo_modalidade_transporte),
            ADD FOREIGN KEY (codigo_unidade_federativa) REFERENCES t_unidade_federativa (codigo),
            ADD FOREIGN KEY (codigo_modalidade_transporte) REFERENCES t_modalidade_transporte (codigo);
    '''

    POPULAR_TABELAS_INICIAIS = '''
        INSERT INTO t_categoria_amenidade (nome) VALUES
        ('Alimentação'),
        ('Compras e Serviços'),
        ('Cultura, Esportes e Lazer'),
        ('Educação'),
        ('Saúde'),
        ('Trabalho'),
        ('Transporte');
        
        DROP TABLE IF EXISTS temp_subcategoria_amenidade;
        CREATE TEMP TABLE temp_subcategoria_amenidade (
            codigo SMALLINT NOT NULL GENERATED ALWAYS AS IDENTITY,
            nome_categoria_pai VARCHAR(50),
            nome_subcategoria VARCHAR(50)
        );

        INSERT INTO temp_subcategoria_amenidade (nome_categoria_pai, nome_subcategoria) VALUES
        ('Alimentação', 'Estabelecimentos de consumo de alimentos e bebidas'),
        ('Alimentação', 'Lojas de alimentos e bebidas'),
        ('Compras e Serviços', 'Serviços públicos'),
        ('Compras e Serviços', 'Serviços financeiros e administrativos'),
        ('Compras e Serviços', 'Compras e serviços gerais'),
        ('Cultura, Esportes e Lazer', 'Centros culturais e locais de eventos'),
        ('Cultura, Esportes e Lazer', 'Instalações de lazer e esportes'),
        ('Cultura, Esportes e Lazer', 'Atrações turísticas'),
        ('Educação', 'Instituições de ensino'),
        ('Saúde', 'Serviços de saúde e assistência social'),
        ('Saúde', 'Lojas de suprimentos médicos'),
        ('Saúde', 'Outros serviços de saúde'),
        ('Trabalho', 'Tipos de edifícios e áreas para trabalho'),
        ('Trabalho', 'Uso do solo com potencial de empregabilidade'),
        ('Trabalho', 'Locais de trabalho'),
        ('Transporte', 'Infraestrutura para bicicletas'),
        ('Transporte', 'Transporte público'),
        ('Transporte', 'Infraestrutura ferroviária'),
        ('Transporte', 'Infraestrutura para pedestres e ciclistas');

        INSERT INTO t_categoria_amenidade (nome, codigo_categoria_pai)
        SELECT 
            tmp.nome_subcategoria,
            categoria.codigo
        FROM temp_subcategoria_amenidade tmp
        INNER JOIN t_categoria_amenidade categoria
            ON tmp.nome_categoria_pai = categoria.nome
        ORDER BY tmp.codigo;

        DROP TABLE temp_subcategoria_amenidade;

        DROP TABLE IF EXISTS temp_feicao_osm;
        CREATE TEMP TABLE temp_feicao_osm (
            codigo SMALLINT NOT NULL GENERATED ALWAYS AS IDENTITY,
            tag_osm VARCHAR(40),
            descricao TEXT,
            nome_categoria_amenidade VARCHAR(50)
        );

        INSERT INTO temp_feicao_osm (tag_osm, descricao, nome_categoria_amenidade) VALUES
        ('amenity=bar', 'Bar', 'Estabelecimentos de consumo de alimentos e bebidas'),
        ('amenity=biergarten', 'Jardim de cerveja', 'Estabelecimentos de consumo de alimentos e bebidas'),
        ('amenity=cafe', 'Café ou lanchonete', 'Estabelecimentos de consumo de alimentos e bebidas'),
        ('amenity=fast_food', 'Restaurante de fast food', 'Estabelecimentos de consumo de alimentos e bebidas'),
        ('amenity=food_court', 'Praça de alimentação', 'Estabelecimentos de consumo de alimentos e bebidas'),
        ('amenity=pub', 'Bar (Pub)', 'Estabelecimentos de consumo de alimentos e bebidas'),
        ('amenity=restaurant', 'Restaurante', 'Estabelecimentos de consumo de alimentos e bebidas'),
        ('shop=alcohol', 'Loja de bebidas alcoólicas', 'Lojas de alimentos e bebidas'),
        ('shop=bakery', 'Padaria', 'Lojas de alimentos e bebidas'),
        ('shop=beverages', 'Loja de bebidas não alcoólicas', 'Lojas de alimentos e bebidas'),
        ('shop=butcher', 'Açougue', 'Lojas de alimentos e bebidas'),
        ('shop=convenience', 'Loja de conveniência', 'Lojas de alimentos e bebidas'),
        ('shop=confectionery', 'Loja de doces', 'Lojas de alimentos e bebidas'),
        ('shop=farm', 'Loja de produtos agrícolas', 'Lojas de alimentos e bebidas'),
        ('shop=food', 'Loja de alimentos', 'Lojas de alimentos e bebidas'),
        ('shop=greengrocer', 'Hortifruti', 'Lojas de alimentos e bebidas'),
        ('shop=supermarket', 'Supermercado', 'Lojas de alimentos e bebidas'),
        ('shop=deli', 'Delicatessen', 'Lojas de alimentos e bebidas'),
        ('shop=cheese', 'Loja de queijos', 'Lojas de alimentos e bebidas'),
        ('amenity=atm', 'Caixa eletrônico', 'Serviços financeiros e administrativos'),
        ('amenity=bank', 'Banco', 'Serviços financeiros e administrativos'),
        ('amenity=money_transfer', 'Serviço de transferência de dinheiro', 'Serviços financeiros e administrativos'),
        ('amenity=courthouse', 'Tribunal', 'Serviços financeiros e administrativos'),
        ('amenity=fire_station', 'Estação de bombeiros', 'Serviços públicos'),
        ('amenity=police', 'Delegacia de polícia', 'Serviços públicos'),
        ('amenity=post_box', 'Caixa de correio', 'Serviços financeiros e administrativos'),
        ('amenity=post_depot', 'Depósito de correios', 'Serviços financeiros e administrativos'),
        ('amenity=post_office', 'Agência dos correios', 'Serviços públicos'),
        ('amenity=townhall', 'Prefeitura', 'Serviços financeiros e administrativos'),
        ('amenity=internet_cafe', 'Café com acesso à internet', 'Compras e serviços gerais'),
        ('amenity=marketplace', 'Mercado público', 'Compras e serviços gerais'),
        ('shop=department_store', 'Loja de departamentos', 'Compras e serviços gerais'),
        ('shop=general', 'Loja geral', 'Compras e serviços gerais'),
        ('shop=mall', 'Shopping center', 'Compras e serviços gerais'),
        ('shop=wholesale', 'Atacado', 'Compras e serviços gerais'),
        ('shop=clothes', 'Loja de roupas', 'Compras e serviços gerais'),
        ('shop=variety_store', 'Loja de variedades', 'Compras e serviços gerais'),
        ('shop=appliance', 'Loja de eletrodomésticos', 'Compras e serviços gerais'),
        ('shop=electrical', 'Loja de produtos elétricos', 'Compras e serviços gerais'),
        ('shop=hardware', 'Loja de ferragens', 'Compras e serviços gerais'),
        ('shop=furniture', 'Loja de móveis', 'Compras e serviços gerais'),
        ('shop=electronics', 'Loja de eletrônicos', 'Compras e serviços gerais'),
        ('shop=telecommunication', 'Loja de telecomunicações', 'Compras e serviços gerais'),
        ('amenity=car_wash', 'Lavagem de carros', 'Compras e serviços gerais'),
        ('amenity=laundry', 'Lavanderia', 'Compras e serviços gerais'),
        ('amenity=dry_cleaning', 'Serviço de limpeza a seco', 'Compras e serviços gerais'),
        ('amenity=arts_centre', 'Centro de artes', 'Centros culturais e locais de eventos'),
        ('amenity=cinema', 'Cinema', 'Centros culturais e locais de eventos'),
        ('amenity=community_centre', 'Centro comunitário', 'Centros culturais e locais de eventos'),
        ('amenity=conference_centre', 'Centro de conferências', 'Centros culturais e locais de eventos'),
        ('amenity=events_venue', 'Local de eventos', 'Centros culturais e locais de eventos'),
        ('amenity=exhibition_centre', 'Centro de exposições', 'Centros culturais e locais de eventos'),
        ('amenity=music_venue', 'Casa de shows', 'Centros culturais e locais de eventos'),
        ('amenity=public_bookcase', 'Estante pública de livros', 'Centros culturais e locais de eventos'),
        ('amenity=social_centre', 'Centro social', 'Centros culturais e locais de eventos'),
        ('amenity=stage', 'Palco', 'Centros culturais e locais de eventos'),
        ('amenity=theatre', 'Teatro', 'Centros culturais e locais de eventos'),
        ('amenity=place_of_worship', 'Local de culto', 'Centros culturais e locais de eventos'),
        ('leisure=dance', 'Local de dança', 'Instalações de lazer e esportes'),
        ('leisure=fitness_centre', 'Centro de fitness (Academia)', 'Instalações de lazer e esportes'),
        ('leisure=fitness_station', 'Estação de fitness', 'Instalações de lazer e esportes'),
        ('leisure=garden', 'Jardim', 'Instalações de lazer e esportes'),
        ('leisure=nature_reserve', 'Reserva natural', 'Instalações de lazer e esportes'),
        ('leisure=playground', 'Parque infantil', 'Instalações de lazer e esportes'),
        ('leisure=sports_centre', 'Centro esportivo', 'Instalações de lazer e esportes'),
        ('leisure=stadium', 'Estádio', 'Instalações de lazer e esportes'),
        ('leisure=swimming_area', 'Área para natação', 'Instalações de lazer e esportes'),
        ('leisure=swimming_pool', 'Piscina', 'Instalações de lazer e esportes'),
        ('leisure=track', 'Pista', 'Instalações de lazer e esportes'),
        ('leisure=water_park', 'Parque aquático', 'Instalações de lazer e esportes'),
        ('sports=dance', 'Esporte: dança', 'Instalações de lazer e esportes'),
        ('sports=fitness', 'Esporte: fitness', 'Instalações de lazer e esportes'),
        --('sports=multi', 'Esporte: multiuso', 'Instalações de lazer e esportes'),
        ('leisure=park', 'Parque', 'Instalações de lazer e esportes'),
        ('leisure=pitch', 'Campo de esportes', 'Instalações de lazer e esportes'),
        ('tourism=gallery', 'Galeria de arte', 'Atrações turísticas'),
        ('tourism=museum', 'Museu', 'Atrações turísticas'),
        ('tourism=theme_park', 'Parque temático', 'Atrações turísticas'),
        ('amenity=college', 'Faculdade', 'Instituições de ensino'),
        ('amenity=kindergarten', 'Jardim de infância', 'Instituições de ensino'),
        ('amenity=library', 'Biblioteca', 'Instituições de ensino'),
        ('amenity=toy_library', 'Biblioteca de brinquedos', 'Instituições de ensino'),
        ('amenity=school', 'Escola', 'Instituições de ensino'),
        ('amenity=university', 'Universidade', 'Instituições de ensino'),
        ('amenity=clinic', 'Clínica', 'Serviços de saúde e assistência social'),
        ('amenity=dentist', 'Consultório dentário', 'Serviços de saúde e assistência social'),
        ('amenity=doctors', 'Consultório médico', 'Serviços de saúde e assistência social'),
        ('amenity=hospital', 'Hospital', 'Serviços de saúde e assistência social'),
        ('amenity=nursing_home', 'Casa de repouso', 'Serviços de saúde e assistência social'),
        ('amenity=pharmacy', 'Farmácia', 'Serviços de saúde e assistência social'),
        ('amenity=social_facility', 'Instalação social', 'Serviços de saúde e assistência social'),
        ('shop=medical_supply', 'Loja de suprimentos médicos', 'Lojas de suprimentos médicos'),
        ('amenity=optician', 'Oculista', 'Outros serviços de saúde'),
        ('amenity=veterinary', 'Consultório veterinário', 'Outros serviços de saúde'),
        ('building=commercial', 'Edifício comercial', 'Tipos de edifícios e áreas para trabalho'),
        ('building=industrial', 'Edifício industrial', 'Tipos de edifícios e áreas para trabalho'),
        ('building=office', 'Edifício de escritórios', 'Tipos de edifícios e áreas para trabalho'),
        ('building=retail', 'Edifício de varejo', 'Tipos de edifícios e áreas para trabalho'),
        ('landuse=commercial', 'Uso do solo: comercial', 'Uso do solo'),
        ('landuse=industrial', 'Uso do solo: industrial', 'Uso do solo'),
        ('landuse=retail', 'Uso do solo: varejo', 'Uso do solo'),
        ('office=True', 'Escritório', 'Locais de trabalho'),
        ('amenity=co_working', 'Espaço de co-working', 'Locais de trabalho'),
        ('amenity=bicycle_parking', 'Estacionamento para bicicletas', 'Infraestrutura para bicicletas'),
        ('amenity=bicycle_repair_station', 'Estação de reparo de bicicletas', 'Infraestrutura para bicicletas'),
        ('amenity=bicycle_rental', 'Locação de bicicletas', 'Infraestrutura para bicicletas'),
        ('amenity=bicycle_wash', 'Lavagem de bicicletas', 'Infraestrutura para bicicletas'),
        ('amenity=bus_station', 'Estação de ônibus', 'Transporte público'),
        ('highway=bus_stop', 'Ponto de ônibus', 'Transporte público'),
        ('highway=platform', 'Plataforma', 'Transporte público'),
        ('public_transport=stop_position', 'Posição de parada', 'Transporte público'),
        ('public_transport=platform', 'Plataforma de transporte público', 'Transporte público'),
        ('public_transport=station', 'Estação de transporte público', 'Transporte público'),
        ('public_transport=stop_area', 'Área de parada de transporte público', 'Transporte público'),
        ('public_transport=stop_area_group', 'Grupo de áreas de parada de transporte público', 'Transporte público'),
        ('railway=subway', 'Metrô', 'Infraestrutura ferroviária'),
        ('railway=tram', 'Bonde', 'Infraestrutura ferroviária'),
        ('railway=platform', 'Plataforma ferroviária', 'Infraestrutura ferroviária'),
        ('railway=station', 'Estação ferroviária', 'Infraestrutura ferroviária'),
        ('railway=subway_entrance', 'Entrada do metrô', 'Infraestrutura ferroviária'),
        ('railway=tram_stop', 'Parada de bonde', 'Infraestrutura ferroviária'),
        ('highway=cycleway', 'Ciclovia', 'Infraestrutura para pedestres e ciclistas'),
        ('highway=footway', 'Calçada', 'Infraestrutura para pedestres e ciclistas');

        INSERT INTO t_feicao_osm (tag_osm, descricao, codigo_categoria_amenidade)
        SELECT
            tmp.tag_osm,
            tmp.descricao,
            categoria.codigo
        FROM temp_feicao_osm tmp
        INNER JOIN t_categoria_amenidade categoria
            ON tmp.nome_categoria_amenidade = categoria.nome
        ORDER BY tmp.codigo;
        
        DROP TABLE temp_feicao_osm;

        UPDATE t_feicao_osm
        SET flag_tag_ativa = TRUE
        WHERE tag_osm IN (
            'amenity=bar',
            'amenity=cafe',
            'amenity=restaurant',
            'shop=convenience',
            'shop=food',
            'shop=greengrocer',
            'shop=supermarket',
            'amenity=bank',
            'amenity=fire_station',
            'amenity=police',
            'amenity=post_office',
            'amenity=townhall',
            'shop=department_store',
            'shop=general',
            'shop=mall',
            'shop=wholesale',
            'shop=variety_store',
            'amenity=cinema',
            'amenity=events_venue',
            'amenity=music_venue',
            'amenity=theatre',
            'amenity=place_of_worship',
            'leisure=fitness_centre',
            'leisure=playground',
            'leisure=sports_centre',
            'leisure=swimming_pool',
            'leisure=park',
            'amenity=kindergarten',
            'amenity=school',
            'amenity=university',
            'amenity=clinic',
            'amenity=hospital',
            'amenity=pharmacy',
            'shop=medical_supply',
            'building=commercial',
            'building=industrial',
            'building=office',
            'building=retail',
            'highway=bus_stop',
            'public_transport=station',
            'railway=station',
            'railway=subway_entrance'
        );

        INSERT INTO t_modalidade_transporte (nome, descricao, velocidade_media_kph) VALUES
        ('walk', 'Caminhada', 4.0),
        ('bike', 'Bicicleta', 13.0);
    '''