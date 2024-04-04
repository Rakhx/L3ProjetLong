from tkinter import *
import tkinter as tk
import time
import Allin_Rakhx.Model.Config as cf
# Vue qui va être utilisée dans un thread à part pour l'affichage côté serveur
class ThreadedViewTT():
    def __init__(self):
        self.root = Tk()
        self.dico_canvas = {}
        self.pionx = 20
        self.piony = 20
        self.wallx = 5
        self.wally = 20
        self.canvas = tk.Canvas(self.root, width=self.pionx * cf.taillePlateau * 2 , height=self.pionx * cf.taillePlateau * 2)
        self.canvas.pack(expand=True, fill=tk.BOTH)
        self.canvas.pack()

    def prepare_matrice(self, matrice):
        for row in range(len(matrice)):
            for col in range(len(matrice)):
                # case de pion 
                if row % 2 == 0 and col % 2 == 0:
                    CANVA = self.canvas.create_rectangle((self.pionx + self.piony) * col ,
                                                         (self.pionx + self.piony) * row ,
                                                         (self.pionx + self.piony) * col  + self.pionx,
                                                         (self.pionx + self.piony) * row  + self.piony, fill="white")
                    milieu_x = (self.pionx + self.piony) * col  + self.pionx / 2
                    milieu_y = (self.pionx + self.piony) * row  + self.pionx / 2
                    rayon = self.pionx / 2
                    if matrice[row][col] == 'P1':
                        self.Pion1_canva = self.canvas.create_oval(milieu_x - rayon, milieu_y - rayon, milieu_x + rayon,
                                                                   milieu_y + rayon, fill="red")
                    elif matrice[row][col] == 'P2':
                        self.Pion2_canva = self.canvas.create_oval(milieu_x - rayon, milieu_y - rayon, milieu_x + rayon,
                                                                   milieu_y + rayon, fill="blue")

                # colonne de mur (mur à droite d'un pion)
                elif col % 2 == 1 and row % 2 == 0:

                    if matrice[row][col] != 'mur':  # mur rempli
                        CANVA = self.canvas.create_rectangle(self.pionx + (self.pionx + self.piony) * (col // 2),
                                                             (self.pionx + self.piony) * row / 2,
                                                             self.pionx + (self.pionx + self.piony) * (col // 2) + self.piony,
                                                             (self.pionx + self.piony) * (row / 2) + self.pionx, fill="black")
                    else:
                        CANVA = self.canvas.create_rectangle(self.pionx + (self.pionx + self.piony) * (col // 2),
                                                             (self.pionx + self.piony) * row / 2,
                                                             self.pionx + (self.pionx + self.piony) * (col // 2) + self.piony,
                                                             (self.pionx + self.piony) * (row / 2) + self.pionx, fill="white")
                # ligne de murs, murs au dessus et en dessous d'un pion
                elif row % 2 == 1 and col % 2 == 0:
                    if matrice[row][col] != 'mur':  # mur rempli
                        CANVA = self.canvas.create_rectangle((self.pionx + self.piony) * col / 2,
                                                             self.pionx + (self.pionx + self.piony) * (row // 2),
                                                             (self.pionx + self.piony) * col / 2 + self.pionx,
                                                             self.pionx + (self.pionx + self.piony) * (row // 2) + self.piony,
                                                             fill="black")
                    else:
                        CANVA = self.canvas.create_rectangle((self.pionx + self.piony) * col / 2,
                                                             self.pionx + (self.pionx + self.piony) * (row // 2),
                                                             (self.pionx + self.piony) * col / 2 + self.pionx,
                                                             self.pionx + (self.pionx + self.piony) * (row // 2) + self.piony,
                                                             fill="white")
                # si double impair, case useless
                elif col % 2 == 1 and row % 2 == 1:
                    CANVA = self.canvas.create_rectangle(self.pionx + (self.pionx + self.piony) * (col // 2),
                                                         self.pionx + (self.pionx + self.piony) * (row // 2),
                                                         self.pionx + (self.pionx + self.piony) * (col // 2) + self.piony,
                                                         self.pionx + (self.pionx + self.piony) * (row // 2) + self.piony,
                                                         fill="green")

                self.dico_canvas[(row, col)] = CANVA


    def loop(self, data_lock, var):
        while True:
            time.sleep(2)
            # self._canvas.delete()
            with data_lock:
                self.prepare_matrice(var[0])

            self.root.update()

