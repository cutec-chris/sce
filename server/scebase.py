import pathlib
class GameObject:
    def __init__(self,Position):
        self.name = None
        self.blueprintPath = None
        self.Position = Position
    def Hit(self,Type,SourceObject): return None,0 #returns List of Items (Loot) and Damage
    def Tick(self,TicksDone):
        #Execute actual Action
            #if Action is disturbed by some Event (Attack,Critical Food/Water,Action execution not possible anymore)
            #if Actions are clear
                #replan Actions
        pass
class AABBColide:
    def Collide(self,other):
        return False
class Creature(GameObject,AABBColide):
    def __init__(self,Position):
        super().__init__(Position)
        self.LastSeen = [] #List of last seen Objects
    def Move(self,Direction,Speed): pass
    def Tick(self,Ticks=1):
        #Calculate Movement
        #Add Objects seen and remove some of lastSeen objects
        super().Tick(self,Ticks) #execute Actions
class World:
    def __init__(self,Path,Blueprint):
        self.Quadrants = []
        self.Path = pathlib.Path(Path)
        if not self.Path.exists():
            self.Path.mkdir(parents=True)
        self.Blueprint = pathlib.Path(Blueprint)
    def Spawn(self,Blueprint,Position):
        return False
    def SaveWorld(self):
        return False
class Quadrant:
    def __init__(self,Position):
        self.Position = Position
        self.Objects = []
class Vector3:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
    def __add__(self,other):
        return Vector3(self.x+other.x,self.y+other.y,self.z+other.z)
    def __mul__(self,scalar):
        return Vector3(self.x*scalar,self.y*scalar,self.z*scalar)
    def lerp(self,other,scale):
        return self*(1-scale)+other*scale
    def __str__(self):
        return f'x:{self.x} y:{self.y} z:{self.z}'