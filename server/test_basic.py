from server.scebase import Vector3
import sce,tempfile,pathlib
world = sce.World(pathlib.Path(tempfile.gettempdir()) / 'sce-test', pathlib.Path(__file__).parent.parent / 'contents' / 'trappist-1f')
world.Spawn('Megalosaurus_Character_BP',Vector3(10,10,0))