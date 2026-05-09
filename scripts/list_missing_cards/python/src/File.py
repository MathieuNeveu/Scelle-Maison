from abc import ABC, abstractmethod
from collections.abc import Callable
from io import TextIOWrapper

from scripts.list_missing_cards.python.src.Exceptions.ParameterException import ParameterException

class File(ABC):

    @abstractmethod
    def get_data_as_dict(self) -> dict:
        pass

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
        if not callable(process):
            raise ParameterException(
                400,
                Callable,
                type(process),
                'open_with_process',
                'process',
            )
        with open(file_absolute_path, 'r') as file:
            return process(file)

    @staticmethod
    def is_path_ok() -> bool:
        return True