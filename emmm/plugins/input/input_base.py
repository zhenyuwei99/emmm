# author: Roy Kid

from collections import defaultdict
from emmm.core.molecule import Molecule

class InputBase:
    """ The parent class for all the input parser
    """
    def __init__(self, world):
        
        self.world = world
        self.system = world.system

    def group_by(self, atoms:list, reference:str='molLabel', returnType:str='Molecule'):
        """ Util method to group atoms by a certain reference. For example, you can group them by the molLable, which means those atoms in a same molecule. 

        Args:
            atoms (list): a list of atoms, usually generate by flatten()
            reference (str, optional): Keyword in Atom. Defaults to 'molLabel'.
            returnType (str, optional): [description]. Defaults to 'Molecule'.

        Returns:
            dict: {reference: molecule, } 
        """ 

        grouped_atoms = defaultdict(list)
        print(f'group the atoms by {reference}')
        for atom in atoms:
            ref = getattr(atom, reference, 'UNDEFINED')
            grouped_atoms[ref].append(atom)

        if returnType == 'dict':
            molecules = defaultdict(Molecule)
            for ref, gatom in grouped_atoms.items():
                molecules[ref].add_items(gatom)

            for ref, mol in molecules.items():
                mol.label = ref

            return molecules