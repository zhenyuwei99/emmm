
import os,sys
# set the source code path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# set current code path

import emmm as em


world = em.World('real')

InputBase = world.active_plugin('INlmpdat')
                     
filepath = os.path.dirname(__file__)+'/'+'h2o.lmpdat'

h2os = InputBase.read_data(filepath)


print(h2os.toDict())

# OutputBase = world.active_plugin('OUTjson')

# OutputBase.vis()
# world.vis()