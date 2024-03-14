import json
from threading import Lock
from flask import Flask, request
from threading import Thread
from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse


from Allin.Model.Config import viewGui, debug
from Allin.Model.Game.EnumCase import EnumPlayer, EnumWall
from Allin.Model.Game.Game import Game

from Allin.Vue.ThreaderView import ThreadedView


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

@app.route("init/askSpawnChoice")
def askSpawnChoice():

    None

@app.route("init/askWallsChoice")
def askWallsChoice():
    None

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

@app.route('/loop/move', methods=['GET'])
def deplacementUnite():
    param = request.args.to_dict()
    return moteur.deplacementUnite(param["team"], (int(param["posX"]), int(param["posY"])))

@app.route('/loop/placeWalls', methods=['GET'])
def placerMur():
    param = request.args.to_dict()
    team = param["team"]
    pos = (param["posX"], param["posY"])
    orientation = param["orientation"]
    # On vérifie si le joueur possede tjrs ce type de mur

    # on vérifie que la case est disponible pour mettre le mur

    # on vérifie que l'orientation du mur ne le fait pas rentrer en intersection avec un autre

@app.route('/loop/usePower', methods=['GET'])
def usePower():
    param = request.args.to_dict()
    team = param["team"]
    pos = (param["posX"], param["posY"])


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
    # TODO checker ici
    representation = moteur.getBoardState()
    modifyValue(representation)
    seeValue()
    # Reload des pouvoirs
    return representation

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
