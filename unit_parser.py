from command import DamageCommand
from mech import Mech
from unit import Unit
from vek import Vek


class UnitParser:
    unit_chars = {'m', 'v', 'u'}

    def __init__(self, grid, width=8, height=8):
        self.string = ""
        self.width = width
        self.height = height
        self.i = 0
        self.xy = 0
        self.grid = grid
        self.map = self.get_map()
        self.fires = []
        self.deathballs = []
        self.spawns = []
        self.mechs = []
        self.veks = []
        self.units = []

    def get_map(self):
        dic = {}
        for i in range(0, self.width):
            for j in range(0, self.height):
                dic[i * self.width + j] = (i, j)
        return dic

    @property
    def char(self):
        return self.string[self.i]

    @property
    def coord(self):
        return self.map[self.xy]

    def get_tile(self):
        char = self.char
        if char == "o":
            self.xy += 1
        elif char == "s":
            #             print(f"add_spawn(Damage({self.coord}))")
            self.spawns.append(self.coord)
            self.xy += 1
        elif char == "d":
            #             print(f"add_deathball(Damage({self.coord}))")
            self.deathballs.append(self.coord)
            self.xy += 1
        elif char == "f":
            #             print(f"add_fire(Damage({self.coord}))")
            self.fires.append(self.coord)
            self.xy += 1
        else:
            raise ValueError(f"{char} not expected, supposed to be o,s,d,or f")

    def spawn_unit(self):
        if self.char == 'm':
            mech = Mech.create(self.grid, *self.get_args())
            self.mechs.append(mech)
            self.grid.gb_place_on_tile(mech, self.coord)
            #             print(f"Mech {self.coord} ({self.get_args()})")
            self.xy += 1

        elif self.char == 'v':
            vek = Vek.create(self.grid, *self.get_args())
            self.veks.append(vek)
            self.grid.gb_place_on_tile(vek, self.coord)
            #             print(f"Vek {self.coord} ({self.get_args()})")
            self.xy += 1

        elif self.char == 'u':
            unit = Unit(*self.get_args())
            self.units.append(unit)
            self.grid.gb_place_on_tile(unit, self.coord)
            #             print(f"Unit {self.coord} ({self.get_args()})")
            self.xy += 1
        else:
            raise ValueError(f"{self.char} not in {self.unit_chars}")

    def get_args(self):
        self.i += 1
        assert self.char == "("
        self.i += 1
        end_index = self.string.find(")", self.i)
        assert end_index != -1, f") expected after index {self.i} in {self.string}"
        capture = self.string[self.i:end_index]
        self.i += len(capture) + 1
        return self.make_numeric(capture.split('_'))

    @staticmethod
    def make_numeric(ls):
        numeric_ls = []
        for item in ls:
            try:
                num = int(item)
                numeric_ls.append(num)
            except ValueError:
                numeric_ls.append(item)
        return numeric_ls

    def skip_until_next_line(self):
        while self.coord[1] != 0:
            self.xy += 1

    def parse_char(self):
        # number-char(empty), number-char(spawn/death/fire), unit_char-(info), /char
        try:
            num = int(self.char)
            self.i += 1
            for _ in range(num):
                self.get_tile()
            self.i += 1
        except ValueError:
            if self.char in self.unit_chars:
                self.spawn_unit()
            elif self.char == "/":
                self.skip_until_next_line()
                self.i += 1
            elif self.char == "~":
                self.xy -= 1
                self.i += 1
            elif self.char == " " or self.char == "\n":
                self.i += 1
            else:
                self.get_tile()
                self.i += 1

    def parse(self):
        while self.i < len(self.string):
            self.parse_char()

    def get_attacks(self):
        attacks = []
        self.veks.sort(key=lambda vek: vek.attack_order)
        for vek in self.veks:
            if vek.direction is not None:
                offset = 1 if vek.offset is None else vek.offset
                attacks.append(vek.attack.attack(vek.direction, offset))
        return attacks

    def run(self):
        self.parse()
        attacks = self.get_attacks()
        end_commands = [DamageCommand(self.grid, coord, 1) for coord in self.fires] + [
            DamageCommand(self.grid, coord, 5) for coord in self.deathballs] + attacks + [
                           DamageCommand(self.grid, coord, 1) for coord in self.spawns]
        self.grid.end_commands = end_commands

    def from_string(self, string):
        self.string = string
        self.run()
        return self.grid
