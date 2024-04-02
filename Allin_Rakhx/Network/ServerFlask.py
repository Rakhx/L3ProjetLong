import json
from threading import Lock
from threading import Thread
from flask import Flask, request
from flask_restful import reqparse

from Allin_Rakhx.Model.Config import viewGui, debug, debugWall
from Allin_Rakhx.Model.Game.EnumCase import EnumPlayer, EnumWall, EnumOrientation
from Allin_Rakhx.Model.Game.Game import Game

from Allin_Rakhx.Vue.ThreaderView import ThreadedView

def display_labyrinth(var):
    view = ThreadedView()
    view.loop(data_lock, var)

data_lock = Lock()

# --------------------------------------
#   Element autre de la classe
# --------------------------------------

app = Flask(__name__)
moteur = Game()
lock = Lock()

parser = reqparse.RequestParser()
parser.add_argument('list', type=list)

land = ["--------------------\n->------------------\n->------------------\n"]
teamWithPrio = EnumPlayer.joueur1
T = Thread(target=display_labyrinth, args=(land,))
if(viewGui):
    T.start()

def modifyValue(representation):
    with data_lock:
        global land
        land[0] = representation
def seeValue():
    with data_lock:
        print(land[0])

def convertToString(value):
    return [tuple(str(x) for x in value)]

# --------------------------------------
#   region Initialisation de début de game
# --------------------------------------

# Register le nom de la team, ainsi que le type de pion choisi
@app.route("/init/registerTeam", methods=['GET'])
def registerTeam():
    arg = request.args.to_dict()
    message = moteur.addPlayer(arg["team"],int(arg["pion"]))
    if debug :
        print("register Team ", arg["team"], "de type: " , arg["pion"], " avec un retour ", message)
    return message

# Renvoi le choix de pion de l'adversaire
@app.route("/init/askSpawnChoice", methods=['GET'])
def askSpawnChoice():
    arg = request.args.to_dict()
    message = moteur.askSpawnTaken(arg["team"])
    if debug:
        print("ask Team ", arg["team"], " pour connaitre le pion en face", message)
    return message

# Renvoi le dictionnaire des choix de mur de l'adversaire
@app.route("/init/askWallsChoice", methods=['GET'])
def askWallsChoice():
    arg = request.args.to_dict()
    message = moteur.askWallsTaken(arg["team"])
    if debug:
        print("ask Team ", arg["team"], " pour connaitre les walls en face", message)
    return message

# Register le nom de la team, ainsi que le type de pion choisi
@app.route("/init/registerWalls", methods=['GET'])
def registerWalls():
    arg = request.args.to_dict()
    player = arg["team"]
    wallz = json.loads(arg["walls"])
    mursCorrect = {}
    # res = ""
    # Le json a converti en char
    for k,v in wallz.items():
        mursCorrect[int(k)] = int(v)
        # if debug :
        #     res += "quantite de mur "+ str(EnumWall(int(k))) + " : " + str(v) + "\n"

    return moteur.initWallsList(player, mursCorrect)
# endregion

# --------------------------------------
#   Boucle en cours de  game
# --------------------------------------

# Deplacement du pion sur une position donnée
# team, posX, posY
@app.route('/loop/move', methods=['GET'])
def deplacementUnite():
    param = request.args.to_dict()
    resultat = moteur.deplacementUnite(param["team"], int(param["posX"]), int(param["posY"]))
    if debugWall:
        print(classTag(), " deplacementUnite result :  ", resultat)
    if isinstance(resultat,str):
        return resultat
    if isinstance(resultat,tuple):
        return convertToString(resultat)

# Placement d'un mur donné pour une team donné
# team, typeMur ,posX, posY, orientation
@app.route('/loop/placeWalls', methods=['GET'])
def placerMur():
    param = request.args.to_dict()
    team = param["team"]
    mur = EnumWall(int(param["typeMur"]))
    pos = (int(param["posX"]), int(param["posY"]))
    orientation = EnumOrientation(int(param["orientation"]))
    if(debugWall):
        print("[ServerFlask]-PlacerMur, parametres: team ", team, " typeMur ", mur, " pos " ,pos, " - ", orientation)
    retour = moteur.placerMur(mur, pos, orientation, team)
    if(debugWall):
        print(classTag(), "PlacerMur et a comme retour ", retour)


    return convertToString(retour)


# Utilisation du pouvoir pour un joueur donnée
# team, posX, posY
@app.route('/loop/usePower', methods=['GET'])
def usePower():
    param = request.args.to_dict()
    team = param["team"]
    pos = (int(param["posX"]), int(param["posY"]))


# --------------------------------------
# region Mutex stuff
# --------------------------------------
@app.route('/loop/askPrio', methods=['GET'])
def getPriority():
    param = request.args.to_dict()
    lock.acquire()
    teamWithPrio = param["team"]
    if debug :
        print("equipe " + param["team"] + " prend la priorite")
    representation = moteur.getBoardState(teamWithPrio)
    modifyValue(representation)
    seeValue()
    return (representation)

@app.route('/loop/releasePrio')
def releasePriority():
    try :
        lock.release()
        if debug:
            print("equipe ", teamWithPrio," release la priorite")
        return str(True)
    except RuntimeError :
        return "Release quelque chose de déjà release"

# endregion

def classTag():
    return "[ServerFlask]- "