# File: sc.py
# Author: Zhenyu Wei
# This file will contain the precast for Simple cubic

from emmm.core.create import Create
from emmm.core.molecule import Molecule
from . import InorganicBase
import numpy as np

class Sc(InorganicBase):
    """
    element: Element name for sc
    """
    def __init__(self, world, lattice_constant=1, element='SC') -> None:
        super().__init__(world)
        self.lattice_constant = lattice_constant
        self.label = element
        self.type = element.upper()
        self.mol = Molecule(self.label)

    def __call__(self, num_x=1, num_y=1, num_z=1):
        # Input
        self.num_x = num_x
        self.num_y = num_y
        self.num_z = num_z

        # Structure info
        self.atom_relative_coord = np.array([
            [0, 0, 0],
        ])
        self.cell_vec = np.array([
            [self.lattice_constant, 0, 0],
            [0, self.lattice_constant, 0],
            [0, 0, self.lattice_constant],
        ])  
        self._type_flag = [1]
        self._atom_type = ('%s' %self.type).split()
        self._atom_charge = [0]
        self._atom_mass = [1]    
        self._input_complete()