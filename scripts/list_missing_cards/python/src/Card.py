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
        #test csv length > 1 line
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
    def csv_line_to_dict(line: list[str]) -> dict:
        return {
            '_id': None,
            'index': None,
            'codeType': line[1],
            'lang': None,
            'units': None,
            'faction': None,
            'name': None
        }

    @staticmethod
    def csv_to_dict_list(csv_file: TextIOWrapper) -> list:
        csv_reader = csv.reader(csv_file, delimiter=',')
        cards: list[dict] = []
        # check that csv columns number match card's dictionary keys number
        # ignore 1st csv line (header)
        for line in csv_reader:
            parsed_line: dict = Card.csv_line_to_dict(line)
            cards.append(parsed_line)
        return cards
