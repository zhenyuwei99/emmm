# File: inorganic_base.py
# Author: Zhenyu Wei
# This file will contain a parent class for inorganic
# material precast

from .. import PrecastBase
from emmm.core.molecule import Molecule
from emmm.core.create import Create
from collections import Counter

class InorganicBase(PrecastBase):
    def __init__(self, world) -> None:
        self.world = world
        super().__init__(world)

    def _generateInfoList(self) -> None:
        self.atom_type = []
        self.atom_charge = []
        self.atom_mass = []
        for (i, type) in enumerate(self._type_flag):
            self.atom_type.append('%s%d' %(self._atom_type[type], 
                Counter(self._type_flag[:i+1])[type])) # The atom with same type in a residue will add a number, avoiding repeating
            self.atom_charge.append(self._atom_charge[type])
            self.atom_mass.append(self._atom_mass[type])
    
    def _generateCellUnit(self) -> None:
        unit = Molecule('%s_%d' %(self.type, 0), self.type)
        for i in range(self.atom_relative_coord.shape[0]):
            atomLabel = '%s_atom_%d' %(unit.label, i)
            type = self.atom_type[i]
            charge = self.atom_charge[i]
            coord = self.cell_vec.dot(self.atom_relative_coord[i, :])
            atom = Create.create_full_atom(atomLabel, type, charge, coord[0], coord[1], coord[2])
            unit.add_items(atom)
        self.mol.add_items(unit)

    def _duplicate(self, move_vec, num_replicas) -> None:
        mol_temp = self.mol.get_replica('template')
        for i in range(1, num_replicas):
            mol_new = mol_temp.get_replica('none')
            mol_new.move(move_vec[0]*i, move_vec[1]*i, move_vec[2]*i)
            for mol in mol_new.container:
                mol.label = '%s_%d' %(self.type, len(self.mol.container))
                self.mol.add_items(mol)

    def _input_complete(self) -> None:
        self._generateInfoList()
        self._generateCellUnit()
        self._duplicate(self.cell_vec[:, 0], self.num_x)
        self._duplicate(self.cell_vec[:, 1], self.num_y)
        self._duplicate(self.cell_vec[:, 2], self.num_z) 