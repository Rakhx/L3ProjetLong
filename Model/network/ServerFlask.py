from threading import Lock
from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse
import tkinter as tk
from tkinter import *
from threading import Thread
import Model.Config as cg
from Model.Game.EnumCase import EnumPlayer
from Model.Game.Game import Game
from Vue.ThreaderView import ThreadedView


def display_labyrinth(var):
    view = ThreadedView()
    view.loop(data_lock, var)

data_lock = Lock()

# --------------------------------------
#   Element autre de la classe
# --------------------------------------

app = Flask("hum")
moteur = Game()
lock = Lock()

land = ["--------------------\n->------------------\n->------------------\n"]
teamWithPrio = EnumPlayer.joueur1
T = Thread(target=display_labyrinth, args=(land,))
if(cg.viewGui):
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
#   Initialisation de début de game
# --------------------------------------

# Register le nom de la team, ainsi que le type de pion choisi
@app.route("/init/register", methods=['GET'])
def registerTeam():
    arg = request.args.to_dict()
    message = moteur.addPlayer(arg["team"],int(arg["pion"]))
    if cg.debug :
        print("register Team ", arg["name"], "de type: " , arg["pion"], " avec un retour ", message)

    return message

# # Taille du terrain
# @app.route("/init/land")
# def getTailleTerrain():
#     return [tuple(str(x) for x in moteur.getTailleMap())]

# Unités disponibles pour préparation
@app.route("/init/units")
def getAvailableUnit():
    return moteur.getStartUnite()



@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'

# --------------------------------------
#   Boucle en cours de  game
# --------------------------------------

# regarde autour
@app.route('/loop/lookAround', methods=['GET'])
def regarderAutour():
    param =  request.args.to_dict()
    # return [tuple(str(x) for x in moteur.regardeAutour(param["team"],param["unitName"]))]
    return moteur.regardeAutour(param["team"],param["unitName"])

@app.route('/loop/move', methods=['GET'])
def deplacementUnite():
    param = request.args.to_dict()
    return moteur.deplacementUnite(param["team"],param["unitName"], (int(param["posX"]), int(param["posY"])))

@app.route('/loop/shoot', methods=['GET'])
def tirer():
    param = request.args.to_dict()
    return moteur.shoot(param["team"], param["unitName"], (int(param["posX"]), int(param["posY"])))

# --------------------------------------
# Mutex stuff
# --------------------------------------
@app.route('/loop/askPrio', methods=['GET'])
def getPriority():
    param = request.args.to_dict()
    lock.acquire()
    teamWithPrio = param["team"]
    if cg.debug :
        print("equipe " + param["team"] + " prend la priorite")
    # TODO checker ici
    representation = moteur.displayLand()
    modifyValue(representation)
    seeValue()
    return moteur.sumupSituation(param["team"])

@app.route('/loop/releasePrio')
def releasePriority():
    try :
        lock.release()
        if cg.debug:
            print("equipe ", teamWithPrio," release la priorite")
        return str(True)
    except RuntimeError :
        return "Release quelque chose de déjà release"

