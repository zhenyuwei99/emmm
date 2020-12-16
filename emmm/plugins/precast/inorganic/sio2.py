from emmm.core.create import Create
from emmm.core.molecule import Molecule
from . import InorganicBase

class SiO2(InorganicBase):
    def __init__(self, world) -> None:
        super().__init__(world)
        self.mol = Molecule("SIO")
