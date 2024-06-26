from warnings import filterwarnings

class WarningUtil:

    @staticmethod
    def ignorar_warning(categoria: type[Warning]) -> None:
        filterwarnings(action="ignore", category=categoria)