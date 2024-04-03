import json
import time
import flask
import requests
from typing import Dict
from Allin_Rakhx.Model.Config import *
import Allin_Rakhx.Model.Config as cf

from Allin_Rakhx.Exception.Exceptions import *
class Client:

    def __init__(self, teamName:str):
        self._name = teamName

    # --------------------------------------
    #  region Initialisation de début de game
    # --------------------------------------

    # enregistre l'équipe auprès du serveur, avec un nom d'équipe et un type de pion
    # type de pion 0:pionSappeur, 1:pion Jumper, 2:pion sprinter
    def registerTeam(self, pionChoisi:int):
        r = requests.get(adresseServeur + "/init/registerTeam?team=" + self._name + "&pion=" + str(pionChoisi))
        return r.text

    # choisi un ensemble de mur pour commencer la partie
    # error 0: trop cher en point
    # Version locale de ce qui se fera sur le serveur
    def choixMur(self, murs:Dict[int,int]):
        totalCout = 0
        try :
            for mur in murs :
                totalCout += cf.kvMurEtCout.get(mur)
            if totalCout > cf.nbrPointAchatMur :
                raise WallInitListException("[ClientFlask] - ChoixMur: " + str(murs))
        except ValueError:
            print("mur n'existe pas dans la liste des murs dispos")

        # a voir avec l'histoire d'utiliser une liste
        # https://stackoverflow.com/questions/65778471/how-to-pass-a-list-as-an-argument-when-using-restful-api-and-flask
        r = requests.get(adresseServeur+"/init/registerWalls?team="+ self._name +"&walls=" + json.dumps(murs) )
        return r.text

   # demande quel pion a été choisi
    def askOtherSpawn(self):
        r = requests.get(adresseServeur+"/init/askSpawnChoice?team="+ self._name)
        return r.text

   # demande quel mur a été choisi
    def askOtherWalls(self):
        r = requests.get(adresseServeur+"/init/askWallsChoice?team=" + self._name)

        if cf.debug :
            print("demande des autres murs", r.text)
        return r.text

    # endregion

    # --------------------------------------
    # region gestion des priorités
    # --------------------------------------

    # fonction à appeler dans le while
    def newTurn(self):
        self.__releasePriority()
        time.sleep(1)
        boardState = self.__askPriority()
        return boardState

    def __askPriority(self):
        r = requests.get(adresseServeur+"/loop/askPrio?team=" + self._name)
        return r.text

    def __releasePriority(self):
        r = requests.get(adresseServeur+"/loop/releasePrio")
        return r.text

    def disconnection(self):
        self.__releasePriority()

    # endregion

    # --------------------------------------
    # region fonction de boucle
    # --------------------------------------

    # return 0 si s'est bien passé
    # Code erreur  1:, 2:obstacle mur, 3:sortie de terrain, 10:mauvais input
    def deplacement(self, positionX:int, positionY:int):
        position = (positionX, positionY)
        r = requests.get(adresseServeur+"/loop/move?team=" + self._name + self.posString(position))

        return r.text

    # Orientation : 0 : vers le haut, 1 vers la droite, 2 vers le bas, 3 vers la gauche
    # type mur : 0:mur incassable 1:mur long 2:mur réutilisable 3:murTemporaire 4:mur "porte"
    # return 0 si ok
    # Code erreur : 1:mur sort map, 2:mur croise autre mur, 3:mur enferme joueur 4:mur non disponible 10:mauvais input
    def placementMur(self, typeMur:int, positionX:int, positionY:int, orientation:int):
        position = (positionX, positionY)
        r = requests.get(adresseServeur+"/loop/placeWalls?team=" + self._name + "&typeMur=" + str(typeMur)
                         + self.posString(position)+"&orientation=" + str(orientation))
        if(debugWall):
            print(r.text)

        return r.text

    # utilisation du pouvoir de l'unité
    # Sauter par dessus
    # return 0 si ok
    # code erreur 1:pouvoir en rechargement  10:mauvais input
    def utilisationPouvoir(self, positionX:int, positionY:int):
        if not isinstance(positionX, int) or not isinstance(positionY, int):
            raise TypeError()
        position = (positionX, positionY)
        r = requests.get(adresseServeur+"/loop/usePower?team=" + self._name + self.posString(position))
        return r.text

    # endregion

    # --------------------------------------
    # region Autres
    # --------------------------------------
    def posString(self, pos):
        return "&posX=" + str(pos[0]) + "&posY=" + str(pos[1])

    def getTeamName(self):
        return self._name

    def fromResponseToString(self, resultRequest):
        resultat = ""
        for i in resultRequest:
            for j in i :
                resultat += j
        return resultat

    def classTag(self):
        return "[ClientFlask]-"
    # endregion
