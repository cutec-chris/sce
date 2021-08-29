import goap,pathlib
from scebase import *
class Creature(GameObject):
    def __init__(self,Position):
        super().__init__(Position)
        self.LastSeen = [] #List of last seen Objects
    def Move(self,Direction,Speed): pass
    def Tick(self,Ticks=1):
        #Calculate Movement
        #Add Objects seen and remove some of lastSeen objects
        super().Tick(self,Ticks) #execute Actions
class Plant(Creature): pass
class Dinos(Creature):
    def __init__(self,Position):
        super().__init__(Position)
        self.fullStatsRaw = [None, None, None, None, None, None, None, None, None, None, None, None]
        self.immobilizedBy = []
        self.noGender = True
        self.colors = []
        self.taming = {'nonViolent': False, 'violent': False, 'tamingIneffectiveness': 8.333333, 'affinityNeeded0': 450, 'affinityIncreasePL': 22.5, 'foodConsumptionBase': 0.001543, 'foodConsumptionMult': 216.0294}
        self.TamedBaseHealthMultiplier = 1
class Player(GameObject): pass
class Structures(GameObject): pass