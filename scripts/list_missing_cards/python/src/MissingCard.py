class MissingCard:
    def __init__(
            self, id: int, index: int, codeType: str, name: str,
            missingUnits: int
            ):
        self.id= id
        self.index= index
        self.codeType= codeType
        self.name= name