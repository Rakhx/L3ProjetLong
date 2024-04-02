import json
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
    # print(client1.choixMur(wallz1))
    client1.choixMur(wallz1)

    boardState = ""
    # on va faire X tour de jeu
    for i in range(nbTour):
        print("[simu]- demande de priorité pour la team "+ client1.getTeamName())
        boardState = client1.newTurn()
        print("client " + client1.getTeamName() + " affiche l'état du jeu suivant" )
        print(boardState)
        if i == 0 :
            client1.placementMur(EnumWall.temp.value, 1,1, EnumOrientation.droite.value)

        elif i == 1:
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
    client2.registerTeam(2)
    client2.choixMur(wallz2)

    boardState = ""
    # on va faire X tour de jeu
    for i in range(nbTour):
        print("[simu]- demande de priorité pour la team "+ client2.getTeamName())
        boardState = client2.newTurn()
        print("client " + client2.getTeamName() + " affiche l'état du jeu suivant" )
        print(boardState)
        if i == 0:
            posActuel = posDepartJ2
            print(client2.deplacement(posActuel[0] - 2, posActuel[1]))
        elif i == 1:
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
