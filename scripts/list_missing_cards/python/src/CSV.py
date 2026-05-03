from scripts.list_missing_cards.python.src.File import File

class CSV(File):

    def get_data_as_dict(self) -> dict:
        return {
            'header': None
        }
