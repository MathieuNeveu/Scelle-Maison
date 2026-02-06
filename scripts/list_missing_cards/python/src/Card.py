class Card:
    def __init__(
            self, id: int, index: int, codeType: str, lang: str, units: int,
            faction: str, name: str
            ):
        self.id = id
        self.index= index
        self.codeType= codeType
        self.lang= lang
        self.units= units
        self.faction= faction
        self.name= name
        
