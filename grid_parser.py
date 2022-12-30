from destructable import Destructable
from grid_builder import GridBuilder
from tiles import WaterTile, MountainTile, GroundTile, CivilianTile, ForestTile


class GridParser:
    def __init__(self, string, width=8, height=8):
        self.string = string.lower()
        self.width = width
        self.height = height
        self.xy = 0
        self.i = 0
        self.gb = GridBuilder()
        self.map = self.get_map()

    def get_map(self):
        dic = {}
        for i in range(0, self.width):
            for j in range(0, self.height):
                dic[i*self.width+j] = (i, j)
        return dic

    def get_tile(self):
        char = self.string[self.i]
        if char == "g":
            return GroundTile()
        elif char == 'f':
            return ForestTile()
        elif char == "w":
            return WaterTile()
        elif char == "m":
            return Destructable(MountainTile(), GroundTile(), 3)
        elif char == "-":
            return Destructable(CivilianTile(), GroundTile(), 1)
        elif char == "=":
            return Destructable(CivilianTile(), GroundTile(), 2)
        else:
            raise ValueError(f"{char} is not a valid token in {self.string}")

    def skip_to_next_row(self):
        while self.map[self.xy][1] != 0:
            self.xy += 1

    def parse_char(self):
        num = 1
        if self.string[self.i] == "/":
            self.skip_to_next_row()
            self.i += 1
            return
        elif self.string[self.i] == " " or self.string[self.i] == "\n":
            self.i += 1
            return
        try:
            num = int(self.string[self.i])
            self.i += 1
        except ValueError:
            pass

        self.place_multiple(num)
        self.i += 1

    def parse(self):
        while self.i < len(self.string):
            self.parse_char()

    def place_multiple(self, num):
        for _ in range(num):
            tile = self.get_tile()
            assert tile, f"{tile} is not a tile"
            x, y = self.map[self.xy]
            self.gb.place(tile, (x, y))
            self.xy += 1

    def to_grid(self):
        return self.gb.to_grid()

    @classmethod
    def from_string(cls, string, width=8, height=8):
        gp = cls(string, width, height)
        gp.parse()
        return gp.to_grid()


if __name__ == "__main__":
    GridParser.from_string("2w2g=m2w/gw=4gw/6gm/6g=/wg=5g/=5gmg/4g=g=wmw5gw")