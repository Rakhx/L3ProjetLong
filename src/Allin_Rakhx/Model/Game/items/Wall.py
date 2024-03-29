from src.Allin_Rakhx.Model.Game.EnumCase import EnumPlayer, EnumWall
from src.Allin_Rakhx.Model.Game.items.Item import Item
import abc

class Wall(Item, abc.ABC):
    def __init__(self, positions, owner, taille=2):
        super().__init__(positions)
        # taille de base
        self.taille = taille
        self.owner = owner
        self.number = 1 if owner == EnumPlayer.joueur1 else 2


class WallClassic(Wall):
    def __init__(self, positions, owner):
        super().__init__(positions, owner)

    def getItemType(self):
        return EnumWall.classic
    def getLetter(self):
        return "C"

class WallSolid(Wall):
    def __init__(self, positions, owner):
        super().__init__(positions, owner)
    def getItemType(self):
        return EnumWall.solid
    def getLetter(self):
        return "S"

class WallLong(Wall):
    def __init__(self, positions, owner):
        super().__init__(positions, owner, 4)
    def getItemType(self):
        return EnumWall.long
    def getLetter(self):
        return "L"

class WallDoor(Wall):
    def __init__(self, positions, owner):
        super().__init__(positions, owner)
    def getItemType(self):
        return EnumWall.door
    def getLetter(self):
        return "D"

