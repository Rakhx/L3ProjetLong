from Allin.Model.Game.EnumCase import *


# Taille du plateau en nombre de case
taillePlateau = 9
viewGui = False
debug = True

# Argent de début pour acheter murs
nbrPointAchatMur = 15

# LES MURS
# Voir document Excel
# 0 Classic 1 Solid 2 Long 3 Door 4 Tempory

#couple type de mur et cout de ce mur
kvMurEtCout = {0:1, 1:2, 2:3, 3:3}

# couple de type pion et etemps de rechargement pouvoir
kvPionEtReload = {EnumPion.sappeur:4, EnumPion.jumper:4, EnumPion.sprinter:4}
