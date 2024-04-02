import Allin_Rakhx.Model.Config as cf
from Allin_Rakhx.Exception.Exceptions import WallDisponibilityException
from Allin_Rakhx.Model.Game.items.Spawn import Spawn


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

    # Utilise un mur, s'il existe dans la kv, l'en retire.
    def useWall(self, enumWallToUse):
        try :
            nbWallAvailable = self.walls[enumWallToUse]
            if(nbWallAvailable == 1):
                del self.walls[enumWallToUse]
            else :
                nbWall = nbWallAvailable - 1
                self.walls[enumWallToUse] = nbWall

        except BaseException as e:
            print("probleme usewall", repr(e))

    def moveSpawn(self, newPosition):
        self.positionPion = newPosition

    def beginTurn(self):
        self.spawn.reloadPower()


    # fonction qui met a jour le tps de reload des pouvoirs ainsi que les mur temporaire
    # utilise une instance d'un mur donné
    def isWallAvailable(self, enumWalLToCheck):
        if(cf.debugWall):
            print(" murs disponibles pour joueur ", self.player , " : ", self.walls)
            print(" type de mur demande ", enumWalLToCheck)

        if enumWalLToCheck in self.walls :
            # self.walls.remove(murUtilise)
            return True
        else :
            raise WallDisponibilityException("[Player.isWallAvailable]")


