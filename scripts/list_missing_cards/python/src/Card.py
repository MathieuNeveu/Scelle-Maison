import csv
from io import TextIOWrapper

class Card:
    def __init__(
            self, _id: int, index: int, code_type: str, lang: str, units: int,
            faction: str, name: str
            ):
        self._id = _id
        self.index= index
        self.codeType= code_type
        self.lang= lang
        self.units= units
        self.faction= faction
        self.name= name

    @classmethod
    def from_csv(cls, csv_file: TextIOWrapper) -> list['Card']:
        return [cls(1, 1, 'R', 'EN', 0, 'Axiom', 'Sierra & Oddball')]

    @staticmethod
    def csv_line_to_dict(csv_file: TextIOWrapper) -> dict:
        # csv_reader = csv.reader(csv_file, delimiter=',')
        return {
            '_id': None,
            'index': None,
            'codeType': None,
            'lang': None,
            'units': None,
            'faction': None,
            'name': None
        }

    @staticmethod
    def csv_to_dict_list(csv_file: TextIOWrapper) -> list:
        return []
