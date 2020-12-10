# author: Roy Kid

from emmm.core.atom import Atom

import numpy as np
class Create:

    @staticmethod
    def _create_atom(**kwarg):
        atom = Atom()
        for k,v in kwarg.items():
            if v is not None:
               setattr(atom, k, v)
        return atom
    
    @staticmethod
    def create_full_atom(atomLabel, molLabel, type, q, x, y, z, neighbor=None):

        atomLabel = str(atomLabel)
        molLabel = str(molLabel)
        type = str(type)
        q = float(q)
        x = float(x)
        y = float(y)
        z = float(z)

        return Create._create_atom( atomlabel=atomLabel,\
                                    mollabel = molLabel,\
                                    type = type,\
                                    q = q,\
                                    coords = np.array([x,y,z]),
                                    neighbor = neighbor)

    @staticmethod
    def create_atoms(atom_style, atoms, topo=None, returnType='list'):

        # getattr(Creator, f'create_{atom_type}_atom', create_full_atom)()
        if returnType == 'list':
            atoms_list = list()
            if atom_style == 'full':
                for atom in atoms:
                    atoms_list.append(Create.create_full_atom(
                            atomLabel=atom[0],
                            molLabel=atom[1],
                            type=atom[2],
                            q = atom[3],
                            x = atom[4],
                            y = atom[5],
                            z = atom[6],
                            neighbor=None   
                    ))
            return atoms_list

        elif returnType == 'dict':
            atoms_dict = dict()
            if atom_style == 'full':
                for atom in atoms:
                    atoms_dict[atom[0]] = Create.create_full_atom(
                        atomLabel=atom[0],
                        molLabel=atom[1],
                        type=atom[2],
                        q = atom[3],
                        x = atom[4],
                        y = atom[5],
                        z = atom[6],
                        neighbor=None   
                )

            return atoms_dict
        
        else:
            raise TypeError(' ')
