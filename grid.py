from abc import ABC, abstractmethod
import pandas as pd

from mech import Mech
from vek import Vek


class IGrid(ABC):
    @abstractmethod
    def get_tile(self, coord):
        pass

    #     @abstractmethod
    #     def push(self, coord, dcoord):
    #         pass

    @abstractmethod
    def get_movable_tiles(self, coord, moves, is_flying):
        pass

    @abstractmethod
    def get_artillery_tiles(self, coord):
        pass

    @abstractmethod
    def get_full_col_and_row(self, coord):
        pass


class Grid(IGrid):
    def __init__(self, tiles, units, square_len=8):
        self.tiles = tiles  # top left is 0,0
        #         self.mechs = mechs
        #         self.veks = veks
        self.units = units
        self.square_len = square_len
        self.end_commands = []

    def show(self):
        return pd.DataFrame(self.tiles)

    @property
    def mechs(self):
        return [v for k, v in self.units.items() if isinstance(v, Mech) and v.is_alive]

    @property
    def veks(self):
        return [v for k, v in self.units.items() if isinstance(v, Vek) and v.is_alive]

    @property
    def veks_in_order(self):
        return self.veks.sort(key=lambda x: x.attack_order)

    def find(self, unit_name):
        return self.units[unit_name]

    #     def show_coords(self, coords):
    #         terrain = self.show()
    #         for x,y in coords:
    #             terrain[x][y] = "TARGET"
    #         return terrain

    #     def show_movable(self, coord, moves):
    #         terrain = self.show()
    #         for x,y in grid.get_movable_tiles(coord, moves):
    #             terrain[x][y] = "MOVABLE"
    #         i,j = coord
    #         terrain[i][j] = "ORIGIN"
    #         return terrain

    def can_move_through(self, coord):
        try:
            return self.get_tile(coord).can_move_through()
        except IndexError:
            return False

    def can_fly_through(self, coord):
        try:
            return self.get_tile(coord).can_fly_through()
        except IndexError:
            return False

    def gb_place_on_tile(self, unit, coord):
        self.place_on_tile(self.tiles, unit, coord)
        self.add_to_units(self.units, unit)

    @staticmethod
    def place_on_tile(tiles, unit, coord):
        x, y = coord
        tile_inst = tiles[x][y]
        #         unit = Killable(unit, tile_inst)
        tile_inst.place(unit)
        unit.coord = coord

    @staticmethod
    def add_to_units(units, unit):  # will only work up to 9 ie no Scarab 10
        while unit.name in units:
            try:
                num = int(unit.name[-1])
                unit.name = unit.name[:-1] + str(num + 1)
            except ValueError:
                unit.name = unit.name + " 2"

        units[unit.name] = unit

    def summon(self, unit, coord):
        self.place_on_tile(self.tiles, unit, coord)
        self.add_to_units(self.units, unit)

    def unsummon(self, unit, coord):
        tile = self.get_tile(coord)
        if tile.visitor == unit:
            tile.visitor = None
        del self.units[unit.name]

    #     def push(self, coord, dcoord):
    #         assert dcoord in {(-1,0),(1,0),(0,-1),(0,1)}, f"{dcoord} is an invalid direction vector"
    #         x, y = coord
    #         dx, dy = dcoord

    #         nx, ny = x+dx, y+dy
    #         try:
    #             self.tiles[x][y].push_units(self.tiles[nx][ny])
    #         except IndexError:
    #             pass

    def damage(self, coord, amount=1):
        self.get_tile(coord).damage(amount)

    def get_tile(self, coord):
        x, y = coord
        if not 0 <= x < self.square_len or not 0 <= y < self.square_len:
            raise IndexError(f"{coord} is out of range of grid ({self.square_len}x{self.square_len})")
        return self.tiles[x][y]

    def get_movable_tiles(self, coord, moves, is_flying):
        if not is_flying:
            return self.get_neighboring_tiles(coord, moves, self.can_move_through)
        tiles = self.get_neighboring_tiles(coord, moves, self.can_fly_through)
        return {tile for tile in tiles if self.get_tile(tile).can_move_through() and self.get_tile(tile).visitor is None}

    def get_neighboring_tiles(self, coord, moves, condition=lambda coord: True):
        explored = {coord}
        queue = [coord]

        for i in range(moves):
            queue = self.get_neighbors(queue, explored, condition)

        return explored

    def get_neighbors(self, queue, explored, condition=lambda coord: True):
        new_queue = []
        while queue:
            x, y = queue.pop()
            for dy, dx in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                if x+dx < 0 or self.square_len <= x+dx or y+dy < 0 or self.square_len <= y+dy:
                    continue
                new_coord = (x + dx, y + dy)
                if new_coord not in explored:
                    if condition(new_coord):
                        new_queue.append(new_coord)
                        explored.add(new_coord)
        return new_queue

    def get_artillery_tiles(self, coord):
        full_col_and_row = self.get_full_col_and_row(coord)

        exclude = self.get_neighboring_tiles(coord, 1)

        return [x for x in full_col_and_row if x not in exclude]

    def get_full_col_and_row(self, coord):
        i, j = coord
        full_col = self.get_full_col(i)
        full_row = self.get_full_row(j)
        return full_col+full_row

    def get_full_col(self, i):
        return [(i, j) for j in range(self.square_len)]

    def get_full_row(self, j):
        return [(i, j) for i in range(self.square_len)]
