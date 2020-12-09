# author: Roy Kid
from copy import deepcopy
from emmm.core.operate import Bioperate, Unioperate

class Item(list):

    def __init__(self, label=None, type=None, parent=None, path=None):
        super().__init__()

        self.label = label
        self.type = type
        self.parent = parent
        self.path = path

    @property
    def id(self):
        return self.id

    
        

    @property
    def coords(self):
        return self.coords
    @coords.setter
    def coords(self, value):
        self.coords = value
        self.x = self.coords[0]
        self.y = self.coords[1]
        self.z = self.coords[2]

    @property
    def x(self):
        return self.coords[0]
    @x.setter
    def x(self, x):
        self.coord[0] = x

    @property
    def y(self):
        return self.coords[1]
    @y.setter
    def y(self, y):
        self.coord[1] = y
    
    @property
    def z(self):
        return self.coords[2]
    @z.setter
    def z(self, z):
        self.coords[2] = z

    def move(self, x, y, z):
        Unioperate.move(self, x, y, z)

    def ranmove(self, distance):
        Unioperate.randmove(self, distance)

    def get_replica(self, newLabel):
        
        newItem = deepcopy(self)
        newItem.label = newLabel
        return newItem



    