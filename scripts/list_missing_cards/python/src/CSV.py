from scripts.list_missing_cards.python.src.File import File

class CSV(File):

    def get_data_as_dict(self) -> dict:
        return {
            'header': [],
            'body': []
        }

    @staticmethod
    def get_header_as_list() -> list:
        return ['name']