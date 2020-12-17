import sys 

path_package = '../emmm'
sys.path.append(path_package)

import emmm as em
import emmm.plugins.constructor.lattice as lattice 
import emmm.plugins.input.IN_lmpdat as IN_lmpdat
import emmm.plugins.output.OUT_lmpdat as OUT_lmpdat

from emmm.plugins.constructor import *