import pandas as pd

class ConexaoBD:
    def __init__(self, flag_modo_testes:bool):
        if flag_modo_testes:
            self.user = 'postgres'
            self.password = '123456'
            self.server = 'localhost'
            self.port = '5432'
            self.database = 'bd_tcc_hml'
        else:
            self.user = 'postgres'
            self.password = '123456'
            self.server = 'localhost'
            self.port = '5432'
            self.database = 'bd_tcc'

class Municipio:
    def __init__(self, sr_municipio:pd.Series):
        self.codigo = sr_municipio['codigo'] # codigo
        self.nome = sr_municipio['nome']
        self.nome_uf = sr_municipio['nome_uf']

class ModalidadeTransporte:
    def __init__(self, sr_modalidade_transporte:pd.Series):
        self.codigo = sr_modalidade_transporte['codigo']
        self.nome = sr_modalidade_transporte['nome']
        self.velocidade_media_kph = sr_modalidade_transporte['velocidade_media_kph']