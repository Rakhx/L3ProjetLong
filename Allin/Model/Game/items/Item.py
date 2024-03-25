# classe commune à tout les éléments sur le plateau
import abc

class Item(abc.ABC):
    def __init__(self, pos):
        self.position = pos
    def getRepr(self):
        return f"{self.getLetter()}{self.number}"
    @abc.abstractmethod
    def getLetter(self):
        pass

    @abc.abstractmethod
    def getItemType(self):
       pass
