from ability import Move, Repair, Artillery, Beam
from beam import VekBeam
from command import CommandDecorator, DamageUnitCommand
from destructable import Destructable
from executor import Executor
from game import Game
from grid_builder import GridBuilder
from shell import ClusterShell, BoulderShell, RegularShell, VekShell
from tiles import WaterTile, MountainTile, GroundTile, CorporateTile, ForestTile, CivilianTile, ForestFireTile, \
    SpawnTile
from unit import Mech, Vek, Unit
from util import Compass


def reset_grid():
    gb = GridBuilder()

    gb.place(WaterTile(), (0, 4))
    gb.place(WaterTile(), (0, 5))
    gb.place(Destructable(MountainTile(), GroundTile(), 3), (0, 6))
    gb.place(Destructable(MountainTile(), GroundTile(), 3), (0, 7))

    gb.place(Destructable(CorporateTile(), GroundTile(), 1), (1, 1))
    gb.place(ForestTile(), (1, 2))
    gb.place(Destructable(CivilianTile(), GroundTile(), 1), (1, 3))
    gb.place(Destructable(CivilianTile(), GroundTile(), 1), (1, 4))
    gb.place(WaterTile(), (1, 5))
    gb.place(WaterTile(), (1, 6))
    gb.place(Destructable(MountainTile(), GroundTile(), 3), (1, 7))

    gb.place(ForestTile(), (2, 3))
    gb.place(Destructable(MountainTile(), GroundTile(), 3), (2, 5))
    gb.place(Destructable(MountainTile(), GroundTile(), 3), (2, 6))
    gb.place(WaterTile(), (2, 7))

    gb.place(Destructable(CivilianTile(), GroundTile(), 1), (3, 1))
    gb.place(WaterTile(), (3, 7))

    gb.place(Destructable(CivilianTile(), GroundTile(), 2), (4, 1))
    gb.place(Destructable(CivilianTile(), GroundTile(), 2), (4, 5))
    gb.place(Destructable(CivilianTile(), GroundTile(), 2), (4, 6))

    gb.place(ForestFireTile(), (5, 1))
    gb.place(ForestFireTile(), (5, 2))
    gb.place(SpawnTile(), (5, 4))
    gb.place(ForestTile(), (5, 7))

    gb.place(Destructable(MountainTile(), GroundTile(), 3), (6, 0))
    gb.place(SpawnTile(), (6, 2))
    gb.place(ForestFireTile(), (6, 3))
    gb.place(ForestFireTile(), (6, 4))

    gb.place(Destructable(MountainTile(), GroundTile(), 3), (7, 0))
    gb.place(Destructable(MountainTile(), GroundTile(), 3), (7, 1))
    gb.place(ForestTile(), (7, 3))
    gb.place(Destructable(MountainTile(), GroundTile(), 3), (7, 7))

    gb.place_on_tile(Mech("Siege Mech", 5, 4), (3, 2))
    gb.place_on_tile(Mech("Artillery Mech", 5, 1), (5, 3))
    gb.place_on_tile(Mech("Boulder Mech", 5, 5, 4), (7, 3))
    gb.place_on_tile(Vek("Psy", 5, 2), (4, 2))
    gb.place_on_tile(Vek("Alpha Firefly", 6, 5, 2), (4, 4))
    gb.place_on_tile(Vek("Scarab", 3, 3), (6, 1))
    gb.place_on_tile(Vek("Firefly", 4, 4, 2), (6, 5))
    gb.place_on_tile(Unit("Boulder", max_health=1, health=1, moves=0), (7, 5))

    grid = gb.to_grid()

    for mech in grid.mechs:
        mech.add(Move(mech, grid))
        mech.add(Repair(mech))

    for vek in grid.veks:
        vek.add(Move(vek, grid))

    siege_mech = grid.units['Siege Mech']
    artillery_mech = grid.units['Artillery Mech']
    boulder_mech = grid.units['Boulder Mech']

    firefly = grid.units['Firefly']
    alpha_firefly = grid.units['Alpha Firefly']
    scarab = grid.units['Scarab']
    psy = grid.units['Psy']

    siege_mech.add(Artillery(siege_mech, grid, ClusterShell, 2))
    boulder_mech.add(Artillery(boulder_mech, grid, BoulderShell, 2))
    artillery_mech.add(Artillery(artillery_mech, grid, RegularShell, 1))

    firefly.add(Beam(firefly, grid, VekBeam, 1))
    alpha_firefly.add(Beam(alpha_firefly, grid, VekBeam, 3))
    scarab.add(Artillery(scarab, grid, VekShell, 1))

    firefly.target = CommandDecorator(firefly, VekBeam(firefly, grid, Compass.NORTH, 1))
    alpha_firefly.target = CommandDecorator(alpha_firefly, VekBeam(alpha_firefly, grid, Compass.NORTH, 3))
    scarab.target = CommandDecorator(scarab, VekShell(scarab, grid, 1, (1, 1)))
    psy.on_death = [DamageUnitCommand(x, 1, grid) for x in grid.veks]

    return grid


if __name__ == "__main__":
    grid = reset_grid()