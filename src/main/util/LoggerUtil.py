from model.constants.ParametrosConstantes import ParametrosConstantes

from logging import Logger, Formatter, StreamHandler, FileHandler, getLogger

class LoggerUtil:

    @staticmethod
    def configurar_logger(arquivo_log: str) -> Logger:
        formatter = Formatter(fmt="%(asctime)s - %(levelname)s - %(module)s - %(message)s")

        handler = StreamHandler()
        handler.setFormatter(fmt=formatter)

        file_handler = FileHandler(filename=arquivo_log)
        file_handler.setFormatter(fmt=formatter)

        logger = getLogger(name=ParametrosConstantes.LOGGER_NOME)
        logger.setLevel(level=ParametrosConstantes.LOGGER_NIVEL)
        logger.addHandler(hdlr=handler)
        logger.addHandler(hdlr=file_handler)

        return logger
    
    @staticmethod
    def recuperar_logger() -> Logger:
        return getLogger(name=ParametrosConstantes.LOGGER_NOME)