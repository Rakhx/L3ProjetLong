
# --------------------------------
# region Exception pour les

# endregion

# --------------------------------
# region Exception pour les

# endregion


# --------------------------------
# region Exception pour les cases

# Si la case de réception est déjà occupée
class CaseOccupedException(LookupError):
    def __init__(self, message):
        LookupError.__init__(self, " Tentative de positionner un element dans une case déjà prise selon " + str(message))

# on essaye de
class CaseEmptyException(LookupError):
    def __init__(self, message):
        LookupError.__init__(self, " Tentative de libérer un element d'une case vide selon " + str(message))

# si on essaye de palcer un certain type d'item dans une mauvaise case
class CaseWrongTypeException(LookupError):
    def __init__(self, message):
        LookupError.__init__(self, " Tentative de positionner un element dans une case déjà prise selon " + str(message))

# endregion

# ------------------------------------
# region Exception concernant les murs

# le choix des murs au démarrage a une valeur totale trop haute
class WallInitListException(IndexError):
    def __init__(self, message):
        IndexError.__init__(self, " Cout total des murs a l'achat supérieur à la limite " + str(message))

class WallDisponibilityException(IndexError):
    def __init__(self, message):
        IndexError.__init__(self, " Le type de mur à placer n'est pas disponible " + str(message))

class WallIntersectionException(IndexError):
    def __init__(self, message):
        IndexError.__init__(self, " Le type de mur à placer n'est pas disponible " + str(message))

class WallOutOfBoundaryException():
    def __init__(self, message):
        IndexError.__init__(self, " Le type de mur à placer déborde du plateau " + str(message))


# endregion
