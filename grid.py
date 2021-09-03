from abc import ABC, abstractmethod
import pandas as pd

from unit import Mech, Vek


class IGrid(ABC):
    @abstractmethod
    def get_tile(self, coord):
        pass

    #     @abstractmethod
    #     def push(self, coord, dcoord):
    #         pass

    @abstractmethod
    def get_movable_tiles(self, coord, moves):
        pass

    @abstractmethod
    def get_artillery_tiles(self, coord):
        pass


class Grid(IGrid):
    def __init__(self, tiles, units, square_len=8):
        self.tiles = tiles  # top left is 0,0
        #         self.mechs = mechs
        #         self.veks = veks
        self.units = units
        self.square_len = square_len

    def show(self):
        return pd.DataFrame(self.tiles)

    @property
    def mechs(self):
        return [v for k,v in self.units.items() if isinstance(v, Mech) and v.is_alive]

    @property
    def veks(self):
        return [v for k,v in self.units.items() if isinstance(v, Vek) and v.is_alive]

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
        x, y = coord
        try:
            return self.tiles[x][y].can_move_through()
        except IndexError:
            return False

    @staticmethod
    def place_on_tile(tiles, unit, coord):
        x, y = coord
        tile_inst = tiles[x][y]
        #         unit = Killable(unit, tile_inst)
        tile_inst.place(unit)
        unit.coord = coord

    @staticmethod
    def add_to_units(units, unit):
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
        x, y = coord
        self.tiles[x][y].damage(amount)

    def get_tile(self, coord):
        x, y = coord
        return self.tiles[x][y]

    def get_movable_tiles(self, coord, moves):
        return self.get_neighboring_tiles(coord, moves, self.can_move_through)

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
                new_coord = (x + dx, y + dy)
                if new_coord not in explored:
                    if condition(new_coord):
                        new_queue.append(new_coord)
                        explored.add(new_coord)
        return new_queue

    def get_artillery_tiles(self, coord):
        i, j = coord
        full_col = self.get_full_col(i)
        full_row = self.get_full_row(j)

        exclude = self.get_neighboring_tiles(coord, 1)

        return [x for x in full_row + full_col if x not in exclude]

    def get_full_col(self, i):
        return [(i, j) for j in range(self.square_len)]

    def get_full_row(self, j):
        return [(i, j) for i in range(self.square_len)]
