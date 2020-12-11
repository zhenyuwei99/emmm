class ForceField:

    def __init__(self, world):
        
        self.world = world
        self.system = world.system
        

    def add_bond_style(self, bond_style):
        self.system['bond_style'] = bond_style

    def add_atom_style(self, atom_style):
        self.system['atom_style'] = atom_style

    def add_bond_coeff(self, a1, a2, *coeffs):
        self.system['bond_coeff'].append([a1, a2, *coeffs])