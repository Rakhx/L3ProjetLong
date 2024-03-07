from Model.Game.EnumCase import EnumPlayer, EnumPion


class Player:
    def __init__(self, enumJoueur ,nom, pion):
        self.walls = []
        self.name = nom
        self.player = enumJoueur
        self.positionPion = (0,0)
        self.spawn = pion

    def setWalls(self, murs):
        self.walls = murs


    # utilise une instance d'un mur donné
    def useWall(self, murUtilise:int):
        if murUtilise in self.walls :
            self.walls.remove(murUtilise)
        else :
            return False
        return True

