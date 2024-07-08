from util.ExceptionUtil import ExceptionUtil
from util.LoggerUtil import LoggerUtil

from yaml import safe_load

log = LoggerUtil.recuperar_logger()
class YAMLUtil:

    @staticmethod
    def converter_yaml_para_dict(arquivo_yaml: str) -> dict:
        try:
            with open(file=arquivo_yaml, mode="r") as stream:
                return safe_load(stream)
            
        except Exception as e:
            log.error(msg=f"Houve um erro ao tentar recuperar os valores do arquivo YAML especificado no caminho {arquivo_yaml}. "
                          f"{ExceptionUtil.montar_erro_exception_padrao(e)}")
            raise e