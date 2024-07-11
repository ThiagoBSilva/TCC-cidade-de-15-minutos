# Sobre o projeto

Este projeto se trata da implementação do processo proposto no Trabalho de Conclusão de Curso da UFV-CRP, com o objetivo de calcular o grau de adequação ao conceito da cidade de 15 minutos dos municípios brasileiros.

O conceito da cidade de 15 minutos foi cunhado pelo planejador urbano Carlos Moreno, em 2016, tomando inspiração em outros modelos de organização e planejamento urbano com um enfoque maior na proximidade dos cidadãos em relação a pontos de interesse, em detrimento da facilidade de locomoção para alcançar um determinado destino.

Em linhas gerais, uma cidade de 15 minutos é aquela em que os seus habitantes conseguem alcançar qualquer amenidade essencial para vivência através de uma viagem de, no máximo, 15 minutos, tanto por meio da caminhada quanto por bicicleta.

Assim, conforme enunciado anteriormente, este projeto visa realizar o cálculo para possibilitar a visualização em termos quantitativos do grau de adequação dos municípios brasileiros a esse conceito e isso é feito através de 6 etapas, sendo elas:

1. Carga inicial dos dados essenciais;
2. Geração da malha hexagonal dos municípios;
3. Extração das amenidades essenciais;
4. Cálculo da matriz de tempos de viagem entre origens e destinos;
5. Cálculo do índice de 15 minutos dos municípios;
6. Cálculo do índice de 15 minutos das unidade federativas.

Ao final, os resultados obtidos são utilizados para alimentar um dashboard, criado principalmente para auxiliar na visualização, análise dos dados gerados e na chegada de conclusões, além de tornar as informações obtidas mais compreensíveis, facilitando a difusão e entendimento dos resultados.

# Detalhamento do projeto

## Estrutura do projeto

O projeto é estruturado de maneira similar a um projeto Java que segue o padrão Spring MVC, principalmente pela familiariadade dos desenvolvedores do projeto a esse padrão. Dessa forma, o projeto é estruturado na seguinte disposição:

```
C:.
├───data
├───logs
└───src
    ├───main
    │   ├───client
    │   │
    │   ├───component
    │   │
    │   ├───model
    │   │   ├───constants
    │   │   │   └───queries
    │   │   │
    │   │   └───enums
    │   │
    │   ├───repository
    │   │
    │   ├───service
    │   │   └───client
    │   │
    │   └───util
    │
    └───resource
```

### Dicionário de diretórios

- **data**: Contém os arquivos utilizados durante o processamento.
- **logs**: Contém os arquivos de logs gerados em cada etapa.
- **src**: Contém o código fonte.
    - **main**: Contém os arquivos principais da implementação.
        - **client**: Contém os arquivos que operam na camada de comunicação com diferentes APIs.
        - **component**: Contém arquivos com implementações mais gerais dos passos executados em cada etapa, basicamente consistem na implementação da "regra de negócio".
        - **model**: Contém arquivos que definem as classes modelo do projeto.
            - **constants**: Contém arquivos onde valores constantes são definidos.
                - **queries**: Contém arquivos onde valores constantes são definidos, porém especificamente para a definição de queries.
        - **repository**: Contém arquivos que operam na camada de comunicação com diferentes entidades do banco de dados.
        - **service**: Contém arquivos que encapsulam os repositories, sendo possível definir tratamentos para cada comportamento ao realizar uma chamada ao banco de dados.
            - **client**: Contém arquivos que encapsulam os clients, sendo possível definir tratamentos para cada comportamento ao realizar uma chamada às APIs.
        - **util**: Contém arquivos que oferecem métodos utilitários.
    - **resource**: Contém os arquivos onde são definidos recursos importantes para a execução do código, geralmente composto por arquivos de configuração.

## Etapas de processamento

Todas as etapas do processo compartilham de alguns passos que são comuns a todas elas, esses passos são:

- Importação dos módulos e classes necessários;
- Desativação dos warnings do tipo DeprecationWarning e UserWarning;
- Criação de diretórios (específico para a etapa 1);
- Configuração do Logger;
- Conexão com o banco de dados;
- Instanciação dos Services e Components utilizados em cada etapa;
- Processamento (difere para cada etapa, será abordado em seguida);
- Desconexão com o banco de dados.

### Etapa 1

Esta é a etapa inicial do processamento, onde as informações essenciais são buscadas e a estrutura do banco de dados é gerada, além da inicialização de alguns dados estáticos. Os passos executados nesta etapa são:

- Inicialização do banco de dados
    - Drop das tabelas existentes
    - Criação das tabelas necessárias
    - Inserção de dados estáticos pré-definidos
        - Categorias e sub-categorias de amenidades
        - Tipos de feições do OSM, que representam as amenidades essenciais
        - Modalidades de transporte e suas respectivas velocidades médias
- Obtenção do shapefile das unidades federativas (Fonte: IBGE)
- Obtenção do shapefile dos municípios (Fonte: IBGE)
- Montagem da carga inicial
    - Conversão dos shapefiles para GeoDataFrames
    - Tratamento de colunas dos GeoDataFrames
- Persistência dos GeoDataFrames na base

### Etapa 2

Etapa onde cada município terá a sua malha hexagonal gerada com base em dados da biblioteca H3. Os passos executados nesta etapa são:

- Verificação de registros pendentes de processamento
- Busca dos registros pendentes de processamento
- Divisão dos registros para processamento paralelo com o Dask
    - Obtenção dos códigos dos hexágonos H3 que compõem o polígono do município
    - Obtenção das bordas de cada hexágono H3
    - Geração do polígono de cada hexágono a partir das bordas obtidas
    


## Estrutura do banco de dados

Incluir diagrama do BD

# Executando o projeto

## 1. Pacotes necessários

## 2. Recomendações

## 3. Instruções