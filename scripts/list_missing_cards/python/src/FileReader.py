from scripts.list_missing_cards.python.src.Exceptions.ParameterException import ParameterException

class FileReader:

    @staticmethod
    def open_with_process(file_absolute_path: str, process):
        if type(file_absolute_path) is not str:
            raise ParameterException(
                400,
                str,
                type(file_absolute_path),
                'open_with_process',
                'file_absolute_path'
            )
        with open(file_absolute_path, 'r') as file:
            return process(file)
