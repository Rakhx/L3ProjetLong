import json
import time
import requests
from typing import List
import Allin.Model.Config as cf
class Client:

    def __init__(self, teamName:str):
        self._name = teamName

        # # Position de départ
        # r = requests.get("http://127.0.0.1:5000/init/register/" + teamName)
        # received = json.loads(r.text)
        # self._startPosition = tuple(int(i) for i in received[0])
        # # Taille du terrain
        # r = requests.get("http://127.0.0.1:5000/init/land")
        # received = json.loads(r.text)
        # self._tailleLand = tuple(int(i) for i in received[0])
        # # Liste d'unités disponibles
        # r = requests.get("http://127.0.0.1:5000/init/units")
        # received = json.loads(r.text)
        # self._unitDispos = tuple(i for i in received)

    # --------------------------------------
    #   Initialisation de début de game
    # --------------------------------------

    # enregistre l'équipe auprès du serveur, avec un nom d'équipe et un type de pion
    # type de pion 0:pionSappeur, 1:pion Jumper, 2:pion sprinter
    def registerTeam(self, pionChoisi:int):
        r = requests.get("http://127.0.0.1:5000/init/register?team=" + self._name + "&pion=" + str(pionChoisi))
        return r.text

    # choisi un ensemble de mur pour commencer la partie
    # error 0: trop cher en point
    # Version locale de ce qui se fera sur le serveur
    def choixMur(self, murs:List[int]):
        totalCout = 0
        try :
            for mur in murs :
                totalCout += cf.murEtCout.get(mur)
        except ValueError:
            print("mur n'existe pas dans la liste des murs dispos")

        # a voir avec l'histoire d'utiliser une liste
        # https://stackoverflow.com/questions/65778471/how-to-pass-a-list-as-an-argument-when-using-restful-api-and-flask
        r = requests.get("http://127.0.0.1:5000/init/register?wall=" + self._name)

        return r.text

    # --------------------------------------
    #   Boucle en cours de  game
    # --------------------------------------

    def __askPriority(self):
        r = requests.get("http://127.0.0.1:5000/loop/askPrio?team=" + self._name)
        received = json.loads(r.text)
        test = tuple(i for i in received)
        return test

    def __releasePriority(self):
        r = requests.get("http://127.0.0.1:5000/loop/releasePrio")
        return r.text

    # fonction à appeler dans le while
    def newTurn(self):
        self.__releasePriority()
        time.sleep(1)
        boardState = self.__askPriority()
        return boardState

    # return 0 si s'est bien passé
    # Code erreur  1:, 2:obstacle mur, 3:sortie de terrain, 10:mauvais input
    def deplacement(self, positionX:int, positionY:int):
        if not isinstance(positionX, int) or not isinstance(positionY, int):
            raise TypeError()

        position = (positionX, positionY)

        r = requests.get("http://127.0.0.1:5000/loop/moving?team=" + self._name + self.posString(position))
        return r.text

    # Orientation : 0 : vers le haut, 1 vers la droite, 2 vers le bas, 3 vers la gauche
    # type mur : 0:mur incassable 1:mur long 2:mur réutilisable 3:murTemporaire 4:mur "porte"
    # return 0 si ok
    # Code erreur : 1:mur sort map, 2:mur croise autre mur, 3:mur enferme joueur 4:mur non disponible 10:mauvais input
    def placementMur(self, typeMur:int, positionX:int, positionY:int, orientation:int):
        position = (positionX, positionY)

        r = requests.get("http://127.0.0.1:5000/loop/lookAround?team=" + self._name + "&typeMur=" + str(typeMur)
                         + self.posString(position)+"&orientation=" + str(orientation))
        received = json.loads(r.text)
        tuple(i for i in received)
        #TODO


    # utilisation du pouvoir de l'unité
    # Sauter par dessus
    # return 0 si ok
    # code erreur 1:pouvoir en rechargement  10:mauvais input
    def utilisationPouvoir(self, positionX:int, positionY:int):
        if not isinstance(positionX, int) or not isinstance(positionY, int):
            raise TypeError()

        position = (positionX, positionY)

        r = requests.get("http://127.0.0.1:5000/loop/moving?team=" + self._name + self.posString(position))
        return r.text



    # --------------------------------------
    #   Autres
    # --------------------------------------
    def posString(self, pos):
        return "&posX=" + str(pos[0]) + "&posY=" + str(pos[1])