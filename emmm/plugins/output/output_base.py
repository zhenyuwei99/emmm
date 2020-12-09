# author: Roy Kid
class OutputBase:
    """ The parent class for all the input parser
    """
    def __init__(self, world):
        self.world = world
        self.system = world.system
    
    def search_topo(self, isBond=True, isAngle=True, isDihedral=True):
        for item in self.world.molecules:
            self.world.topo.search_topo(item, isBond, isAngle, isDihedral)