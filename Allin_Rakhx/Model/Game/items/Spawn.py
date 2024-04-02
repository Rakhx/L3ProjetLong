from Allin_Rakhx.Model.Game.EnumCase import EnumPlayer, EnumPion
from Allin_Rakhx.Model.Game.items.Item import Item
import Allin_Rakhx.Model.Config as cg
class Spawn(Item):
    def __init__(self, pos, owner, typeAsEnum):
        super().__init__(pos)
        self.owner = owner
        self.number = 1 if owner == EnumPlayer.joueur1 else 2
        self.typeAsEnum = typeAsEnum
        self.reloadTime = cg.kvPionEtReload[typeAsEnum]
        self.chargingTime = self.reloadTime
        if typeAsEnum == EnumPion.sappeur :
            self.letter = "S"
        elif typeAsEnum == EnumPion.jumper:
            self.letter = "J"
        elif typeAsEnum == EnumPion.sprinter:
            self.letter = "Z"

    def reloadPower(self):
        if self.chargingTime < self.reloadTime:
            self.chargingTime += 1

    # si le pouvoir est chargé, le décharge et renvoi True
    def usePower(self):
        if(self.chargingTime == self.typeAsEnum):
            self.chargingTime = 0
            return True
        return False

    def getLetter(self):
        return "P"

    def getName(self):
        return self.typeAsEnum.name

    def getItemType(self):
        return self.typeAsEnum

    def __str__(self):
        return self.typeAsEnum.name
