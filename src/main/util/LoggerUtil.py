from model.constants.ParametrosConstantes import ParametrosConstantes

import logging

class LoggerUtil:

    @staticmethod
    def configurar_logger(arquivo_log: str) -> logging.Logger:
        formatter = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(module)s - %(message)s")

        handler = logging.StreamHandler()
        handler.setFormatter(fmt=formatter)

        file_handler = logging.FileHandler(filename=arquivo_log)
        file_handler.setFormatter(fmt=formatter)

        logger = logging.getLogger(name=ParametrosConstantes.LOGGER_NOME)
        logger.setLevel(level=ParametrosConstantes.LOGGER_NIVEL)
        logger.addHandler(hdlr=handler)
        logger.addHandler(hdlr=file_handler)

        return logger
    
    @staticmethod
    def recuperar_logger() -> logging.Logger:
        return logging.getLogger(name=ParametrosConstantes.LOGGER_NOME)