# Sobre o projeto

Este projeto se trata da implementação do método proposto no Trabalho de Conclusão de Curso da UFV-CRP, com o objetivo de calcular o grau de adequação ao conceito da "cidade de 15 minutos" dos municípios brasileiros.

O conceito da "cidade de 15 minutos" foi cunhado pelo planejador urbano Carlos Moreno em 2016, tomando inspiração em outros modelos de organização e planejamento urbano com um enfoque maior na proximidade dos cidadãos em relação a pontos de interesse, em detrimento da facilidade de locomoção para alcançar um determinado destino.

Em linhas gerais, uma "cidade de 15 minutos" é aquela em que os seus habitantes conseguem alcançar qualquer amenidade essencial para vivência através de uma viagem de, no máximo, 15 minutos, tanto por meio da caminhada quanto por bicicleta.

Assim, conforme enunciado anteriormente, este projeto visa realizar o cálculo para possibilitar a visualização em termos quantitativos do grau de adequação dos municípios brasileiros a esse conceito. Esse processo é realizado através de 6 etapas, que serão melhor detalhadas mais a frente.

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

- **data**: Arquivos de dados utilizados durante o processamento.
- **logs**: Arquivos de logs gerados em cada etapa.
- **src**: Código fonte.
    - **main**: Arquivos principais da implementação.
        - **client**: Operações na camada de comunicação com diferentes APIs.
        - **component**: Implementação da "regra de negócio".
        - **model**: Classes modelo do projeto.
            - **constants**: Definição de valores constantes (parâmetros).
                - **queries**: Definição de queries constantes. 
        - **repository**: Operações na camada de comunicação com diferentes entidades do banco de dados.
        - **service**: Encapsulamento dos repositories.
            - **client**: Encapsulamento dos clients.
        - **util**: Métodos utilitários.
    - **resource**: Recursos importantes para a execução do código, geralmente composto por arquivos de configuração.

## Etapas de processamento

A seguir há um maior detalhamento sobre as etapas de processamento, cada uma contendo uma breve descrição do seu funcionamento e um fluxograma ilustrando os passos realizados.

### Etapa 1

Esta é a etapa inicial do processamento, onde as informações essenciais são buscadas e a estrutura do banco de dados criada, além da inserção de dados estáticos em algumas tabelas.

![fluxograma-etapa-1](https://github.com/user-attachments/assets/fc89133e-de9e-4b32-ad33-5d47f844b552)

### Etapa 2

Nesta etapa cada município terá a sua malha hexagonal gerada a partir da sua geometria. Para isso, o módulo H3 é empregado para realizar a busca pelos hexágonos que compõem o município, definidos através do índice espacial hierárquico hexagonal do Uber.

![fluxograma-etapa-2](https://github.com/user-attachments/assets/e1814539-f0df-4a59-9297-023ee8f182b2)

### Etapa 3

Aqui serão extraídas as amenidades dos municípios. A busca pelos dados ocorre por meio de chamadas à API Overpass, realizadas com o módulo OSMnx, que acessa a base de dados da plataforma colaborativa de dados geográficos OpenStreetMap.

![fluxograma-etapa-3](https://github.com/user-attachments/assets/8e47fbf5-dccb-4879-b15f-c9602cbeb5f5)

### Etapa 4

Nesta etapa é realizada a construção das matrizes de tempos de viagem dos municípios, para ambas as modalidades de transporte consideradas. Essa tarefa é realizada com o uso dos dados previamente obtidos e também dos grafos da rede de transporte dos municípios extraídos da API Overpass. Com esses dados são formadas associações de pontos de origem e destino e, posteriomente, é aplicado o algoritmo de Djikstra, por meio do OSMnx, para encontrar rotas de caminho mínimo entre esses pontos considerando o tempo de viagem o fator de custo do algoritmo. 

![fluxograma-etapa-4](https://github.com/user-attachments/assets/4eb08022-43ad-456d-8469-bacf2fb2b1fb)

### Etapa 5

Após a construção das matrizes de tempo de viagem dos municípios, o índice de conformidade dos municípios à "cidade de 15 minutos" é calculado, tomando como base os tempos obtidos e os tipos de amenidades atingíveis em até 15 minutos, para cada modalidade de transporte.

![fluxograma-etapa-5](https://github.com/user-attachments/assets/fe1d935a-f764-4f5d-9450-1e616e7f1766)

### Etapa 6

Na última etapa, há a agregação dos valores do índice calculado para os municípios para formar os índices das unidades federativas em que pertencem.

![fluxograma-etapa-6](https://github.com/user-attachments/assets/ed5914c3-4026-4b27-aff5-f34968de7e16)

## Estrutura do banco de dados

A figura baixo ilustra as tabelas que compõem o banco de dados e seus relacionamentos, em notação crow's foot. Acompanhado a ela se encontra uma relação que descreve os dados armazenados em cada uma das entidades do banco.

![diagrama-bd](https://github.com/user-attachments/assets/4f7e4038-4471-4258-882b-ea8368765f57)

| Tabela                          | Descrição                                                                                                                                              |
|---------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| `t_no_grafo_municipio`          | Tabela auxiliar dos nós dos grafos da rede de transporte de um município.                                                                              |
| `t_historico_erro`              | Tabela para armazenamento de registros de erros.                                                                                                       |
| `t_categoria_amenidade`         | Tabela das categorias e subcategorias das amenidades.                                                                                                  |
| `t_feicao_osm`                  | Tabela das *features* do *OpenStreetMap*, mapeadas para uma determinada subcategoria.                                                                  |
| `t_modalidade_transporte`       | Tabela das modalidades de transporte e suas velocidades médias em km/h.                                                                                |
| `t_unidade_federativa`          | Tabela das unidades federativas do Brasil.                                                                                                             |
| `t_municipio`                   | Tabela dos municípios brasileiros.                                                                                                                     |
| `t_malha_hexagonal_municipio`   | Tabela dos hexágonos que compõem a representação dos municípios em uma malha hexagonal.                                                                |
| `t_amenidade_municipio`         | Tabela das amenidades dos municípios.                                                                                                                  |
| `t_matriz_tempo_viagem`         | Tabela que contém os valores calculados dos tempos de viagem entre cada associação de origem e destino formada, sendo as origens os centroides dos hexágonos da malha hexagonal e os destinos as amenidades. |
| `t_indice_hexagono`             | Tabela com os valores calculados para o índice de conformidade de cada hexágono das malhas hexagonais.                                                  |
| `t_indice_municipio`            | Tabela com os valores calculados para o índice de conformidade de cada município brasileiro.                                                           |
| `t_indice_unidade_federativa`   | Tabela com os valores calculados para o índice de conformidade de cada unidade federativa do Brasil.                                                   |


# Executando o projeto

Para a execução do projeto é necessário a instalação do Python em sua versão 3.11.5 e uma instância de banco de dados PostgreSQL com a extensão espacial PostGIS habilitada. Abaixo serão detalhados os pacotes necessários, algumas recomendações para melhoria de desempenho e visualização e as instruções para a execução correta do projeto.

## 1. Pacotes necessários

| Módulo      | Versão  | Finalidade                                                                                                     |
|-------------|---------|-----------------------------------------------------------------------------------------------------------------|
| `dask`      | 2023.6.0| Processamento paralelizado de DataFrames.                                                                       |
| `geopandas` | 0.14.3  | Manipulação de GeoDataFrames; operações no banco de dados geográfico.                                           |
| `h3`        | 3.7.6   | Extração da malha hexagonal a partir do polígono dos municípios.                                                |
| `networkx`  | 3.1     | Manipulação dos grafos da rede de transporte dos municípios.                                                    |
| `numpy`     | 1.24.3  | Operações sobre arrays NumPy.                                                                                   |
| `osmnx`     | 1.9.1   | Extração de dados das amenidades essenciais; extração dos grafos das redes de transporte dos municípios.        |
| `pandas`    | 2.0.3   | Manipulação de DataFrames; operações no banco de dados.                                                         |
| `retry`     | 0.9.2   | Aplicação de retentativas para chamadas de API.                                                                 |
| `shapely`   | 2.0.2   | Manipulação de geometrias.                                                                                      |
| `sqlalchemy`| 1.4.39  | Manipulação e controle de conexões com o banco de dados.                                                        |
| `urllib`    | 1.26.16 | Realização de downloads de arquivos na internet.                                                                |
| `yaml`      | 0.2.5   | Manipulações de arquivos YAML.                                                                                  |

## 2. Recomendações

* **DBeaver**: é um gerenciador universal de banco de dados. O uso dele é recomendado pelo fato de ser muito versátil, contém inúmeras ferramentas para auxiliar na visualização dos dados e aprimora bastante a qualidade de vida em comparação ao pgAdmin 4. Além disso, para dados geográficos, o DBeaver conta com uma ferramenta nativa para a visualização dos dados.

* **API Overpass via Docker**: é uma instância local da API Overpass que pode ser utilizada no lugar do serviço hospedado na Internet. O uso da instância local acelera consideravelmente a rapidez na consulta das informações, uma vez que o trâmite para estabelecimento de conexão em rede remota e problemas de rede não existem. Além disso o serviço API Overpass pode bloquear o acesso em decorrência do volume elevado de chamadas.
  - A imagem utilizada foi criada pelo usuário [wiktorn](https://github.com/wiktorn) e pode ser acessada aqui: [Overpass-API](https://github.com/wiktorn/Overpass-API/tree/master).
  - O projeto conta com um arquivo compose.yaml configurado, que pode ser utilizado para a criação e execução do container da instância local.
  - O processo para download e inicialização pode demorar um pouco. Para a execução realizada pelos desenvolvedores o processo demorou pouco mais de 4 horas.

* **Arquivo de parâmetros**: o projeto conta com um arquivo chamado ParametrosConstantes.py. Nele, são definidos valores para diversos parâmetros utilizados em diferentes partes e etapas do processamento. É recomendável não alterar os parâmetros referentes ao processamento em batch que é realizado, principalmente para a etapa 4 e 5, onde muitas das operações são realizadas via banco de dados. A quantidade de partições para processamento paralelizado está setado como 1 para essas etapas, em função de um problema de condição de corrida no banco de dados que estava ocorrendo.
  
## 3. Instruções

O processo para a execução do código é simples, basta seguir o passo-a-passo abaixo:

1. Clonar o repositório do projeto
2. Criar um banco de dados específico para o projeto
3. Alterar o arquivo de propriedades da aplicação (./src/resource/application.yaml) inserindo as configurações para conexão com o banco de dados
    - Caso esteja usando a API Overpass via Docker, configurar a porta correta para o recurso e habilitar o uso da instância local
5. Executar os notebooks localizados no diretório main, pela ordem de numeração
