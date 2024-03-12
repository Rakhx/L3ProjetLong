from Allin.Exception.Exceptions import CaseOccupedException, CaseEmptyException


class plateau :

    # struture interne, dictionnaire de tuple (position) element à la position
    def __init__(self, taillePlateau):
        # Plateau par défault
        #self.plateau = np.chararray(taillePlateau*2-1,taillePlateau*2-1)
        self.size = taillePlateau * 2 + 1

        # Rempli par les éléments par défault
        self.kvPosItem = {}

    def getAsciiRepresentation(element):
        None

    # region Structure's manipulation

    # si collision, raise exception
    def moveItem(self, oldPosition, newPosition):
        if(newPosition in self.kvPosItem):
            raise CaseOccupedException( self.moveItem.__qualname__ +" oldP "+ str(oldPosition) +" newP "+ str(newPosition))
        objectToMove = self.kvPosItem.pop(oldPosition)
        self.kvPosItem[newPosition] = objectToMove

    # si case deja occupé, exception
    def putItem(self,item, position):
        if(position in self.kvPosItem):
            raise CaseOccupedException( self.moveItem.__qualname__ +" item "+ str(item) +" position "+ str(position))
        self.kvPosItem[position] = item

    # si case vide, exception
    def removeItem(self, position):
        if(position not in self.kvPosItem):
            raise CaseEmptyException(self.moveItem.__qualname__ + " position " + str(position))

    # endregion
