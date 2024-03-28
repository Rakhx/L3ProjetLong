from src.Allin_Rakhx.Model.Game.EnumCase import EnumPlayer, EnumPion
from src.Allin_Rakhx.Model.Game.items.Item import Item
import src.Allin_Rakhx.Model.Config as cg
class Spawn(Item):
    def __init__(self, pos, owner, typeAsEnum):
        super().__init__(pos)
        self.owner = owner
        self.number = 1 if owner == EnumPlayer.joueur1 else 2
        self.typeAsEnum = typeAsEnum
        self.reloadTime = cg.kvPionEtReload[typeAsEnum]
        if typeAsEnum == EnumPion.sappeur :
            self.letter = "S"
        elif typeAsEnum == EnumPion.jumper:
            self.letter = "J"
        elif typeAsEnum == EnumPion.sprinter:
            self.letter = "Z"

    def getLetter(self):
        return "P"

    def getName(self):
        return self.typeAsEnum.name

    def getItemType(self):
        return self.typeAsEnum

    def __str__(self):
        return self.typeAsEnum.name


