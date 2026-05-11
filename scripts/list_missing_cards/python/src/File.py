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
        if File.is_path_ok(file_absolute_path):
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
        raise Exception

    @staticmethod
    def are_parameters_ok(is_path_ok: bool, process: bool) -> bool:
        if type(is_path_ok) is not bool or type(process) is not bool:
            raise Exception
        return False

    @staticmethod
    def is_path_ok(absolute_path: str) -> bool:
        if File.is_parameter_str(absolute_path):
            return True
        raise Exception

    @staticmethod
    def is_parameter_str(param: str) -> bool:
        if type(param) is not str:
            raise ParameterException(
                400,
                str,
                type(param),
                'open_with_process',
                'file_absolute_path'
            )
        return True

    @staticmethod
    def is_process_ok(process: Callable) -> bool:
        if not callable(process):
            raise ParameterException(
                400,
                Callable,
                type(process),
                'open_with_process',
                'process',
            )
        return False