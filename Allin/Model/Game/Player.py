import Allin.Model.Config as cf
import typing

from Allin.Exception.Exceptions import WallDisponibilityException
from Allin.Model.Game.items.Spawn import Spawn


class Player:
    def __init__(self, enumJoueur, nom:str, enumPion):
        self.walls = {}
        self.name = nom
        self.player = enumJoueur

        # deux positions possible pour le pions
        pos = ( (cf.taillePlateau-1)*2 * (enumJoueur.value-1) , (cf.taillePlateau-1) )
        self.positionPion = pos
        self.spawn = Spawn(pos, enumJoueur, enumPion)


    def setWalls(self, murs):
        self.walls = murs

    def useWall(self, enumWallToUse):
        wallAsNumber = enumWallToUse.value
        try :
            nbWallAvailable = self.walls[wallAsNumber]
            if(nbWallAvailable == 1):
                del self.walls[wallAsNumber]
            else :
                nbWall = nbWallAvailable - 1
                self.walls[wallAsNumber] = nbWall

        except :
            print("probleme usewall")


    # utilise une instance d'un mur donné
    def isWallAvailable(self, enumWalLToCheck):
        if enumWalLToCheck.value in self.walls :
            # self.walls.remove(murUtilise)
            return True
        else :
            raise WallDisponibilityException("[Player.isWallAvailable]")

    def moveSpawn(self, newPosition):
        self.positionPion = newPosition
