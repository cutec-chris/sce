import goal
class GameObject:
    def __init__(self):
        self.name = None
        self.blueprintPath = None
    def Hit(self,Type,SourceObject): return None,0 #returns List of Items (Loot) and Damage
    def Tick(self,TicksDone):
        #Execute actual Action
            #if Action is disturbed by some Event (Attack,Critical Food/Water,Action execution not possible anymore)
            #if Actions are clear
                #replan Actions
class Creature(GameObject):
    def __init__(self):
        super().__init__(self)
        self.LastSeen = [] #List of last seen Objects
    def Move(self,Direction,Speed): pass
    def Tick(self,Ticks):
        #Calculate Movement
        #Add Objects seen and remove some of lastSeen objects
        super().Tick(self,Ticks) #execute Actions
class Plant(Creature): pass
class Dinos(Creature):
    def __init__(self):
        super().__init__(self)
        self.fullStatsRaw = [None, None, None, None, None, None, None, None, None, None, None, None]
        self.immobilizedBy = []
        self.noGender = True
        self.colors = []
        self.taming = {'nonViolent': False, 'violent': False, 'tamingIneffectiveness': 8.333333, 'affinityNeeded0': 450, 'affinityIncreasePL': 22.5, 'foodConsumptionBase': 0.001543, 'foodConsumptionMult': 216.0294}
        self.TamedBaseHealthMultiplier = 1
class Carnivore(Dinos): pass
class Herbivore(Dinos): pass
class Omnivore(Herbivore,Carnivore): pass
class Player(GameObject): pass
class Structures(GameObject): pass