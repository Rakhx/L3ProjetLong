from enum import Enum, auto

#@verify(UNIQUE)
class EnumCase(Enum):
    pionVide = auto()
    murVide = auto()
    caseUseless = auto()
    pionJ1 = auto()
    pionJ2 = auto()
    classiqueJ1 = auto()
    classiqueJ2 = auto()
    temporyJ1 = auto()
    temporyJ2 = auto()
    doorJ1 = auto()
    doorJ2 = auto()
    longJ1 = auto()
    longJ2 = auto()
    solideJ1 = auto()
    solideJ2 = auto()

    def fromEnumToChar(self):
        print(self.name)

    def __str__(self):
        return self.name

    def __repr__(self):
        if self.name == EnumCase.pionVide.name:
            return 'c0'
        if self.name == EnumCase.murVide.name:
            return 'm0'
        if self.name == EnumCase.caseUseless.name:
            return 'u0'
        if self.name == EnumCase.pionJ1.name:
            return 'p1'
        if self.name == EnumCase.pionJ2.name:
            return 'p2'
        if self.name == EnumCase.classiqueJ1.name:
            return 'c1'
        if self.name == EnumCase.classiqueJ2.name:
            return 'c2'
        if self.name == EnumCase.temporyJ1.name:
            return 't1'
        if self.name == EnumCase.temporyJ2.name:
            return 't2'
        if self.name == EnumCase.doorJ1.name:
            return 'd1'
        if self.name == EnumCase.doorJ2.name:
            return 'd2'
        if self.name == EnumCase.longJ1.name:
            return 'l1'
        if self.name == EnumCase.longJ2.name:
            return 'l2'
        if self.name == EnumCase.solideJ1.name:
            return 's1'
        if self.name == EnumCase.solideJ2.name:
            return 's2'

class EnumOrientation(Enum):
    haut = 0
    droite = 1
    bas = 2
    gauche = 3

class EnumPlayer(Enum):
    joueur1 = 0
    joueur2 = 1

class EnumPion(Enum):
    sappeur = 0
    jumper = 1
    sprinter = 2

class EnumWall(Enum):
    classic = 0
    solid = 1
    long = 2
    door = 3

class EnumTypeCase(Enum):
    forSpawn = auto()
    forWall = auto()
    forNothing = auto()
