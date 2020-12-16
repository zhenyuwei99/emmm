# File: lattice.py
# Author: Zhenyu Wei
# This file will contain the constructors for the basic
#  lattcie structure like sc, bcc, fcc, dc, etc

from emmm.core.create import Create
from emmm.core.atom import Atom
from emmm.core.molecule import Molecule
from emmm.plugins.precast.precast_base import PrecastBase
import numpy as np

class Lattice(PrecastBase):
    def __init__(self, world):
        super().__init__(world)
        self.mol = Molecule('Lattice')
    
    def _generateLattice(self):
        9562
        lattice = Molecule('%s_%d' %(self.name, 0))
        for i in range(self.atom_relative_coord.shape[0]):
            coord = self.cell_vec.dot(self.atom_relative_coord[i, :])
            lattice.add_item(Create.create_coord_atom('%s_atom_%d' %(self.name, i), coord))
        self.mol.add_item(lattice)
        self.mol.label = self.name

    def _addWorld(self):
        self.world.molecules.add_items(self.mol)

    def _duplicate(self, move_vec, num_replicas):
        mol_temp = self.mol.get_replica('template')
        for i in range(1, num_replicas):
            mol_new = mol_temp.get_replica('none')
            mol_new.move(move_vec[0]*i, move_vec[1]*i, move_vec[2]*i)
            for mol in mol_new.container:
                mol.label = '%s_%d' %(self.name, len(self.mol.container))
                self.mol.add_item(mol)

    def _input_complete(self):
        self._generateLattice()
        self._duplicate(self.cell_vec[:, 0], self.num_x)
        self._duplicate(self.cell_vec[:, 1], self.num_y)
        self._duplicate(self.cell_vec[:, 2], self.num_z)

    def sc(self, lattice_constant=1, num_x=1, num_y=1, num_z=1, name='sc'):
        # Structure info
        self.atom_relative_coord = np.array([
            [0, 0, 0],
        ])
        self.cell_vec = np.array([
            [lattice_constant, 0, 0],
            [0, lattice_constant, 0],
            [0, 0, lattice_constant],
        ])      
        self.num_x = num_x
        self.num_y = num_y
        self.num_z = num_z
        self.name = name
        self._input_complete()

    def bcc(self, lattice_constant=1, num_x=1, num_y=1, num_z=1, name='bcc'):
        # Structure info
        self.atom_relative_coord = np.array([
            [0, 0, 0],
            [0.5, 0.5, 0.5],
        ])
        self.cell_vec = np.array([
            [lattice_constant, 0, 0],
            [0, lattice_constant, 0],
            [0, 0, lattice_constant],
        ])
        self.num_x = num_x
        self.num_y = num_y
        self.num_z = num_z
        self.name = name
        self._input_complete()

    def fcc(self, lattice_constant=1, num_x=1, num_y=1, num_z=1, name='fcc'):
        # Structure info
        self.atom_relative_coord = np.array([
            [0, 0, 0],
            [0, 0.5, 0.5],
            [0.5, 0, 0.5],
            [0.5, 0.5, 0],
        ])
        self.cell_vec = np.array([
            [lattice_constant, 0, 0],
            [0, lattice_constant, 0],
            [0, 0, lattice_constant],
        ])
        self.num_x = num_x
        self.num_y = num_y
        self.num_z = num_z
        self.name = name
        self._input_complete()
    
    def dc(self, lattice_constant=1, num_x=1, num_y=1, num_z=1, name='dc'):
        # Structure info
        self.atom_relative_coord = np.array([
            [0, 0, 0],
            [0, 0.5, 0.5],
            [0.5, 0, 0.5],
            [0.5, 0.5, 0],
            [0.25, 0.25, 0.25],
            [0.25, 0.75, 0.75],
            [0.75, 0.25, 0.75],
            [0.75, 0.75, 0.25],
        ])
        self.cell_vec = np.array([
            [lattice_constant, 0, 0],
            [0, lattice_constant, 0],
            [0, 0, lattice_constant],
        ])
        self.num_x = num_x
        self.num_y = num_y
        self.num_z = num_z
        self.name = name
        self._input_complete()

    def hcp(self, lattice_constant=1, num_x=1, num_y=1, num_z=1, name='hcp'):
        # Structure info
        self.atom_relative_coord = np.array([
            [0, 0, 0],
            [0, 0.5, 0.5],
            [0.5, 0, 0.5],
            [0.5, 0.5, 0],
            [0.25, 0.25, 0.25],
            [0.25, 0.75, 0.75],
            [0.75, 0.25, 0.75],
            [0.75, 0.75, 0.25],
        ])
        self.cell_vec = np.array([
            [lattice_constant, 0, 0],
            [0, lattice_constant, 0],
            [0, 0, lattice_constant],
        ])
        self.num_x = num_x
        self.num_y = num_y
        self.num_z = num_z
        self.name = name
        self._input_complete()