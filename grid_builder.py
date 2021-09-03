from grid import Grid
from tile import TileInst
from tiles import GroundTile
import pandas as pd


class GridBuilder:
    def __init__(self, square_len=8):
        self.tiles = []
        self.units = {}

        self.square_len = square_len
        self.init_all_ground()

    def show(self):
        return pd.DataFrame(self.tiles)

    def init_all_ground(self):
        for i in range(self.square_len):
            square = []
            for j in range(self.square_len):
                square.append(TileInst(GroundTile(), (i, j)))
            self.tiles.append(square)

    def place(self, type_object, coord):
        x, y = coord
        self.tiles[x][y] = TileInst(type_object, coord)

    def place_on_tile(self, unit, coord):
        Grid.place_on_tile(self.tiles, unit, coord)
        Grid.add_to_units(self.units, unit)

    #         if isinstance(unit, Vek):
    #             self.veks.append(unit)

    #         if isinstance(unit, Mech):
    #             self.mechs.append(unit)

    def to_grid(self):
        return Grid(self.tiles, self.units, self.square_len)

