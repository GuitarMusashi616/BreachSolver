from tile import ITile
from util import Util


class Destructable(ITile):
    "DestructableTileDecorator Keeps track of health and destruction of tile type object"

    def __init__(self, tile, dead_tile, health):
        self.tile = tile
        self.tile_alive = tile
        self.tile_dead = dead_tile
        self.max_health = health
        self.health = health

    def can_move_through(self):
        return self.tile.can_move_through()

    def vek_can_emerge(self):
        return self.tile.vek_can_emerge()

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = Util.clamp(value, 0, self.max_health)

        if self.tile == self.tile_alive and self._health <= 0:
            self.tile = self.tile_dead

        if self.tile == self.tile_dead and self._health > 0:
            self.tile = self.tile_alive

        self.tile_alive.health = self.health

    def damage(self, amount):
        self.health -= amount

    def heal(self, amount):
        self.health += amount

    def __repr__(self):
        return repr(self.tile)
