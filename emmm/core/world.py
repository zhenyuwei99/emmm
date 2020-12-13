# author: Roy Kid

from emmm.core.topo import Topo
from emmm.core.forcefield import ForceField
from emmm.plugins import PluginManager
from emmm.core.molecule import Molecule

class World:

    def __init__(self, unit):
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
            'masses', 
            'items',
            'atoms', # raw info of each atom
            'atomNum', # the number of atoms 
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
            'topo',
            'topoBond', 
            'topoAngle', 
            'topoDihedral',
            'forcefield',
        
        ]

        self._world = dict()

        self.forcefield = ForceField(self)

        self.topo  = Topo(self)

        self.items = Molecule('world')

        self.pluginManager = PluginManager(self)

    def __getitem__(self, k):
        return self._world[k]

    def __setitem__(self, k, v):
        if k not in self.limitedKeys:
            raise KeyError('World has no %s keyword'%k)
        self._world[k] = v

    def active_plugin(self, pname):
        """ to instanciate a plugin and return its instance

        Args:
            pname ([str]): [class name of plugin]

        Returns:
            [plugin]: [instance of plugin]
        """

        return self.pluginManager.plugins[pname](self)

    def vis(self):
        out = self.active_plugin('OUTjson')
        json = out.dump_data()
        import eel
        eel.init('/home/roy/Work/emmm/emmm/vis')
        eel.readDataInJs(json)
        eel.start('atom-sim.html', mode='chrome')