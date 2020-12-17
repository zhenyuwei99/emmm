
import os,sys
# set the source code path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# set current code path

import emmm as em


world = em.World('real')

sio2 = em.plugins.precast.inorganic.SiO2(world)


# OutputBase.vis()
# world.vis()