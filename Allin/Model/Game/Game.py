from typing import List
from Allin.Model.Game.EnumCase import EnumPion, EnumPlayer
from Allin.Model.Game.Player import Player


# Classe de moteur de jeu

class Game :
    def __init__(self):
        self.numPlayer = -1
        self.playersByName = {}
        self.playersByNum = {}


    # Ajoute un joueur a la partie, avec son nom et le pion choisi.
    def addPlayer(self, name:str, pion:int):
        self.numPlayer+=1
        joueur = Player(EnumPlayer(self.numPlayer), name, EnumPion(pion))
        self.playersByName[name] =  joueur
        self.playersByNum[self.numPlayer] =  joueur
        return ("joueur " + name + " enregistré avec un pion " + EnumPion(pion).__str__() + " en joueur numero " + str(EnumPlayer(self.numPlayer)))


    # Donne les murs choisit par le joueur
    def addWalls(self, playerName ,murs:List[int]):
        self.playersByName[playerName].setWalls(murs)
