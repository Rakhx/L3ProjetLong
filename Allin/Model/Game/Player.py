import Allin.Model.Config as cf
import typing

from Allin.Exception.Exceptions import WallDisponibilityException


class Player:
    def __init__(self, enumJoueur, nom:str, pion):
        self.walls = []
        self.name = nom
        self.player = enumJoueur
        # pas sur de vouloir cette info ici
        # deux positions possible pour le pions
        pos1 = (0, (cf.taillePlateau-1) / 2 )
        pos2 = (cf.taillePlateau*2-1 , (cf.taillePlateau-1) / 2 )
        pos = (cf.taillePlateau*2-1 * enumJoueur.value , (cf.taillePlateau-1) / 2 )
        self.positionPion = pos
        self.spawn = pion

    def setWalls(self, murs):
        self.walls = murs


    # utilise une instance d'un mur donné
    def isWallAvailable(self, murUtilise:int):
        if murUtilise in self.walls :
            # self.walls.remove(murUtilise)
            return True
        else :
            raise WallDisponibilityException("[Player.isWallAvailable]")

    def moveSpawn(self, newPosition):
        self.positionPion = newPosition