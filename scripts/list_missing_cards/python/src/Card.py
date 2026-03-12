class Card:
    def __init__(
            self, _id: int, index: int, code_type: str, lang: str, units: int,
            faction: str, name: str
            ):
        self.id = _id
        self.index= index
        self.codeType= code_type
        self.lang= lang
        self.units= units
        self.faction= faction
        self.name= name

    @staticmethod
    def from_csv(self):
        return Card(1, 1, 'H', 'EN', 0, 'Axiom', 'Sierra & Oddball')
