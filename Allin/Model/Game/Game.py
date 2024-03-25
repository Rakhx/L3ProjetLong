from typing import List, Dict

from Allin.Exception.Exceptions import WallInitListException, CaseOccupedException, CaseWrongTypeException, \
    WallDisponibilityException, WallIntersectionException
from Allin.Model.Game.EnumCase import EnumPion, EnumPlayer, EnumWall, EnumTypeCase, EnumOrientation
from Allin.Model.Game.Plateau import Plateau, isCaseForType
from Allin.Model.Game.Player import Player
import Allin.Model.Config as cf

# Classe de moteur de jeu

class Game :
    def __init__(self):
        self.numPlayer = 0
        self.kvPlayersByName = {}
        self.kvPlayersByNum = {}
        self.__plateau = Plateau(cf.taillePlateau)

    def getBoardState(self):
        return self.__plateau.getAsciiRepresentation()

    # --------------------------------------
    #   region Initialisation de début de game
    # --------------------------------------

    # Ajoute un joueur a la partie, avec son nom et le pion choisi.
    def addPlayer(self, name:str, pion:int):
        self.numPlayer+=1
        joueur = Player(EnumPlayer(self.numPlayer), name, EnumPion(pion))
        self.kvPlayersByName[name] = joueur
        self.kvPlayersByNum[self.numPlayer] = joueur
        # positionner le pion du joueur
        lePion = joueur.spawn
        self.__plateau.putItem(lePion, lePion.position)
        return ("joueur " + name + " enregistré avec un pion " + str(joueur.spawn) + " en joueur numero " + joueur.player.name)

    # Donne les murs choisit par le joueur
    def initWallsList(self, playerName, murs:Dict[int,int]):
        kvMurQuantity = {}
        totalCout = 0

        for key, value in murs.items():
            totalCout += cf.kvMurEtCout.get(key)*value
            kvMurQuantity[EnumWall(key)] = value

        if totalCout > cf.nbrPointAchatMur:
            raise WallInitListException("[Game.addWalls]")

        self.kvPlayersByName[playerName].setWalls(kvMurQuantity)
        res = "Joueur "+ playerName + "enregistre \n"
        for k, v in murs.items():
            res += "quantite de mur " + str(EnumWall(int(k))) + " : " + str(v) + "\n"
        return res

    # Retourne le pion pris par l'autre équipe
    def askSpawnTaken(self, playerName):
        for key,value in self.kvPlayersByName.items():
            if key != playerName:
                return value.spawn.number

    def askWallsTaken(self, playerName):
        for key, value in self.kvPlayersByName.items():
            if key != playerName:
                return value.walls.copy()

    # endregion

    # --------------------------------------
    # region fonction de boucle
    # --------------------------------------

    def deplacementUnite(self, team, posX, posY):
        try :
            player = self.kvPlayersByName[team]
            pion = player.spawn
            oldPosition = player.positionPion
            newPosition = (posX, posY)
            self.__plateau.moveItem(pion, oldPosition, newPosition )
            player.moveSpawn(newPosition)
        except CaseOccupedException :
            return "Not Moved, already occuped"
        except CaseWrongTypeException :
            return "Not Moved, destination n'a pas le bon type de case pour le mouvement"
        except Exception as e:
            return "DeplacementUnit, autre type de probleme " + e.__str__()

        return "ok"

    def placerMur(self, mur, pos, orientation, team):

        try :
            player = self.kvPlayersByName[team]

            # Mur dispo ?
            player.isWallAvailable(mur)
            # Case du bon type pour mettre un mur ?
            if not isCaseForType(EnumTypeCase.forNothing,pos):
                raise CaseWrongTypeException("[Game.placerMur]")
            # Case dispo ?
            if not self.__plateau.isCaseAvailable(pos) :
                raise CaseOccupedException("[Game.placerMur]")
            # intersection ?

            # Si tout est ok, on y va
            self.__plateau.putWall(mur, pos, orientation, player)


        except WallDisponibilityException:
            print("WallDisponibilityException BEBE")
        except CaseWrongTypeException:
            print("CaseWrongTypeException BEBE")
        except CaseOccupedException:
            print("CaseOccupedException BEBE")
        except WallIntersectionException:
            print("WallIntersectionException BEBE")


        print(player.walls)

    def usePower(self, team, posX, posY):
        None


    # endregion

gamou = Game()
print(gamou.addPlayer("zozo", EnumPion.sappeur.value))
print(gamou.addPlayer("zinzin", EnumPion.jumper.value))
#
walls1 = {0:2,1:1,2:1,3:1}
walls2 = {0:1,1:1,2:1,3:1}
print(gamou.initWallsList("zozo", walls1))
gamou.placerMur(EnumWall.classic,(1,1),EnumOrientation.droite,"zozo")
gamou.placerMur(EnumWall.classic,(3,1),EnumOrientation.droite,"zozo")
gamou.placerMur(EnumWall.classic,(5,1),EnumOrientation.droite,"zozo")


# gamou.initWallsList("zinzin", walls2)
print(gamou.getBoardState())

