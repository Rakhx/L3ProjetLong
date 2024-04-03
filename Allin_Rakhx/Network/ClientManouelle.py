import json
import time

import requests
from multiprocessing import Process
from Allin_Rakhx.Network.ClientFlask import Client
from Allin_Rakhx.Model.Config import *
from Allin_Rakhx.Model.Config import *

team1 = "john"
wallz1= {0:1,1:1,2:1,3:1,4:1}
team2 = "Fanfan"
wallz2= {0:1,1:0,2:2,3:2,4:1}
nbTour = 2

# Fonction appelée par deux threads
def boucleJeuJ1():

    client1 = Client(team1)
    client1.registerTeam(2)

    # print("boucleJeuJ1 demande le spawn en face ", client1.askOtherSpawn())

    client1.choixMur(wallz1)

    # client1.askOtherWalls()

    boardState = ""
    # on va faire X tour de jeu
    for i in range(nbTour):
        # if debugManuel:
        #     print("[simu]- demande de priorité pour la team "+ client1.getTeamName())
        boardState = client1.newTurn()
        if debugManuel:
            print("client " + client1.getTeamName() + " affiche l'état du jeu suivant" )
            print(boardState)
        if(debugManuel):
            print ( "tour ",i," , " ,client1.getTeamName())


        if i == 0 :
            if debugManuel:
                print ("placement de mur en 15 9")
            client1.placementMur(EnumWall.temp.value, 7,9, EnumOrientation.gauche.value)

        elif i == 1:
            if debugManuel:
                print("deplacement ")
            posActuel = posDepartJ1
            client1.deplacement(posActuel[0], posActuel[1] + 2)

        elif i == 2:
            None
        elif i == 3:
            None

        elif i == 4:
            None

        elif i == 5:
            None

        print("[simu]- fin de boucle pour " + client1.getTeamName())

    client1.disconnection()

# Fonction appelée par deux threads
def boucleJeuJ2():
    client2 = Client(team2)
    client2.registerTeam(1)

    # print("boucleJeuJ1 demande le spawn en face ", client2.askOtherSpawn())

    # client2.askOtherSpawn()

    client2.choixMur(wallz2)

    # client2.askOtherWalls()


    boardState = ""
    # on va faire X tour de jeu
    for i in range(nbTour):
        # if(debugManuel):
        #     print("[simu]- demande de priorité pour la team "+ client2.getTeamName())
        boardState = client2.newTurn()
        if (debugManuel):
            print("client " + client2.getTeamName() + " affiche l'état du jeu suivant" )
            print(boardState)
        if(debugManuel):
            print ( "tour ",i," , " ,client2.getTeamName())
        if i == 0:
            if debugManuel:
                print("demande d'utilisation de pouvoir")
            posActuel = posDepartJ2
            # print(client2.deplacement(posActuel[0] - 2, posActuel[1]))
            print(client2.utilisationPouvoir(posActuel[0] - 2, posActuel[1]))
        elif i == 1:
            if debugManuel:
                print("demande de placement de mur")
            client2.placementMur(EnumWall.temp.value, 5,5, EnumOrientation.haut.value)

        elif i == 2:
            None

        elif i == 3:
            None

        elif i == 4:
            None

        elif i == 5:
            None

        print("[simu]- fin de boucle pour " + client2.getTeamName())

    client2.disconnection()

if __name__ == "__main__":
    client2 = Client(team2)

    procs=[]
    proc = Process(target=boucleJeuJ1, args=())
    procs.append(proc)
    proc.start()

    proc = Process(target=boucleJeuJ2, args=())
    procs.append(proc)
    proc.start()

    for proc in procs:
        proc.join()

    print("[Simu]- Fin de simulation")
