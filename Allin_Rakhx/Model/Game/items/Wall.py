from Allin_Rakhx.Model.Game.EnumCase import EnumPlayer, EnumWall
from Allin_Rakhx.Model.Game.items.Item import Item
from Allin_Rakhx.Model.Config import *
import abc

class Wall(Item, abc.ABC):
    def __init__(self, positions, owner, taille=2):
        super().__init__(positions)
        # taille de base
        self.taille = taille
        self.owner = owner
        self.number = 1 if owner.player == EnumPlayer.joueur1 else 2

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

class WallTemp(Wall):
    def __init__(self, positions, owner):
        super().__init__(positions, owner)
        self.timeRemaining = wallTempLifetime
    def getItemType(self):
        return EnumWall.temp
    def getLetter(self):
        return "T"

    def isTimeToRemove(self):
        self.timeRemaining -= 1
        if(self.timeRemaining <= 0):
            return True
        return False

