# File: sio2.py
# Author: Zhenyu Wei
# This file will contain the precast for SiO2

from emmm.core.create import Create
from emmm.core.molecule import Molecule
from . import InorganicBase
import numpy as np

class SiO2(InorganicBase):
    def __init__(self, world) -> None:
        super().__init__(world)
        self.label = 'SIO'
        self.type = 'SIO'
        self.mol = Molecule(self.label)

    def __call__(self, num_x=1, num_y=1, num_z=1):
        # Input
        self.num_x = num_x
        self.num_y = num_y
        self.num_z = num_z

        # Structure info
        self.atom_relative_coord = np.array([
            [0.196866211329851,   0.196866211329851,   0],
            [0.136601044596223,   0,                   0.178468624064479],
            [0.596625150662917,   0.596625150662917,   0.500000000000000],
            [0.656890317396545,   0.793491361992768,   0.678468624064479],
            [0.096625150662917,   0.696866211329852,   0.250000000000000],
            [0.293491361992768,   0.636601044596224,   0.428468624064479],
            [0.696866211329852,   0.096625150662917,   0.750000000000000],
            [0.500000000000000,   0.156890317396545,   0.928468624064479],
            [0.156890317396545,   0.500000000000000,   0.071531375935521],
            [0.636601044596224,   0.293491361992768,   0.571531375935521],
            [0,                   0.136601044596223,   0.821531375935521],
            [0.793491361992768,   0.656890317396545,   0.321531375935521]
        ])
        self.cell_vec = np.array([
            [4.9780,  0,           0],
            [0,       4.9780,      0],
            [0,       0,           6.9480]
        ])
        self._type_flag = [2, 1, 2, 2, 1, 2, 
                        1, 1, 2, 1, 1, 2, 1, 
                        1, 2, 1, 2, 2, 1, 2, 
                        1, 1, 2, 1, 1, 2, 1, 1]
        self._atom_type = 'N SI'.split()
        self._atom_charge = [0.7679, -0.575925]
        self._atom_mass = [14.0067, 28.0855] # N: 14.0067. Si: 28.085501. Unit: g/mol

        self._input_complete()