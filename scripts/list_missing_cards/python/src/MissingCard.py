class MissingCard:
    def __init__(
            self, _id: int, index: int, code_type: str, name: str,
            missing_units: int
            ):
        self.id= _id
        self.index= index
        self.codeType= code_type
        self.name= name
        self.missing_units= missing_units