# author: Roy Kid
from emmm.core.molecule import Molecule
from emmm.plugins.output.output_base import OutputBase
import json
import eel

class OUTjson(OutputBase):

    def __init__(self, world):
        super().__init__(world)

    def dump_data(self):
        
        w = self.world
        d = dict()
        def w2d(*kws):
            for kw in kws:
                d[kw] = w[kw]

        # add atoms
        atoms = w.items.flatten()
        items = list()
        for atom in atoms:
            items.append(atom.toDict())

        # add bonds
        bonds = list()
        self.search_topo(isAngle=False, isDihedral=False)
        bonds = self.world.topo.gen_bond()

        d['items'] = items
        d['bonds'] = bonds

        json_str = json.dumps(d)
        print(json_str)
        return json_str

