import sce,tempfile,pathlib
world = sce.World(pathlib.Path(tempfile.gettempdir()) / 'sce-test')
plant1 = sce.Plant([10,10,0])
dino1 = sce.Dinos([0,0,0])