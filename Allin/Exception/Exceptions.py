class CaseOccupedException(LookupError):
    def __init__(self, message):
        LookupError.__init__(self, " Tentative de positionner un element dans une case déjà prise selon " + str(message))
class CaseEmptyException(LookupError):
    def __init__(self, message):
        LookupError.__init__(self, " Tentative de libérer un element d'une case vide selon " + str(message))
