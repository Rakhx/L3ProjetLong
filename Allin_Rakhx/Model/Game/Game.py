from typing import Dict

from Allin_Rakhx.Exception.Exceptions import WallInitListException, CaseOccupedException, CaseWrongTypeException, \
    WallDisponibilityException, WallIntersectionException
from Allin_Rakhx.Model.Game.EnumCase import EnumPion, EnumPlayer, EnumWall, EnumTypeCase, EnumOrientation
from Allin_Rakhx.Model.Game.Plateau import Plateau, isCaseForType
from Allin_Rakhx.Model.Game.Player import Player
import Allin_Rakhx.Model.Config as cf

# Classe de moteur de jeu

class Game :
    def __init__(self):
        self.numPlayer = 0
        self.kvPlayersByName = {}
        self.kvPlayersByNum = {}
        self.__plateau = Plateau(cf.taillePlateau)

    def getBoardState(self, teamAsking):
        player = self.kvPlayersByName[teamAsking]
        player.beginTurn()
        self.__plateau.newTurn()
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
        self.__plateau.putItem(lePion, lePion.positions)
        return ("joueur " + name + " enregistré avec un pion " + str(joueur.spawn) + " en joueur numero " + joueur.player.name)

    # Donne les murs choisit par le joueur
    def initWallsList(self, playerName, murs:Dict[EnumWall,int]):
        kvMurQuantity = {}
        totalCout = 0

        for key, value in murs.items():
            totalCout += cf.kvMurEtCout.get(key)*value
            kvMurQuantity[EnumWall(key)] = value

        if totalCout > cf.nbrPointAchatMur:
            raise WallInitListException("[Game.addWalls]")

        self.kvPlayersByName[playerName].setWalls(kvMurQuantity)
        res = "Joueur "+ playerName + " enregistre \n"
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

    def askSpawnForTeam(self, playerName):
        player = self.kvPlayersByName[playerName]
        return player.spawn

    # endregion

    # --------------------------------------
    # region fonction de boucle
    # --------------------------------------

    def deplacementUnite(self, team, posX, posY, enumPowerType = None):
        try :
            deepth = 1
            player = self.kvPlayersByName[team]
            pion = player.spawn
            oldPosition = player.positionPion
            newPosition = (posX, posY)
            # Verification que le chemin existe depuis la position source
            setCases = set()
            if enumPowerType == EnumPion.sprinter:
                deepth = 2

            if not self.__plateau.getCasesReachable(setCases,oldPosition, deepth, enumPowerType) :
                return "Not moved, case pas atteignable pour l'unité"


            self.__plateau.moveItem(pion, oldPosition, newPosition )
            player.moveSpawn(newPosition)
        except CaseOccupedException :
            return "Except: DeplacementUnite- Not Moved, already occuped"
        except CaseWrongTypeException :
            return "Except: DeplacementUnite- Not Moved, destination n'a pas le bon type de case pour le mouvement"
        except Exception as e:
            return "Except: DeplacementUnite- autre type d'exception " + e.__str__()

        return newPosition

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

        print(self.classTag(), "suite au placement du mur" , player.walls)
        return "ok"

    def usePower(self, team, posX, posY):
        return self.deplacementUnite(team, posX, posY, self.kvPlayersByName[team].spawn)

    def classTag(self):
        return "[Game]- "

    def getCaseReachable(self, posDepart, enumPowerType = None):
        possibilite = set()
        self.__plateau.getCasesReachable(possibilite, posDepart, 1)
        print(possibilite)

    # endregion
if __name__ == '__main__' :
    gamou = Game()
    print(gamou.addPlayer("zozo", EnumPion.sappeur.value))
    print(gamou.addPlayer("zinzin", EnumPion.jumper.value))
    #
    walls1 = {0:2,1:1,2:1,3:1, 4:1}
    walls2 = {0:1,1:1,2:1,3:1, 4:1}
    print(gamou.initWallsList("zozo", walls1))
    print(gamou.initWallsList("zinzin", walls2))

    # print(gamou.askSpawnTaken("zozo"))
    # print(gamou.askSpawnTaken("zinzin"))
    # print(gamou.askWallsTaken("zinzin"))
    # print(gamou.askWallsTaken("zozo"))

    gamou.placerMur(EnumWall.classic,(1,1),EnumOrientation.droite,"zozo")
    gamou.placerMur(EnumWall.classic,(3,1),EnumOrientation.droite,"zozo")
    # gamou.placerMur(EnumWall.classic,(5,1),EnumOrientation.droite,"zozo")


    # gamou.initWallsList("zinzin", walls2)
    print(gamou.getBoardState("zinzin"))

    # gamou.getCaseReachable((4,4))
    gamou.getCaseReachable((8,8))
    # gamou.getCaseReachable((16,16))
