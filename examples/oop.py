class Drink:
    def __init__(self, lit: float = 0.5, fiz: bool = False):
        self.liters = lit 
        self.fizzy = fiz
    
    @classmethod
    def getDescription(cls) -> str:
        return "Brilliant drink"


class Beer(Drink):
    def __init__(self, perc: int = 5, lit: float = 0.5, fiz: bool = False):
        super().__init__(lit, fiz)
        self.percents = perc
    
    def getPercents(self) -> int:
        return self.percents
    
    def getNothing(self) -> None:
        return None


bgh: Beer = Beer(6, 0.499) 
bgh.getDescription()

# improve regular beer
bgh.percents = bgh.percents + 1 
