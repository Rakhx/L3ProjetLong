from Allin_Rakhx.Network.ClientFlask import Client


# cet exemple regroupe la logique des fichiers main, model et presenter


# PARTIE INITIALISATION

# création d'un objet client qui va permettre de communiquer avec le serveur
client = Client("monEquipe")

# On enregistre le pion qu'on souhaite utiliser. La fonction renvoie 1 ou 2 pour savoir quel joueur on est
#     sappeur = 0
#     jumper = 1
#     sprinter = 2
monNumeroJoueur = client.registerTeam(0)

# on demande au serveur le choix des autres joueurs
choixAdversePion = client.askOtherSpawn()

# on choisit les murs que on veut acheter
murs = {0:5, 1:3,2:1,3:1}
client.choixMur(murs)

# on demande les murs des autres joueurs
choixAdverseMur = client.askOtherWalls()

# PARTIE BOUCLE JEU
finDeParti = False

while not finDeParti :
    # cette fonction va renvoyer une matrice contenant les objets dans chaque case. Voir fichier EnumCase pour voir les correspondances
    # si le plateau renvoyé est vide, il s'agit de la fin de partie
    etatPlateau = client.newTurn()
    if ( etatPlateau == ""):
        finDeParti = True

    # Ici, il vous faudra convertir le plateau recu pour le transformer dans la représentation que vous utilisez en interne dans votre code

    # Ensuite, utilisez vos algorithmes pour déterminer ce que vous souhaitez faire entre vous déplacer, placer un mur ou utiliser un pouvoir
    # les fonctions renvoient True si l'action que vous avez demandée a pu etre réalisée
    choix = ""
    if choix == "deplacement":
        posX = 1
        posY = 9
        resultat = client.deplacement(posX, posY)

    if choix == "utiliserPouvoir":
        posX = 1
        posY = 9
        resultat = client.utilisationPouvoir(posX, posY)

    # Pour le placement de mur, on choisit une case de jonction ( c'est a dire ni mur ni pion), et l'orientation.
    # on place donc les murs sur les emplacements de combinaisons x et y tout les deux impairs
    if choix == "placerMur":
        posX = 1
        posY = 9
        typeMur = 0
        orientation = 2
        resultat = client.placementMur(typeMur, posX, posY, orientation)

    #  Mur : classic = 0
    #     solid = 1
    #     long = 2
    #     door = 3
    # Orientation : haut = 0
    #     droite = 1
    #     bas = 2
    #     gauche = 3

