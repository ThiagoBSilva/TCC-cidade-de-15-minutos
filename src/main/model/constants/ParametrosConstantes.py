from logging import INFO

class ParametrosConstantes:

    # Parâmetros para logging
    LOGGER_NOME = "root"
    LOGGER_NIVEL = INFO

    # Parâmetro para definição de diretórios (caminhos relativos ao diretório src/main)
    DIRETORIO_DADOS = "../../data"
    DIRETORIO_CACHE_OSMNX = "./cache"
    DIRETORIO_LOGS = "../../logs"
    DIRETORIO_RESOURCE = "../resource"

    # Parâmetros para caminhos de arquivos
    CAMINHO_APPLICATION_YAML = DIRETORIO_RESOURCE + "/application.yaml"
    CAMINHO_LOG_CARGA_INICIAL = DIRETORIO_LOGS + "/1_carga_inicial.log"
    CAMINHO_LOG_GERACAO_MALHA_HEXAGONAL = DIRETORIO_LOGS + "/2_geracao_malha_hexagonal.log"
    CAMINHO_LOG_EXTRACAO_AMENIDADES = DIRETORIO_LOGS + "/3_extracao_amenidades.log"
    CAMINHO_LOG_CALCULO_MATRIZ_TEMPO_VIAGEM = DIRETORIO_LOGS + "/4_calculo_matriz_tempo_viagem.log"
    CAMINHO_SHAPEFILE_UNIDADES_FEDERATIVAS = DIRETORIO_DADOS + "/BR_UF_2022.zip"
    CAMINHO_SHAPEFILE_MUNICIPIOS = DIRETORIO_DADOS + "/BR_Municipios_2022.zip"

     # URLs para obtenção de dados
    URL_IBGE_SHAPEFILE_UNIDADES_FEDERATIVAS = "https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2022/Brasil/BR/BR_UF_2022.zip"
    URL_IBGE_SHAPEFILE_MUNICIPIOS = "https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2022/Brasil/BR/BR_Municipios_2022.zip"

    # Parâmetros para o fluxo de retries em requisições
    RETRY_QTDE_MAX_RETENTATIVAS = 3
    RETRY_DELAY_ENTRE_RETENTATIVAS = 30 # Segundos  

    # Parâmetros relacionados à geometrias
    GEOMETRIA_COLUNA_DEFAULT = "geometria"
    GEOMETRIA_CRS_DEFAULT = "EPSG:4326" # WGS84
    GEOMETRIA_CRS_METRICO_DEFAULT = "EPSG:3857" # Pseudo-Mercator

    # Parâmetro para a resolução da malha hexagonal
    RESOLUCAO_MALHA_HEXAGONAL = 8
    MULTIPLICADOR_AREA_ANALISE_HEXAGONO = 1.5

    # Parâmetros para processamento em batch
    BATCH_QTDE_REGISTROS_ETAPA_GERACAO_MALHA = 100
    BATCH_QTDE_PARTICOES_DASK_ETAPA_GERACAO_MALHA = 10

    BATCH_QTDE_REGISTROS_ETAPA_EXTRACAO_AMENIDADES = 5
    BATCH_QTDE_PARTICOES_DASK_ETAPA_EXTRACAO_AMENIDADES = 5

    BATCH_QTDE_REGISTROS_ETAPA_CALCULO_MATRIZ_TEMPO_VIAGEM = 5
    BATCH_QTDE_PARTICOES_DASK_ETAPA_CALCULO_MATRIZ_TEMPO_VIAGEM = 5

    # Parâmetros de configuração do OSMnx
    OSMXN_USAR_CACHE = False
    OSMNX_LIMPAR_CACHE = False