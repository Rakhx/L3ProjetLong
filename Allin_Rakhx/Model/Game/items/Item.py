# classe commune à tout les éléments sur le plateau
import abc

class Item(abc.ABC):
    def __init__(self, pos):
        self.positions = pos
    def getRepr(self):
        return f"{self.getLetter()}{self.number}"
    @abc.abstractmethod
    def getLetter(self):
        pass

    def getPositions(self):
        return self.positions

    @abc.abstractmethod
    def getItemType(self):
       pass
