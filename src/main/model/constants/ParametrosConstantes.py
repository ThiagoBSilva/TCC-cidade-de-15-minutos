from logging import INFO

class ParametrosConstantes:

    # Parâmetros para logging
    NOME_LOGGER = "root"
    NIVEL_LOGGER = INFO

    # Parâmetro para definição de diretórios
    DIRETORIO_DADOS = "../../data"
    DIRETORIO_LOGS = "../../logs"
    DIRETORIO_RESOURCE = "../resource"

    # Parâmetros para caminhos de arquivos
    CAMINHO_APPLICATION_YAML = DIRETORIO_RESOURCE + "/application.yaml"
    CAMINHO_LOG_CARGA_INICIAL = DIRETORIO_LOGS + "/1_carga_inicial.log"
    CAMINHO_LOG_GERACAO_MALHA_HEXAGONAL = DIRETORIO_LOGS + "/2_geracao_malha_hexagonal.log"
    CAMINHO_SHAPEFILE_UNIDADES_FEDERATIVAS = DIRETORIO_DADOS + "/BR_UF_2022.zip"
    CAMINHO_SHAPEFILE_MUNICIPIOS = DIRETORIO_DADOS + "/BR_Municipios_2022.zip"

     # URLs para obtenção de dados
    URL_IBGE_SHAPEFILE_UNIDADES_FEDERATIVAS = "https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2022/Brasil/BR/BR_UF_2022.zip"
    URL_IBGE_SHAPEFILE_MUNICIPIOS = "https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2022/Brasil/BR/BR_Municipios_2022.zip"

    # Parâmetros para o fluxo de retries em requisições
    QTDE_MAX_RETENTATIVAS = 3
    DELAY_ENTRE_RETENTATIVAS = 30 # Segundos  

    # Parâmetros relacionados à geometrias
    COLUNA_GEOMETRIA_DEFAULT = "geometria"
    CRS_DEFAULT = "EPSG:4326"

    # Parâmetro para a resolução da malha hexagonal
    RESOLUCAO_MALHA_HEXAGONAL = 7

    # Parâmetros para processamento em batch
    QTDE_REGISTROS_ETAPA_GERACAO_MALHA = 100
    QTDE_PARTICOES_DASK = 10
  