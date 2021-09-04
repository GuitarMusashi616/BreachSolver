from ability import Move, Repair, Artillery, Beam, Melee
from beam import VekBeam, VekCharge
from command import CommandDecorator, DamageUnitCommand, DamageCommand
from destructable import Destructable
from executor import Executor
from game import Game
from grid_builder import GridBuilder
from melee import VekMelee
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

    siege_mech     = Mech("Siege Mech", 5, 4)
    artillery_mech = Mech("Artillery Mech", 5, 1)
    boulder_mech   = Mech("Boulder Mech", 5, 5, 4)

    firefly       = Vek("Firefly", 4, 4, 2)
    alpha_firefly = Vek("Alpha Firefly", 6, 5, 2)
    scarab        = Vek("Scarab", 3, 3)
    psy           = Vek("Psy", 5, 2)

    gb.place_on_tile(siege_mech, (3, 2))
    gb.place_on_tile(artillery_mech, (5, 3))
    gb.place_on_tile(boulder_mech, (7, 3))
    gb.place_on_tile(psy, (4, 2))
    gb.place_on_tile(alpha_firefly, (4, 4))
    gb.place_on_tile(scarab, (6, 1))
    gb.place_on_tile(firefly, (6, 5))
    gb.place_on_tile(Unit("Boulder", max_health=1, health=1, moves=0), (7, 5))

    grid = gb.to_grid()

    for mech in grid.mechs:
        mech.add(Move(mech, grid))
        mech.add(Repair(mech))

    for vek in grid.veks:
        vek.add(Move(vek, grid))

    siege_mech.add(Artillery(siege_mech, grid, ClusterShell, 2))
    boulder_mech.add(Artillery(boulder_mech, grid, BoulderShell, 2))
    artillery_mech.add(Artillery(artillery_mech, grid, RegularShell, 1))

    firefly.add(Beam(firefly, grid, VekBeam, 1))
    alpha_firefly.add(Beam(alpha_firefly, grid, VekBeam, 3))
    scarab.add(Artillery(scarab, grid, VekShell, 1))

    firefly.target = CommandDecorator(firefly, VekBeam(firefly, grid, Compass.NORTH, 1))
    alpha_firefly.target = CommandDecorator(alpha_firefly, VekBeam(alpha_firefly, grid, Compass.NORTH, 3))
    scarab.target = CommandDecorator(scarab, VekShell(scarab, grid, 1, (1, 1)))
    # psy.on_death = [DamageUnitCommand(x, 1, grid) for x in grid.veks]

    return grid


def reset_grid2():
    gb = GridBuilder()

    gb.place(WaterTile(), (0, 4))
    gb.place(WaterTile(), (0, 5))
    gb.place(Destructable(MountainTile(), GroundTile(), 3), (0, 6))
    gb.place(Destructable(MountainTile(), GroundTile(), 3), (0, 7))

    gb.place(Destructable(CorporateTile(), GroundTile(), 1), (1, 1))
    gb.place(ForestTile(), (1, 2))
    gb.place(Destructable(CivilianTile(), GroundTile(), 1), (1, 3))
    gb.place(GroundTile(), (1, 4))
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

    siege_mech = Mech("Siege Mech", 5, 4, 3)
    artillery_mech = Mech("Artillery Mech", 5, 1, 3)
    boulder_mech = Mech("Boulder Mech", 5, 5, 4)

    firefly = Vek("Firefly", 4, 2, 2)
    alpha_firefly = Vek("Alpha Firefly", 6, 2, 2)

    hornet = Vek("Hornet", 2, 2, 5, True)
    alpha_hornet = Vek("Alpha Hornet", 4, 4, 5, True)

    gb.place_on_tile(siege_mech, (1, 2))
    gb.place_on_tile(artillery_mech, (6, 1))
    gb.place_on_tile(boulder_mech, (7, 2))
    gb.place_on_tile(alpha_firefly, (5, 3))
    gb.place_on_tile(firefly, (4, 4))
    gb.place_on_tile(hornet, (3, 2))
    gb.place_on_tile(alpha_hornet, (1, 4))
    gb.place_on_tile(Unit("Boulder", max_health=1, health=1, moves=0), (7, 5))

    grid = gb.to_grid()

    for mech in grid.mechs:
        mech.add(Move(mech, grid))
        mech.add(Repair(mech))

    for vek in grid.veks:
        vek.add(Move(vek, grid))

    siege_mech.add(Artillery(siege_mech, grid, ClusterShell, 2))
    boulder_mech.add(Artillery(boulder_mech, grid, BoulderShell, 2))
    artillery_mech.add(Artillery(artillery_mech, grid, RegularShell, 1))

    firefly.add(Beam(firefly, grid, VekBeam, 1))
    alpha_firefly.add(Beam(alpha_firefly, grid, VekBeam, 3))
    hornet.add(Melee(hornet, grid, VekMelee, 1))
    alpha_hornet.add(Melee(alpha_hornet, grid, VekMelee, 2, 2))

    firefly.target = CommandDecorator(firefly, VekBeam(firefly, grid, Compass.WEST, 1))
    alpha_firefly.target = CommandDecorator(alpha_firefly, VekBeam(alpha_firefly, grid, Compass.NORTH, 3))
    hornet.target = CommandDecorator(alpha_firefly, VekMelee(hornet, grid, Compass.WEST, 1))
    alpha_hornet.target = CommandDecorator(alpha_firefly, VekMelee(alpha_hornet, grid, Compass.WEST, 2, 2))
    # psy.on_death = [DamageUnitCommand(x, 1, grid) for x in grid.veks]

    return grid


def reset_grid3():
    gb = GridBuilder()

    gb.place(WaterTile(), (0, 0))
    gb.place(WaterTile(), (0, 1))
    gb.place(Destructable(MountainTile(), GroundTile(), 3), (0, 2))
    gb.place(Destructable(CivilianTile(), GroundTile(), 2), (0, 3))
    gb.place(Destructable(MountainTile(), GroundTile(), 3), (0, 6))
    gb.place(Destructable(MountainTile(), GroundTile(), 3), (0, 7))

    gb.place(WaterTile(), (1, 0))
    gb.place(Destructable(CivilianTile(), GroundTile(), 2), (1, 2))
    gb.place(Destructable(CivilianTile(), GroundTile(), 2), (1, 3))
    gb.place(Destructable(MountainTile(), GroundTile(), 3), (1, 6))
    gb.place(Destructable(MountainTile(), GroundTile(), 3), (1, 7))

    gb.place(Destructable(MountainTile(), GroundTile(), 3), (4, 0))
    gb.place(Destructable(CivilianTile(), GroundTile(), 2), (4, 1))
    gb.place(Destructable(CivilianTile(), GroundTile(), 2), (4, 6))
    gb.place(WaterTile(), (4, 7))

    gb.place(Destructable(CivilianTile(), GroundTile(), 2), (5, 1))
    gb.place(Destructable(CivilianTile(), GroundTile(), 2), (5, 6))
    gb.place(WaterTile(), (5, 7))

    gb.place(WaterTile(), (6, 0))
    gb.place(Destructable(MountainTile(), GroundTile(), 3), (6, 1))
    gb.place(WaterTile(), (7, 0))

    gb.place(WaterTile(), (2, 6))
    gb.place(WaterTile(), (3, 6))
    gb.place(WaterTile(), (3, 5))
    gb.place(WaterTile(), (3, 4))

    siege_mech = Mech("Siege Mech", 5, 5, 3)
    artillery_mech = Mech("Artillery Mech", 5, 5, 4)
    boulder_mech = Mech("Boulder Mech", 5, 5, 4)

    firefly = Vek("Firefly", 4, 2, 2)
    alpha_firefly = Vek("Alpha Firefly", 5, 5, 2)

    hornet = Vek("Hornet", 2, 2, 5, True)
    alpha_hornet = Vek("Alpha Hornet", 4, 4, 5, True)

    scarab = Vek("Scarab", 2, 2)
    alpha_scarab = Vek("Alpha Scarab", 4, 4)

    beetle = Vek("Beetle", 4, 4, 2)

    blobber = Vek("Blobber", 3, 3, 2)
    blob = Unit("Blob", 1, 1, 0)

    gb.place_on_tile(siege_mech, (3, 2))
    gb.place_on_tile(boulder_mech, (2, 3))
    gb.place_on_tile(artillery_mech, (2, 5))

    gb.place_on_tile(alpha_firefly, (5, 4))
    gb.place_on_tile(scarab, (6, 6))
    gb.place_on_tile(alpha_scarab, (6, 2))
    gb.place_on_tile(beetle, (6, 3))

    grid = gb.to_grid()

    for mech in grid.mechs:
        mech.add(Move(mech, grid))
        mech.add(Repair(mech))

    for vek in grid.veks:
        vek.add(Move(vek, grid))

    siege_mech.add(Artillery(siege_mech, grid, ClusterShell, 2))
    boulder_mech.add(Artillery(boulder_mech, grid, BoulderShell, 3))
    artillery_mech.add(Artillery(artillery_mech, grid, RegularShell, 1))

    grid.end_commands = [
        DamageCommand(grid, (1, 5), 5),
        DamageCommand(grid, (3, 2), 5),
        DamageCommand(grid, (5, 5), 5),
        DamageCommand(grid, (6, 1), 5),
        VekBeam(alpha_firefly, grid, Compass.EAST, 3),
        VekShell(scarab, grid, 1, (4, 6)),
        VekShell(alpha_scarab, grid, 3, (1, 2)),
        VekCharge(beetle, grid, Compass.NORTH, 1),
        DamageCommand(grid, (6, 4), 1),
        DamageCommand(grid, (5, 2), 1),
        DamageCommand(grid, (7, 5), 1),
    ]

    return grid


if __name__ == "__main__":
    grid = reset_grid()