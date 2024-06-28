from traceback import format_exc

class ExceptionUtil:

    @staticmethod
    def montar_exception_padrao(exception: type[Exception]) -> str:
        return f"Erro: {type(exception).__name__} na linha {exception.__traceback__.tb_lineno} do arquivo {exception.__traceback__.tb_frame.f_code.co_filename}: {exception}."
    
    @staticmethod
    def montar_exception_historico_erro(exception: type[Exception]) -> str:
        return f"{type(exception).__name__}: {exception}. {format_exc()}."