class Color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


class Compass:
    NORTH = (-1, 0)
    SOUTH = (1, 0)
    EAST = (0, 1)
    WEST = (0, -1)
    FACES = [NORTH, SOUTH, EAST, WEST]

    @classmethod
    def match(cls, coord):
        for k, v in cls.__dict__.items():
            if v == coord:
                return k

    @classmethod
    def get_direction(cls, from_coord, to_coord):
        "finds the unit vector pointing from_coord to_coord, should point north, south, east, west"
        xf, yf = to_coord
        xi, yi = from_coord

        deltas = [xf - xi, yf - yi]
        assert xf - xi == 0 or yf - yi == 0, f"{from_coord} to {to_coord} is not perpendicular"

        return tuple(delta // abs(delta) if delta != 0 else 0 for delta in deltas)


class Util:
    @staticmethod
    def clamp(a,low,high):
        return max(low, min(a, high))

    @staticmethod
    def assertEqual(expected, actual):
        assert expected == actual, f"Expected: {expected}, Actual: {actual}"