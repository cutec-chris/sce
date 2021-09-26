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
class Player(GameObject): pass
class World:
    def __init__(self,Path):
        self.Tiles = []
        self.Path = pathlib.Path(Path)
        if not self.Path.exists():
            self.Path.mkdir(parents=True)
        (self.Path / 'users').mkdir(parents=True,exist_ok=True)
        (self.Path / 'tiles').mkdir(parents=True,exist_ok=True)
    def Spawn(self,Blueprint,Position):
        return False
    def SaveWorld(self):
        return False
    def processMessage(self,Message):
        if message['method'] == 'login':
            if (self.Path / 'users' / (message['user']+'.json')).exists():

            if World.Login(message['user'],message['password']):
                message['status'] = 200
            else:
                message['status'] = 401
            await socket.send(json.dumps(message))
        elif message['method'] == 'register':
            if World.Register(message['from']):
                message['status'] = 200
            else:
                message['status'] = 401
        pass
class Tile:
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