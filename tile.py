from abc import abstractmethod, ABC


class ITile(ABC):
    @abstractmethod
    def can_move_through(self):
        pass

    @abstractmethod
    def can_fly_through(self):
        pass

    @abstractmethod
    def vek_can_emerge(self):
        pass

    @abstractmethod
    def ground_vek_dies_when_pushed_into(self):
        pass

    @abstractmethod
    def makes_unit_waterlogged(self):
        pass

    @property
    @abstractmethod
    def is_objective_to_protect(self):
        pass

    @abstractmethod
    def damage(self, amount):
        pass

    @property
    @abstractmethod
    def health(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass


class Tile(ITile):
    @property
    def health(self):
        return False

    @health.setter
    def health(self, value):
        pass

    @property
    def is_objective_to_protect(self):
        raise ValueError("Can only call/set this on instance layers of tile")

    def heal(self, amount):
        pass

    def damage(self, amount):
        pass

    def makes_unit_waterlogged(self):
        return False

    def can_move_through(self):
        return True

    def can_fly_through(self):
        return True

    def vek_can_emerge(self):
        return False

    def ground_vek_dies_when_pushed_into(self):
        return False


class TileInst(ITile):
    def __init__(self, type_object, coord):
        self.type_object = type_object  # also acts as a state object
        self.destroyed = None
        self.visitor = None
        self.coord = coord
        self.is_objective_to_protect = False

    def __repr__(self):
        if self.has_no_visitor:
            return repr(self.type_object)
        else:
            return repr(self.visitor)

    @property
    def health(self):
        return self.type_object.health

    @property
    def is_objective_to_protect(self):
        return self._is_objective_to_protect

    @is_objective_to_protect.setter
    def is_objective_to_protect(self, value):
        self._is_objective_to_protect = value

    @property
    def has_no_visitor(self):
        return self.visitor is None or not self.visitor.is_alive

    def place(self, visitor):
        assert self.has_no_visitor, f"Tile {self.coord} already has a unit {self.visitor}"
        self.visitor = visitor

    def can_move_through(self):
        return self.has_no_visitor and self.type_object.can_move_through()

    def can_fly_through(self):
        return self.type_object.can_fly_through()

    def vek_can_emerge(self):
        return self.type_object.vek_can_emerge()

    def ground_vek_dies_when_pushed_into(self):
        return self.type_object.ground_vek_dies_when_pushed_into()

    def makes_unit_waterlogged(self):
        return self.type_object.makes_unit_waterlogged()

    def move_units(self, tile):
        # move this tiles units to tile
        if self.has_no_visitor:
            return

        if not tile.can_move_through():
            return

        tile.visitor = self.visitor
        tile.visitor.coord = tile.coord
        self.visitor = None

        if tile.makes_unit_waterlogged():
            tile.visitor.is_waterlogged = True
        else:
            tile.visitor.is_waterlogged = False

    def push_units(self, tile):
        # self gets pushed into tile
        if self.has_no_visitor:
            return

        if tile.can_move_through():  # no visitor or building/mountain
            self.move_units(tile)
            return

        self.damage(1)
        tile.damage(1)

    def heal(self, amount):  # todo: make this undamage if people start getting raised from the dead (no healing units I think)
        self.type_object.heal(amount)
        if self.visitor:
            self.visitor.health += amount

    def damage(self, amount):
        self.type_object.damage(amount)
        if self.visitor:
            self.visitor.health -= amount