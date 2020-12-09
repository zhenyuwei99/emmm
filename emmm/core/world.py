# author: Roy Kid

from emmm.core.system import System
from emmm.core.topo import Topo
from emmm.core.forcefield import ForceField
from emmm.plugins import PluginManager
from emmm.core.molecule import Molecule

class World:

    def __init__(self):

        # self.forcefield = ForceField()

        self.system = System(self)

        self.forcefield = ForceField(self)

        self.topo  = Topo(self)

        self.molecules = Molecule('world')

        self.pluginManager = PluginManager(self)

    def active_plugin(self, pname):
        """ to instanciate a plugin and return its instance

        Args:
            pname ([str]): [class name of plugin]

        Returns:
            [plugin]: [instance of plugin]
        """

        return self.pluginManager.plugins[pname](self)