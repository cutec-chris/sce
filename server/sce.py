import goal
class GameObject:
    def __init__(self):
        name = None
        blueprintPath = None
    def HitActionL(SourceObject): return None,0
    def HitActionR(SourceObject): return None,0
    def HitActionC(SourceObject): return None,0
class Creature(GameObject): pass
class Plant(Creature): pass
class Dinos(Creature):
    def __init__(self):
        super().__init__(self)
        fullStatsRaw = [None, None, None, None, None, None, None, None, None, None, None, None]
        immobilizedBy = []
        noGender = True
        colors = []
        taming = {'nonViolent': False, 'violent': False, 'tamingIneffectiveness': 8.333333, 'affinityNeeded0': 450, 'affinityIncreasePL': 22.5, 'foodConsumptionBase': 0.001543, 'foodConsumptionMult': 216.0294}
        TamedBaseHealthMultiplier = 1
class Carnivore(Dinos): pass
class Herbivore(Dinos): pass
class Omnivore(Herbivore,Carnivore): pass
class Player(GameObject): pass
class Structures(GameObject): pass