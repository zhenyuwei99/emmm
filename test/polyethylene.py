#     H1   H4   H1
#     |    |    |
# H2- C1 - C3 - C1 - H2
#     |    |    | 
#     H3   H5   H3
# methyl1    methyl2
#    / methylene \
#     polythylene


import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from src.world import World

world = World()


# InputBase = world.active_plugin('LmpDat')
InputBase = world.active_plugin('Pdb')
InputBase.read_data('polyethylene.pdb')
OutputBase = world.active_plugin('GraphViz')

OutputBase.show()