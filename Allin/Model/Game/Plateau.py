from Allin.Exception.Exceptions import CaseOccupedException, CaseEmptyException, CaseWrongTypeException
from Allin.Model.Game.EnumCase import EnumCase, EnumTypeCase, EnumWall


class Plateau:

    # struture interne, dictionnaire de tuple (position) element à la position
    def __init__(self, taillePlateau):
        self.size = taillePlateau * 2 - 1
        # Deux representations?
        # les items particuliers
        self.kvPosItem = {}
        # et le labyrinthe case par case? Ou inutile

    # region Structure's manipulation

    # si collision, raise exception
    def moveItem(self, itemType, oldPosition, newPosition):
        if newPosition in self.kvPosItem:
            raise CaseOccupedException(
                self.moveItem.__qualname__ + " oldP " + str(oldPosition) + " newP " + str(newPosition))

        if isCaseForType(itemType, newPosition):
            raise CaseWrongTypeException(self.moveItem.__qualname__ + " itemType " + str(itemType))

        objectToMove = self.kvPosItem.pop(oldPosition)  # remove + retrieve
        self.kvPosItem[newPosition] = objectToMove  # replace

    # si case deja occupé, exception
    def putItem(self, enumCase, position):
        if (position in self.kvPosItem):
            raise CaseOccupedException(
                self.putItem.__qualname__ + " item " + str(enumCase) + " position " + str(position))
        if not isinstance(enumCase, EnumCase):
            raise TypeError()

        self.kvPosItem[position] = enumCase

    # si case vide, exception
    def removeItem(self, position):
        if (position not in self.kvPosItem):
            raise CaseEmptyException(self.removeItem.__qualname__ + " position " + str(position))

    def placerMur(self, murType, postition):
        None

    # endregion

    def getAsciiRepresentation(self):
        res = ""
        for i in range(self.size):
            for j in range(self.size):
                # on inverse i et j pour lire ligne par ligne
                pos = (i, j)
                # si un item spécial est la
                if pos in self.kvPosItem:
                    toAdd = EnumCase(self.kvPosItem[pos]).__repr__()
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

    # Test si la case donné en pos. correspond au type d'item qu'on souhaite y mettre

    def isCaseAvailable(self, pos):
        if pos in self.kvPosItem:
            return False
        return True

    def isWallCanBePlaced(self, murType, orientation):
       longueur = 4 if murType == EnumWall.long.value else 2




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


# test = Plateau(9)
# test.putItem(EnumCase.pionJ1, (0,8))
# test.putItem(EnumCase.pionJ2, (0,0))
# lol = test.getAsciiRepresentation()
# print(lol)
