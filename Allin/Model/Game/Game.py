from typing import List, Dict

from Allin.Exception.Exceptions import WallInitListException, CaseOccupedException, CaseWrongTypeException, \
    WallDisponibilityException, WallIntersectionException
from Allin.Model.Game.EnumCase import EnumPion, EnumPlayer, EnumWall, EnumTypeCase
from Allin.Model.Game.Plateau import Plateau, isCaseForType
from Allin.Model.Game.Player import Player
import Allin.Model.Config as cf

# Classe de moteur de jeu

class Game :
    def __init__(self):
        self.numPlayer = -1
        self.kvPlayersByName = {}
        self.kvPlayersByNum = {}
        self.__plateau = Plateau(cf.taillePlateau)

    def getBoardState(self):
        return self.__plateau.getAsciiRepresentation()

    # Ajoute un joueur a la partie, avec son nom et le pion choisi.
    def addPlayer(self, name:str, pion:int):
        self.numPlayer+=1
        joueur = Player(EnumPlayer(self.numPlayer), name, EnumPion(pion))
        self.kvPlayersByName[name] =  joueur
        self.kvPlayersByNum[self.numPlayer] =  joueur
        return ("joueur " + name + " enregistré avec un pion " + EnumPion(pion).__str__() + " en joueur numero " + str(EnumPlayer(self.numPlayer)))

    # Donne les murs choisit par le joueur
    def initWallsList(self, playerName, murs:Dict[int,int]):
        totalCout = 0
        print(murs)
        for mur in murs:
            totalCout += cf.murEtCout.get(mur)
        if totalCout > cf.nbrPointAchatMur:
            raise WallInitListException("[Game.addWalls]")

        self.kvPlayersByName[playerName].setWalls(murs)
        res = "Joueur "+ playerName + "enregistre \n"
        for k, v in murs.items():
            res += "quantite de mur " + str(EnumWall(int(k))) + " : " + str(v) + "\n"
        return res
        return ""

    def deplacementUnite(self, team, posX, posY):
        try :
            player = self.kvPlayersByName[team]
            oldPosition = player.positionPion
            newPosition = (posX, posY)
            self.__plateau.moveItem(EnumTypeCase.forSpawn, oldPosition, newPosition )
            player.moveSpawn(newPosition)
        except CaseOccupedException :
            return "Not Moved, already occuped"
        except CaseWrongTypeException :
            return "Not Moved, destination n'a pas le bon type de case pour le mouvement"
        except Exception as e:
            return "DeplacementUnit, autre type de probleme " + e.__str__()

        return "ok"

    def placerMur(self, team, mur, posX, posY, orientation):

        try :
            player = self.kvPlayersByName[team]
            pos = (posX, posY)

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
            self.__plateau.placerMur(mur, pos, orientation)


        except WallDisponibilityException:
            None
        except CaseWrongTypeException:
            None
        except CaseOccupedException:
            None
        except WallIntersectionException:
            None



    def usePower(self, team, posX, posY):
        None


gamou = Game()
print(gamou.addPlayer("zozo", EnumPion.sappeur.value))
print(gamou.addPlayer("zinzin", EnumPion.jumper.value))
print(gamou.getBoardState())

