import json
import requests
from multiprocessing import Process
from src.Allin_Rakhx.Network.ClientFlask import Client

team1 = "john"
team2 = "Fanfan"
wallz= {0: 1, 1: 1, 2: 1, 3: 1}
wallz2= {0: 1, 1: 0, 2: 2, 3: 2}
def registerPlayers(team):
    print("Request register player ", team)
    r = requests.get(adresseServeur+"/init/registerTeam?team="+team+"&pion=0")
    print(r.text)

def registerWalls(team, wallz):
    print("Request register walls team", team, wallz, sep=";")
    r = requests.get(adresseServeur+"/init/registerWalls?team="+ team +"&walls=" + json.dumps(wallz) )
    print(r.text)

# Fonction appelée par deux threads
def boucleJeu(client):
    registerPlayers(client.getTeamName())
    registerWalls(client.getTeamName(), wallz)
    boardState = ""
    # on va faire X tour de jeu
    for i in range(3):
        print("demande de priorité pour la team "+ client.getTeamName())
        boardState = client.newTurn()
        print("la team "+ client.getTeamName() + " est en train de travailler fort")
        #time.sleep(2)
        print("fin de boucle pour "+ client.getTeamName())
    client.bye()

if __name__ == "__main__":
    client1 = Client(team1)
    client2 = Client(team2)

    procs=[]
    proc = Process(target=boucleJeu, args=(client1,))
    procs.append(proc)
    proc.start()

    proc = Process(target=boucleJeu, args=(client2,))
    procs.append(proc)
    proc.start()

    for proc in procs:
        proc.join()

    print("finito")
