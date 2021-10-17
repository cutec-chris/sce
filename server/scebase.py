import pathlib,json,time
from vectormath.vector import Vector3
class GameObject:
    def __init__(self,World,name,Position=Vector3(0,0,0),Direction=Vector3(0,0,0)):
        if not hasattr(self,'Folder'):
            self.Folder = 'tiles/%d_%d_%d' % (Position[0] / World.TileSize,
                                              Position[1] / World.TileSize,
                                              Position[2] / World.TileSize)
        self.World = World
        self.name = name
        self.blueprintPath = pathlib.Path(__file__).parent
        self.Path = self.World.Path / self.Folder / (self.name + '.json')
        self.Position = Position
        self.Direction = Direction
        if self.Path.exists():
            with open(self.Path,'r') as f:
                aJson = f.read()
                if aJson != '':
                    self.fromJson(aJson)
    def GetModel(self,lod=10):
        return self.blueprintPath / ('%s_%d.glb' % (str(self.__name__),lod))
class  DynamicObject(GameObject):
    def __getstate__(self):
        return {
            'Name': self.name,
            'Position': self.Position,
            'Direction': self.Direction,
            'blueprintPath' : str(self.blueprintPath),
        }
    def Hit(self,Type,SourceObject): return None,0 #returns List of Items (Loot) and Damage
    def Tick(self,TicksDone):
        #Execute actual Action
            #if Action is disturbed by some Event (Attack,Critical Food/Water,Action execution not possible anymore)
            #if Actions are clear
                #replan Actions
        pass
    def toJson(self):
        return json.dumps(self, default=lambda o: self.__getstate__)
    def fromJson(self,aJson):
        self.__dict__ = json.loads(aJson)
    def Save(self):
        with open(self.Path,'w') as f:
            aJson = self.toJson()
            f.write(aJson)
    def __del__(self):
        self.Save()
class AABBColide:
    def Collide(self,other):
        if  self.Position.x > other.Left\
        and self.Position.x < other.Right\
        and self.Position.y > other.Near\
        and self.Position.y < other.Far\
        and self.Position.z > other.Bottom\
        and self.Position.z < other.Top:
            return True
        return False
class Creature(DynamicObject,AABBColide):
    def __init__(self,Position):
        super().__init__(Position)
        self.LastSeen = [] #List of last seen Objects
    def Move(self,Direction,Speed): pass
    def Tick(self,Ticks=1):
        #Calculate Movement
        #Add Objects seen and remove some of lastSeen objects
        super().Tick(self,Ticks) #execute Actions
class Player(DynamicObject):
    def __init__(self,World,name):
        self.Folder = 'players'
        super().__init__(World,name)
        self.knownTiles = []
        self.move(Vector3(0,0,0),0)
        self.lastUpdate = time.time()
    def move(self,Direction,Speed):
        #update Position (lastUpdate time-now)
        #Check if tile known to client and create if not there
        tileFound = False
        for tile in self.knownTiles:
            if self.Collide(tile):
                tileFound = True
                break
        if not tileFound:
            for tile in self.World.Tiles:
                if self.Collide(tile):
                    tileFound = True
                    self.knownTiles.append(tile)
                    break
        if not tileFound:
            self.World.Tiles.append(Tile(Vector3(self.Position.x/self.World.TileSize,
                                                 self.Position.y/self.World.TileSize,
                                                 self.Position.z/self.World.TileSize
                                                )))
        #background load tiles in Sight until Framerate or Memory dropps
class World:
    def __init__(self,Path):
        self.Players = []
        self.Tiles = []
        self.TileSize = 100
        self.Path = pathlib.Path(Path)
        if not self.Path.exists():
            self.Path.mkdir(parents=True)
        (self.Path / 'players').mkdir(parents=True,exist_ok=True)
        (self.Path / 'tiles').mkdir(parents=True,exist_ok=True)
    def Spawn(self,Blueprint,Position):
        return False
    def SaveWorld(self):
        return False
    async def processMessage(self,message):
        if message['method'] == 'login':
            message['status'] = 500
            for player in self.Players:
                if player.name == message['user']:
                    message['status'] = 200
                    break
            if message['status'] != 200:
                self.Players.append(Player(self,message['user']['user']))
                message['status'] = 200
            return message
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