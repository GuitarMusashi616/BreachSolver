from ability import Artillery, Move, Repair, Cross, Beam
from beam import AcidBeam, UnstableBeam
from shell import ClusterShell, BoulderShell, RegularShell, JumpShell
from unit import Unit


class Mech(Unit):
    def __init__(self, name, max_health=4, health=4, moves=3, is_flying=False):
        super().__init__(name, max_health, health, moves, is_flying)
        self.is_massive = True

    @staticmethod
    def init_mech(mech, grid):
        if mech is None:
            return
        mech.add(Move(mech, grid))
        mech.add(Repair(mech))

    @classmethod
    def create(cls, grid, name, max_health, health, moves):
        # max_health = int(max_health)
        # health = int(health)
        # moves = int(moves)

        mech = Mech(name, max_health, health, moves)
        if name == "Siege Mech":
            mech.add(Artillery(mech, grid, ClusterShell, 2))

        elif name == "Boulder Mech":
            mech.add(Artillery(mech, grid, BoulderShell, 3))

        elif name == "Artillery Mech":
            mech.add(Artillery(mech, grid, RegularShell, 1))

        elif name == "Leap Mech":
            mech.add(Cross(mech, grid, JumpShell, 1))

        elif name == "Nano Mech":
            mech.add(Beam(mech, grid, AcidBeam, 0))

        elif name == "Unstable Mech":
            mech.add(Beam(mech, grid, UnstableBeam, 2))

        if "Mech" in name:
            mech.add(Move(mech, grid))
            mech.add(Repair(mech))

        return mech


