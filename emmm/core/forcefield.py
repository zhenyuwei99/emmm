class ForceField:

    def __init__(self, world):
        
        self.world = world

    def set_bond_coeffs(self, style, label, item1, item2, *coeffs):

        # self.world['bondCoeffs] -> (style, label, item1, item2, coeff1, coeff2)

        self.world['bondStyle'] = style
        ## self.world['bondLabel']
        self.world.setdefault('bondCoeffs', list).append([str(item1), str(item2), *map(str,coeffs)])

    def set_angle_coeffs(self, style, item1, item2, item3, *coeffs):
        self.world['angleStyle'] = style
        self.world['angleCoeffs'] = [str(item1), str(item2), str(item3), *map(str,coeffs)]

    def set_dihedral_coeff(self, style, item1, item2, item3, item4, *coeffs):
        self.world['dihedralStyle'] = style
        self.world['dihedralCoeffs'] = [str(item1), str(item2), str(item3), str(item4), *map(str, coeffs)]

    def _match_items(self, items1:list, items2:list)->bool:
        if sorted(items1) == sorted(items2):
            return True
        else:
            return False

    def match_bond(self, item1, item2):
        for coeff in self.world['bondCoeffs']:
            if self._match_items([item1, item2], coeff[:2]):
                return [self.world['bondStyle'], *coeff[2:]]

                
