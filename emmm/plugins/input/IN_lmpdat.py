#author: Roy Kid

from emmm.core.create import Create
from emmm.plugins.input.input_base import InputBase



class INlmpdat(InputBase):

    def __init__(self, world):
        super().__init__(world)
        self.temp_system = dict()

    def _read_title(self, line):
        self.comment = line
        return self._readline()

    def _readline(self):
        return self.file.readline()

    def _skipblankline(self, line):
        while line.startswith('\n') or line.startswith('#'):
            line = self.file.readline()
        return line

    def _deal_with_comment(self, line):

        if '#' in line:
            return line[:line.index('#')]
        else:
            return line
        

    def read_data(self, file, atom_style='full'):

        self.file_name = file

        self.file = open(self.file_name)

        line = self._readline()
        line = self._read_title(line)
        line = self._skipblankline(line)
        ##
        number_of_section = 9
        i = 0
        while i < number_of_section and line != '':

            line = self._read_bondaries(line)
            line = self._read_system(line)
            line = self._read_masses(line)
            line = self._read_pair_coeffs(line)
            line = self._read_bond_coeffs(line)
            line = self._read_angle_coeffs(line)
            line = self._read_velocities(line)
            line = self._read_dihedral_coeffs(line)
            line = self._read_improper_coeffs(line)

            line = self._read_atoms(line)
            line = self._read_angles(line)
            line = self._read_bonds(line)
            line = self._read_dihedrals(line)
            line = self._read_impropers(line)

            i+=1

        # while parse is complete
        return self.input_completed()
        

    def input_completed(self):
        """to convert self.temp_system to System class; to convert raw atoms to molecules tree and atoms graph
        """

        self.file.close()
        if len(self.temp_system['Atoms'][0]) == 7:
            self.temp_system['atom_style'] = 'full'


        elif 'atom_style' not in self.temp_system:
            self.temp_system['atom_style'] = input('> enter atom style')

        else:
            raise KeyError('atom style undefined')

        ## convert temp_system to System

        temp2sys = {
            'xlo':'xlo',
            'ylo':'ylo',
            'zlo':'zlo',
            'xhi':'xhi',
            'yhi':'yhi',
            'zhi':'zhi',
            'Masses': 'masses',
            'atom_style':'atomStyle',
            'Atoms':'atoms',
            'atoms':'atomNum',
            'atom types':'atomTypeNum',
            'Bonds':'bonds',
            'bonds':'bondNum',
            'bond types':'bondTypeNum',
            'Angles':'angles',
            'angles':'angleNum',
            'angle types':'angleTypeNum',
            'Dihedrals':'dihedral',
            'dihedrals':'dihedralNum',
            'dihedral types':'dihedralTypeNum',
            'Imrpopers':'impropers',
            'impropers':'improperNum',
            'improper types':'improperTypeNum',
        }

        for k,v in self.temp_system.items():
            self.world[temp2sys[k]] = v


        atoms = Create.create_atoms(self.temp_system['atom_style'], self.temp_system['Atoms'], returnType='list')

        # add topo
        for b in self.temp_system['Bonds']:
            # b[0] id
            # b[1] type
            clabel = b[2] # center atom id
            plabel = b[3] # pair atom id
            catom = None
            patom = None
            for atom in atoms:
                if atom.label == clabel:
                    catom = atom
                if atom.label == plabel:
                    patom = atom
            
            if catom is None or patom is None:
                raise ValueError('')
            catom.add_neighbors(patom)
        
        mol = self.group_by('lmpdat', atoms, reference='parent')
        # print(mol, mol.values())
        # defaultdict(<class 'emmm.core.molecule.Molecule'>, {'1': < molecule: 1 in None>, '2': < molecule: 2 in None>, '3': < molecule: 3 in None>}) dict_values([< molecule: 1 in None>, < molecule: 2 in None>, < molecule: 3 in None>])
        self.world.items.add_items(mol)

        return mol

    def _read_atoms(self, line):
        line = self._skipblankline(line)        
        if 'Atoms' in line:
            line = self._skipblankline(self._readline())
            Atoms = list()
            while line != '\n' and line != '':
                line = self._deal_with_comment(line.split())
                Atoms.append(line)
                line = self._readline()

            self.temp_system['Atoms'] = Atoms

        return line 

    def _read_bonds(self, line):
        line = self._skipblankline(line)

        if 'Bonds' in line :
            line = self._skipblankline(self._readline())
            Bonds = list()

            while line != '\n' and line != '':
                Bonds.append(self._deal_with_comment(line.split()))
                line = self._readline()
            self.temp_system['Bonds'] = Bonds

        return line

    def _read_angles(self, line):
        line = self._skipblankline(line)
        if 'Angles' in line :
            line = self._skipblankline(self._readline())
            self.Angles = list()

            while line != '\n' and line != '':
                self.Angles.append(self._deal_with_comment(line.split()))
                line = self._readline()

            self.temp_system['Angles'] = self.Angles

        return line

    def _read_dihedrals(self, line):
        line = self._skipblankline(line)
        if 'Dihedrals' in line:
            line = self._skipblankline(self._readline())
            self.Dihedrals = list()

            while line != '\n' and line != '':
                self.Dihedrals.append(self._deal_with_comment(line.split()))
                line = self._readline()

            self.temp_system['Dihedrals'] = self.Dihedrals

        return line

    def _read_impropers(self, line):
        line = self._skipblankline(line)
        if 'Impropers' in line:
            line = self._skipblankline(self._readline())
            self.Impropers = list()

            while line != '\n' and line != '':
                self.Impropers.append(self._deal_with_comment(line.split()))
                line = self._readline()

            self.temp_system['Impropers'] = self.Impropers

        return line


    def _read_velocities(self, line):
        line = self._skipblankline(line)
        if 'Velocities' in line:
            line = self._skipblankline(self._readline())
            self.velocities = list()

            while line != '\n':
                line = self._deal_with_comment(line.split())
                self.velocities.append(line)
                line = self._readline()

            self.temp_system['velocities'] = self.velocities
        return line

    def _read_improper_coeffs(self, line):
        line = self._skipblankline(line)
        if 'Improper' in line and 'Coeffs' in line:
            line = self._skipblankline(self._readline())
            self.improper_coeff = list()

            while line != '\n':
                line = self._deal_with_comment(line.split())
                self.improper_coeff.append(line)
                line = self._readline()

            self.temp_system['improper_coeff'] = self.improper_coeff
        return line

    def _read_dihedral_coeffs(self, line):
        line = self._skipblankline(line)
        if 'Dihedral' in line and 'Coeffs' in line:
            line = self._skipblankline(self._readline())
            self.dihedral_coeffs = list()

            while line != '\n':
                line = self._deal_with_comment(line.split())
                self.dihedral_coeffs.append(line)
                line = self._readline()

            self.temp_system['dihedral_coeffs'] = self.dihedral_coeffs
        return line

    def _read_angle_coeffs(self, line):
        line = self._skipblankline(line)
        if 'Angle' in line and 'Coeffs' in line:
            line = self._skipblankline(self._readline())
            self.angle_coeffs = list()

            while line != '\n':
                line = self._deal_with_comment(line.split())
                self.angle_coeffs.append(line)
                line = self._readline()
            self.temp_system['angle_coeffs'] = self.angle_coeffs
        return line

    def _read_bond_coeffs(self, line):
        line = self._skipblankline(line)        
        if 'Bond' in line and 'Coeffs' in line:
            line = self._skipblankline(self._readline())
            self.bond_coeffs = list()

            while line != '\n':
                line = self._deal_with_comment(line.split())
                self.bond_coeffs.append(line)
                line = self._readline()    
            self.temp_system['bond_coeffs'] = self.bond_coeffs
        return line    

    def _read_pair_coeffs(self, line):
        line = self._skipblankline(line) # /n
        if 'Pair' in line and 'Coeffs' in line:
            line = self._skipblankline(self._readline())
            self.pair_coeffs = list()

            while line != '\n':
                line = self._deal_with_comment(line.split())
                self.pair_coeffs.append(line)
                line = self._readline()
            self.temp_system['pair_coeffs'] = self.pair_coeffs
        return line

    def _read_masses(self, line):
        line = self._skipblankline(line) # Masses
        if 'Masses' in line:
            line = self._skipblankline(self._readline())
            
            self.masses = list()

            while line!= '\n':
                line = self._deal_with_comment(line.split())
                self.masses.append(line)
                line = self._readline()
            self.temp_system['Masses'] = self.masses
            
        return line

    def _read_system(self, line):
        line = self._skipblankline(line)
        def _check_system(line):
            KEYWORDS = ['atoms', 'atom types', 'bonds', 'bond types', 'angles', 'angle types', 'dihedrals', 'dihedral types', 'impropers', 'improper types']

            for k in KEYWORDS:
                if k in line:
                    return k # while 'atom' == while True

            return False

        KEYWORD = _check_system(line)
        while KEYWORD:

            line = self._deal_with_comment(line.split())

            self.temp_system[KEYWORD] = line[0]

            line = self._readline()
            KEYWORD = _check_system(line)
        

        return line

    def _read_bondaries(self, line):

        line = self._skipblankline(line)
        def _check_system(line):
            KEYWORDS = ['xlo', 'ylo', 'zlo']

            for k in KEYWORDS:
                if k in line:
                    return k # while 'atom' == while True

            return False

        KEYWORD = _check_system(line)
        while KEYWORD:
            line = self._deal_with_comment(line.split())
            self.temp_system[KEYWORD] = line[0]
            self.temp_system[line[-1]] = line[1]
            
            line = self._readline()
            KEYWORD = _check_system(line)

        return line
