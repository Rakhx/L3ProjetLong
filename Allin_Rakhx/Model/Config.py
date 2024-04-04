from Allin_Rakhx.Model.Game.EnumCase import *


# Taille du plateau en nombre de case
taillePlateau = 9
viewGui = True
debug = True

debugWall = debug & True
debugMvt = debug & False
debugPower = debug & True
debugManuel = debug & True


posDepartJ1 = (0, taillePlateau - 1)
posDepartJ2 = ((taillePlateau - 1) * 2, taillePlateau - 1)


# Argent de début pour acheter murs
nbrPointAchatMur = 15

# LES MURS
# Voir document Excel
# 0 Classic 1 Solid 2 Long 3 Door 4 Tempory

#couple type de mur et cout de ce mur
kvMurEtCout = {0:1, 1:2, 2:3, 3:3, 4:2}

# nb de tour restant pour le mur temporaire
wallTempLifetime = 3

# couple de type pion et etemps de rechargement pouvoir
kvPionEtReload = {EnumPion.sappeur:4, EnumPion.jumper:4, EnumPion.sprinter:4}



releaseMode = False

adresseServeur = "http://10.2.74.16:5000" if releaseMode else "http://127.0.0.1:5000"