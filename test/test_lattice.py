import sys
path_package = '../emmm'
sys.path.append(path_package)

import emmm

world = emmm.World('real')

lattice = emmm.plugins.precast.inorganic.Lattice(world)
lattice.bcc(1, 2, 2, 2)