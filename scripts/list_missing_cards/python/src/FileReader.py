from collections.abc import Callable
from io import TextIOWrapper

from scripts.list_missing_cards.python.src.Exceptions.ParameterException import ParameterException

class FileReader:

    @staticmethod
    def open_with_process(file_absolute_path: str, process: Callable[[TextIOWrapper], ...]):
        if type(file_absolute_path) is not str:
            raise ParameterException(
                400,
                str,
                type(file_absolute_path),
                'open_with_process',
                'file_absolute_path'
            )
        if type(process) is int:
            raise ParameterException(
                400,
                Callable,
                int,
                'open_with_process',
                'process',
            )
        with open(file_absolute_path, 'r') as file:
            return process(file)
