# author: Roy Kid

class System(dict):

    def __init__(self):
        # self.world = world
        self.limitedKeys = [
            'unit',
            'xlo', 
            'xhi',
            'ylo', 
            'yhi', 
            'zlo',
            'zhi', 
            'boundaryX', 
            'boundaryY',
            'boundaryZ', 
            'atoms', # raw info of each atom
            'atomsNum', # the number of atoms 
            'atomStyle', 
            'atomTypeNum',
            'bonds',
            'bondNum', 
            'bondStyle', 
            'bondTypeNum',
            'bondCoeffs', 
            'angles', 
            'angleNum', 
            'angleStyle', 
            'angleTypeNum', 
            'angleCoeffs',
            'dihedrals', 
            'dihedralNum', 
            'dihedralStyle',
            'dihedralTypeNum', 
            'dihedralCoeffs', 
            'impropers', 
            'improperNum', 
            'improperStyle',
            'improperTypeNum', 
            'improperCoeffs',
            'topoBonds', 
            'topoAngles', 
            'topoDihedrals',
        ]

    def check_system(self):
        pass
    
    def __getitem__(self, k):
        return super().__getitem__(k)

    def __setitem__(self, k, v):
        if k not in self.limitedKeys:
            raise KeyError('System has no %s keyword', k)
        
        if k == 'xlo' or k == 'xhi' or k=='ylo' or k=='yhi' or k=='zlo' or k=='zhi':
            v = float(v)

        elif k == 'atomNum' or k=='bondNum' or k=='angleNum' or k=='dihedralNum' or k=='improperNum':
            v = int(v)
           
        super().__setitem__(k, v)
