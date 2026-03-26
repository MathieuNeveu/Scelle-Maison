import csv
import json
from io import TextIOWrapper

from scripts.list_missing_cards.python.src.ParameterException import ParameterException
from scripts.list_missing_cards.python.src.ParsingException import ParsingException
from scripts.list_missing_cards.python.src.ResourceException import ResourceException


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
    def from_csv(cls, csv_absolute_path: str) -> list['Card']:
        #test csv length > 1 line
        csv_file: TextIOWrapper = cls.open_csv_file(csv_absolute_path)
        dict_list: list[dict] = cls.csv_to_dict_list(csv_file)
        card_list: list[Card] = []
        for card_dict in dict_list:
            card_list.append(cls(
                card_dict['_id'],
                card_dict['index'],
                card_dict['codeType'],
                card_dict['lang'],
                card_dict['units'],
                card_dict['faction'],
                card_dict['name']
            ))
        # test that returned Card objects number is equal to csv lines -1
        return card_list

    @staticmethod
    def open_csv_file(csv_absolute_path: str) -> TextIOWrapper:
        if type(csv_absolute_path) is not str:
            raise ParameterException(
                400,
                str,
                type(csv_absolute_path),
                'open_csv_file',
                'csv_absolute_path'
            )
        try:
            file = open(csv_absolute_path, 'r', encoding='utf-8-sig')
        except:
            raise ResourceException(
                404,
                csv_absolute_path
            )
        else:
            return file

    @staticmethod
    def csv_line_to_dict(line: list[str]) -> dict:
        return {
            '_id': None,
            'index': None,
            'codeType': Card.parse_code_type(line[1]),
            'lang': None,
            'units': None,
            'faction': None,
            'name': None
        }

    @staticmethod
    def parse_code_type(code_type_input: str) -> str:
        return code_type_input[0]

    @staticmethod
    def csv_to_dict_list(csv_file: TextIOWrapper) -> list:
        # check that csv columns number match card's dictionary keys number
        if Card.csv_header_validation(csv_file):
            csv_reader = csv.reader(csv_file, delimiter=',')
            cards: list[dict] = []
            # ignore 1st csv line (header)
            # csv_body = next(csv_reader)
            for line in csv_reader:
                parsed_line: dict = Card.csv_line_to_dict(line)
                cards.append(parsed_line)
            return cards
        raise Exception('Mauvais format CSV.')

    @staticmethod
    def csv_header_validation(csv_file: TextIOWrapper) -> bool:
        config_file = open("../config.json")
        json_config = json.load(config_file)
        card_csv_keys_config = json_config['csv']['header_keys']['Card']

        csv_reader = csv.reader(csv_file, delimiter=',')
        csv_header = next(csv_reader)

        validation_status: bool = True

        for key_value in card_csv_keys_config.values():
            if key_value not in csv_header:
                config_file.close()
                raise ParsingException(
                    400,
                    "Mauvais format CSV: une/des clés n'est pas présente de le header",
                    key_value,
                    csv_header
                )
                validation_status = False

        config_file.close()
        return validation_status