from util.ExceptionUtil import ExceptionUtil
from util.LoggerUtil import LoggerUtil

from os import mkdir
from os.path import isdir, isfile
from shutil import rmtree

log = LoggerUtil.recuperar_logger()
class OSUtil:

    @staticmethod
    def verificar_diretorio_existente(diretorio: str) -> bool:
        return isdir(s=diretorio)
    
    @staticmethod
    def verificar_arquivo_existente(arquivo: str) -> bool:
        return isfile(path=arquivo)
    
    @staticmethod
    def criar_diretorio(diretorio: str) -> None:
        try:
            if not OSUtil.verificar_diretorio_existente(diretorio):
                mkdir(path=diretorio)
        except Exception as e:
            log.error(msg=f"Houve um erro ao criar o diretório {diretorio}. {ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e

    @staticmethod   
    def deletar_diretorio(diretorio: str) -> None:
        try:
            if OSUtil.verificar_diretorio_existente(diretorio):
                rmtree(path=diretorio)
                return
            
            log.warning(msg=f"O diretório informado ({diretorio}) não foi encontrado.")
        except Exception as e:
            log.error(msg=f"Houve um erro ao tentar remover o diretório {diretorio}. {ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e