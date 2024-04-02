import typing
from typing import List
import time
import numpy as np

import json
import time
import requests
from typing import Dict


# taille de la carte
tailleMap = 11
matriceVide = np.zeros((tailleMap*2-1, tailleMap*2-1))
# Argent de début pour acheter murs
nbrPointAchatMur = 15

# Argent de début pour acheter murs
nbrPointAchatMur = 15

# LES MURS
# Voir document Excel
# 0 Classic 1 Solid 2 Long 3 Door 4 Tempory

#couple type de mur et cout de ce mur
kvMurEtCout = {0:1, 1:2, 2:3, 3:3}

# LES MURS
# Voir document Excel
# 0 Classic 1 Solid 2 Long 3 Door

#couple type de mur et cout de ce mur
murEtCout = {0:1,1:2,2:3,3:3}

class Client:

    def __init__(self, teamName:str):
        self._name = teamName


    # --------------------------------------
    #  region Initialisation de début de game
    # --------------------------------------

    # enregistre l'équipe auprès du serveur, avec un nom d'équipe et un type de pion
    # type de pion 0:pionSappeur, 1:pion Jumper, 2:pion sprinter
    def registerTeam(self, pionChoisi:int):
        return "ok"

    # choisi un ensemble de mur pour commencer la partie
    # error 0: trop cher en point
    # Version locale de ce qui se fera sur le serveur
    def choixMur(self, murs:Dict[int,int]):
        totalCout = 0
        try :
            for mur in murs :
                totalCout += kvMurEtCout.get(mur)
            if totalCout > nbrPointAchatMur :
                print("[ClientFlask] - ChoixMur: " + str(murs))
        except ValueError:
            print("mur n'existe pas dans la liste des murs dispos")

        return "ok"

   # demande quel pion a été choisi
    def askOtherSpawn(self):
        return 0

   # demande quel mur a été choisi
    def askOtherWalls(self):
        return {0:3,1:3,2:1,3:1}

    # endregion

    # --------------------------------------
    # region gestion des priorités
    # --------------------------------------

    def __askPriority(self):
        # received = json.loads(r.text)
        # Doit retourner l'état du board.
        # test = tuple(i for i in received)
        # return test
        return "ok"

    def __releasePriority(self):
        None
    # fonction à appeler dans le while
    def newTurn(self):

        return []

    def disconnection(self):
        self.__releasePriority()

    # endregion

    # --------------------------------------
    # region fonction de boucle
    # --------------------------------------

    # return 0 si s'est bien passé
    # Code erreur  1:, 2:obstacle mur, 3:sortie de terrain, 10:mauvais input
    def deplacement(self, positionX:int, positionY:int):
        return True

    # Orientation : 0 : vers le haut, 1 vers la droite, 2 vers le bas, 3 vers la gauche
    # type mur : 0:mur incassable 1:mur long 2:mur réutilisable 3:murTemporaire 4:mur "porte"
    # return 0 si ok
    # Code erreur : 1:mur sort map, 2:mur croise autre mur, 3:mur enferme joueur 4:mur non disponible 10:mauvais input
    def placementMur(self, typeMur:int, positionX:int, positionY:int, orientation:int):
        return True


    # utilisation du pouvoir de l'unité
    # Sauter par dessus
    # return 0 si ok
    # code erreur 1:pouvoir en rechargement  10:mauvais input
    def utilisationPouvoir(self, positionX:int, positionY:int):
        return True

    # endregion

    # --------------------------------------
    # region Autres
    # --------------------------------------
    def posString(self, pos):
        return "&posX=" + str(pos[0]) + "&posY=" + str(pos[1])

    def getTeamName(self):
        return self._name

    # endregion
