# author: Roy Kid


class PrecastBase:

    def __init__(self, world) -> None:
        self.world = world
        self.system = world.system