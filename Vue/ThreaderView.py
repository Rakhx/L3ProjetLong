from tkinter import *
import tkinter as tk
import time

# Vue qui va être utilisée dans un thread à part pour l'affichage côté serveur
class ThreadedView():
    def __init__(self):
        print("Call once")
        self.root = Tk()
        self._canvas2 = Canvas(self.root, width=200, height=500, bg="#FFFFFF")
        self._canvas2.grid(row = 0, column = 0)
        self._canvas = Canvas(self.root, width=1000, height=500, bg="#000000")
        self._canvas.grid(row = 0, column = 1)
        # self.img = PhotoImage(width=1000, height=500)
        # self._canvas.create_image((1000, 500), image=self.img, state="normal")
        self.cpt = 0
        self._offset = 10
        self._correspondanceColor = {}
        self.createCorrespondance()
        self.drawEnonce()

    def loop(self, data_lock, var):
        while True:
            time.sleep(2)
            self._canvas.delete()
            with data_lock:
                self.displayLabyrinthe(var)

            self.root.update()

    def displayLabyrinthe(self, var):
        print(var[0])
        self.draw("r", 10, 10)


    def draw(self, char, x, y):
        if char == '-': # case vide - blanc
            self._canvas.create_rectangle(x, y, x + self._offset, y + self._offset, fill="#FFFFFF")
        if char == 'O': # Obstacle - noir
            self._canvas.create_rectangle(x, y, x + self._offset, y + self._offset, fill="#000000")
        if char == 'A': # Artilleur rose
            self._canvas.create_rectangle(x, y, x + self._offset, y + self._offset, fill="#800080")
        if char == 'a': # Artilleur vert
            self._canvas.create_rectangle(x, y, x + self._offset, y + self._offset, fill="#008000")
        if char == 'M': # Marines fuccia
            self._canvas.create_rectangle(x, y, x + self._offset, y + self._offset, fill="#FF00FF")
        if char == 'm': # Marines fuccia
            self._canvas.create_rectangle(x, y, x + self._offset, y + self._offset, fill="#808000")
        if char == 'E':
            self._canvas.create_rectangle(x, y, x + self._offset, y + self._offset, fill="#000000")
        if char == 'B':
            self._canvas.create_rectangle(x, y, x + self._offset, y + self._offset, fill="#FFFF00")
        if char == 'F': # Flag, rouge
            self._canvas.create_rectangle(x, y, x + self._offset, y + self._offset, fill="#FF0000")


    def createCorrespondance(self):
        self._correspondanceColor['F'] = "#FF0000"
        self._correspondanceColor['O'] = "#000000"
        self._correspondanceColor['M'] = "#FF00FF"
        self._correspondanceColor['m'] = "#808000"

    def drawEnonce(self):
        x = 0
        y = 0
        for key in self._correspondanceColor:
            self._canvas2.create_rectangle(x, y, x + self._offset, y + self._offset, fill=self._correspondanceColor[key])
            label = Label(self._canvas2, text=key)
            label.place(relx = 0+ self._offset, rely = 0)
            x = 0
            y = y + self._offset

