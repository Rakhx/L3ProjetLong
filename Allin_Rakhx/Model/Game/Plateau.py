from Allin_Rakhx.Exception.Exceptions import CaseOccupedException, CaseEmptyException, CaseWrongTypeException, \
    WallIntersectionException
from Allin_Rakhx.Model.Game.EnumCase import EnumCase, EnumTypeCase, EnumWall, EnumOrientation, EnumPion
import Allin_Rakhx.Model.Config as cg
from Allin_Rakhx.Model.Game.items.Wall import WallDoor, WallSolid, WallClassic, WallLong, Wall, WallTemp

class Plateau:

    # struture interne, dictionnaire de tuple (position) element à la position
    def __init__(self, taillePlateau):
        self.size = taillePlateau * 2 - 1
        # Deux representations?
        # les items particuliers
        self.kvPosItem = {}
        # et le labyrinthe case par case? Ou inutile

        # Liste des murs temporaires
        self.listTempWall = []

    # region Structure's manipulation

    # si collision, raise exception
    def moveItem(self, item, oldPosition, newPosition):
        itemType = item.getItemType()
        if newPosition in self.kvPosItem:
            raise CaseOccupedException(
                self.moveItem.__qualname__ + " oldP " + str(oldPosition) + " newP " + str(newPosition))

        if isCaseForType(itemType, newPosition):
            raise CaseWrongTypeException(self.moveItem.__qualname__ + " itemType " + str(itemType))

        objectToMove = self.kvPosItem.pop(oldPosition)  # remove + retrieve
        self.kvPosItem[newPosition] = objectToMove  # replace

    # si case deja occupé, exception
    def putItem(self, item, position):

        if (position in self.kvPosItem):
            raise CaseOccupedException(
                self.putItem.__qualname__ + " item " + item.getItemType() + " position " + str(position))

        self.kvPosItem[position] = item

    # si case vide, exception
    def removeItem(self, position):
        if (position not in self.kvPosItem):
            raise CaseEmptyException(self.removeItem.__qualname__ + " position " + str(position))

    # endregion

    # met a jour les lifespan des mur temp.
    def newTurn(self):
        for mur in self.listTempWall:
            if mur.isTimeToRemove():
                position = mur.getPositions()[0]
                self.removeWall(position)

    def getAsciiRepresentation(self):
        res = ""
        for i in range(self.size):
            for j in range(self.size):
                # on inverse i et j pour lire ligne par ligne
                pos = (i, j)
                # si un item spécial est la
                if pos in self.kvPosItem:
                    toAdd = self.kvPosItem[pos].getRepr()
                # sinon si double pair, case joueur vide
                elif (i % 2 == j % 2) & (i % 2 == 0):
                    toAdd = EnumCase.pionVide.__repr__()
                # si somme est pair, on a donc double impair
                elif ((i + j) % 2 == 0):
                    toAdd = EnumCase.caseUseless.__repr__()
                # sinon, double impair
                else:
                    toAdd = EnumCase.murVide.__repr__()
                # case par case dans la meme ligne
                res += toAdd
                if (j < self.size - 1):
                    res += "-"
            # a la fin d'une ligne
            res += "\n"

        # en sortie, on est censé avoir l'ascii Repr.
        return res

    # fonction de placement de mur.
    def putWall(self, murType, position, orientation, owner):
        ok = True
        # on regarde les cases concernées si le mur est placé
        cases = []
        cases = fromWallToCase(murType, position, orientation)
        # les cases sont-elles dispo, et dans le plateau de jeu ?
        for pos in cases:
            ok &= self.isCaseAvailable(pos) & isCaseLegit(pos)
        if not ok :
            raise WallIntersectionException("[PutWall]")

        mur = ""
        # creation d'un objet mur qui sera placé aux différentes cases
        if murType is EnumWall.classic:
            mur = WallClassic(cases, owner)
        elif murType is EnumWall.solid:
            mur = WallSolid(cases, owner)
        elif murType is EnumWall.long:
            mur = WallLong(cases, owner)
        elif murType is EnumWall.door:
            mur = WallDoor(cases, owner)
        elif murType is EnumWall.temp:
            mur = WallTemp(cases, owner)
            self.listTempWall.append(mur)

        for pos in cases:
            self.kvPosItem[pos] = mur

        owner.useWall(murType)

    # supprime un mur par une de ses positions
    def removeWall(self, pos):
        if(isinstance(pos, list)):
            pos = pos[0]

        # checker si existe


        # puis
        mur = self.kvPosItem[pos]
        positions = mur.positions

        # pour chacune des positions on desalloue
        for pos in positions:
            self.removeItem(pos)
        # Nécessaire?
        del mur

    # listeResultat = set qui contiendra les cases atteignables
    # posDepart = coordonnée d'une case autour de laquelle regarder
    # profondeur ( 2 = sprinter )
    # Si un pouvoir est utilisé
    def getCasesReachable(self, listeResultat, posDepart, deepth, EnumPowerType=None):
        if(deepth > 0):
            posX = posDepart[0]
            posY = posDepart[1]
            for i in range(-1, 2):
                for j in range(-1, 2):
                    # Inclu les cas l'un forcement égal a 0, exclu les deux égaux à 0
                    if (i * j == 0) & (i != j):
                        passeDroit = False
                        posWall = (posX + i, posY + j)
                        # si le mur est sur le chemin, ca dépend de si on a utiliser un pouvoir ou si c'est un mur door de la meme equipe
                        if posWall in self.kvPosItem and (EnumPowerType == EnumPion.jumper or EnumPowerType == EnumPion.sappeur) :
                            wall = self.kvPosItem[posWall]
                            if wall.getItemType() != EnumWall.solid :
                                passeDroit = True
                            elif wall.getItemType() == EnumWall.door :
                                passeDroit = True
                                # if EnumPowerType == EnumPion.sappeur:
                                #     self.removeWall(wall.positions)

                        # on vérifie qu'il n'y a pas de mur sur le chemin
                        if posWall not in self.kvPosItem or passeDroit:
                            posCase = (posX + 2*i, posY + 2*j)
                            # Si il y a le pion adverse en face, on appelle récursivement cette fonction
                            if (posCase in self.kvPosItem):
                                # Faire l'appel récursif
                                None
                                self.getCasesReachable(listeResultat, posCase, deepth - 1)

                                # passage à l'itération suivante
                                # break ?
                            # dans le cas ou la case suivante est dispo, on l'ajoute aux cases ou on peut aller,
                            # et qu'on ne sort pas du cadre
                            elif  ( 0 <= posCase[0] <=cg.taillePlateau*2 - 1) & ( 0 <= posCase[1] <=cg.taillePlateau*2 - 1):
                                listeResultat.add(posCase)
                                self.getCasesReachable(listeResultat,posCase,deepth-1)




    # Test si la case donné en pos. correspond au type d'item qu'on souhaite y mettre
    def isCaseAvailable(self, pos):
        if pos in self.kvPosItem:
            return False
        return True

    def isWallCanBePlaced(self, murType, orientation):
        longueur = 4 if murType == EnumWall.long.value else 2


# --------------------------
# region fonction statique
def isCaseForType(enumCaseType, pos):
    i = pos[0]
    j = pos[1]
    result = False
    # sinon si double pair, case joueur
    if (i % 2 == j % 2) & (i % 2 == 0):
        if enumCaseType == EnumTypeCase.forSpawn:
            result = True

    # si somme est pair, on a donc double impair
    elif ((i + j) % 2 == 0):
        if enumCaseType == EnumTypeCase.forNothing:
            result = True
    # sinon, double impair
    else:
        if enumCaseType == EnumTypeCase.forWall:
            result = True

    return result

# Depuis un placement hypothétique, et un type de mur, renvoie les cases concernées
def fromWallToCase(typeWall, pos, orientation):
    cases = []
    repetition = 2
    if orientation == EnumOrientation.droite:
        offsetX = 0
        offsetY = 1

    elif orientation == EnumOrientation.gauche:
        offsetX = 0
        offsetY = -1

    elif orientation == EnumOrientation.haut:
        offsetX = -1
        offsetY = 0

    elif orientation == EnumOrientation.bas:
        offsetX = 1
        offsetY = 0

    # on décale la position pour avoir la premiere cellule comme cellule case
    pos = (pos[0] + offsetX, pos[1] + offsetY)


    # ensuite l'offset sera de deux en deux
    offsetY *= 2
    offsetX *= 2

    if typeWall == EnumWall.long:
        repetition = 4

    for i in range(repetition):
        cases.append((pos[0] + i*offsetX, pos[1] +i* offsetY))

    return cases

# La case existe t elle par rapport à la dimension du plateau
def isCaseLegit(pos):
    posX = pos[0]
    posY = pos[1]
    return 0 <= posX < cg.taillePlateau * 2 - 1 and 0 <= posY < cg.taillePlateau * 2 - 1

# endregion
