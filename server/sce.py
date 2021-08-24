import goal
class GameObject:
    __init__(self):
        pass
    def HitActionL(SourceObject): return None,0
    def HitActionR(SourceObject): return None,0
    def HitActionC(SourceObject): return None,0
class Creature(GameObject): pass
class Plant(Creature): pass
class Carnivore(Creature): pass
class Herbivore(Creature): pass
class Omnivore(Herbivore,Carnivore): pass
class Player(GameObject): pass