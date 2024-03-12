from Allin.Model.Game.EnumCase import EnumOrientation
from Allin.Model.Game.items.Item import Item


class Wall(Item):
    def __init__(self, pos):
        super().__init__(pos)
        # mur non placé, initialement
        self.placed = False
        # direction de base, nord
        self.direction = EnumOrientation.haut
        # taille de base
        self.taille = 2