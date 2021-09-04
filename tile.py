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
    def damage(self, amount):
        pass

    @property
    @abstractmethod
    def health(self):
        pass

    # @abstractmethod
    # def deal_damage(self) -> int:
    #     """fire tiles burn visitor, spawn tiles hurt visitor, etc"""
    #     pass

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

    def heal(self, amount):
        pass

    def damage(self, amount):
        pass

    # def deal_damage(self):
    #     return 0

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

    def __repr__(self):
        if self.has_no_visitor:
            return repr(self.type_object)
        else:
            return repr(self.visitor)

    @property
    def health(self):
        return self.type_object.health

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

    def move_units(self, tile):
        # move this tiles units to tile
        if self.has_no_visitor:
            return

        if not tile.can_move_through():
            return

        tile.visitor = self.visitor
        tile.visitor.coord = tile.coord
        self.visitor = None

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

    # def deal_damage(self):
    #     dmg = self.type_object.deal_damage()
    #     self.damage(dmg)
    #     return dmg

    def damage(self, amount):
        self.type_object.damage(amount)
        if self.visitor:
            self.visitor.health -= amount