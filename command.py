from abc import ABC, abstractmethod

from util import Compass


class ICommand(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass


class NullCommand(ICommand):
    def execute(self):
        super().execute()

    def undo(self):
        super().execute()


class MoveCommand(ICommand):
    def __init__(self, grid, unit_coord, to_coord):
        self.grid = grid
        self.unit_coord = unit_coord
        self.to_coord = to_coord

    def __repr__(self):
        return f"MOVE {self.unit_coord} to {self.to_coord}"

    def execute(self):
        unit_tile = self.grid.get_tile(self.unit_coord)
        to_tile = self.grid.get_tile(self.to_coord)
        unit_tile.move_units(to_tile)

    def undo(self):
        unit_tile = self.grid.get_tile(self.unit_coord)
        to_tile = self.grid.get_tile(self.to_coord)
        to_tile.move_units(unit_tile)


class HealCommand(ICommand):
    def __init__(self, unit, amount):
        self.unit = unit
        self.amount = amount

    def __repr__(self):
        return f"HEAL +{self.amount}"

    def execute(self):
        if self.unit.at_max_health:
            self.healed_amount = 0
            return

        self.unit.health += self.amount
        self.healed_amount = self.amount

    def undo(self):
        assert self.healed_amount is not None, "has yet to heal"
        self.unit.health -= self.healed_amount


class DamageCommand(ICommand):
    def __init__(self, grid, coord, amount):
        self.grid = grid
        self.coord = coord
        self.amount = amount

    def __repr__(self):
        return f"DAMAGE {self.coord} -{self.amount}"

    def execute(self):
        try:
            tile = self.grid.get_tile(self.coord)
            tile.damage(self.amount)
        except IndexError:
            pass

    def undo(self):
        try:
            tile = self.grid.get_tile(self.coord)
            tile.heal(self.amount)
        except IndexError:
            pass


class DamageUnitCommand(ICommand):
    def __init__(self, unit, amount):
        self.unit = unit
        self.amount = amount

    def __repr__(self):
        return f"DAMAGE {self.unit} -{self.amount}"

    def execute(self):
        self.unit.health -= self.amount

    def undo(self):
        self.unit.health += self.amount


class PushCommand(ICommand):
    def __init__(self, grid, coord, direction):
        self.grid = grid
        self.coord = coord
        self.direction = direction
        self.unit_pushed = None
        self.tiles_damaged = None

    def __repr__(self):
        return f"PUSH {self.coord} to {Compass.match(self.direction)}"

    def get_dest_tile(self):
        "The tile that the unit is pushed onto"
        x, y = self.coord
        dx, dy = self.direction
        new_coord = (x + dx, y + dy)

        try:
            new_tile = self.grid.get_tile(new_coord)
        except IndexError:
            return

        return new_tile

    def execute(self):
        try:
            tile = self.grid.get_tile(self.coord)
        except IndexError:
            return

        if tile.visitor is None:
            return  # does nothing when no unit is on tile

        new_tile = self.get_dest_tile()
        if new_tile is None:
            return  # does nothing when dest tile is out of bounds

        self.unit_pushed = tile.visitor
        if not new_tile.can_move_through():
            self.tiles_damaged = True  # saves that tiles have been damaged if unit collides when pushed

        tile.push_units(new_tile)

    def undo(self):
        if self.unit_pushed is None:
            return  # does nothing unless a unit was pushed previously

        try:
            origin_tile = self.grid.get_tile(self.coord)
            dest_tile = self.get_dest_tile()
        except IndexError:
            return

        if self.tiles_damaged:  # just heal both tiles if collision happened
            origin_tile.heal(1)
            dest_tile.heal(1)
            return

        dest_tile.push_units(origin_tile)  # otherwise push the unit back


class SummonCommand(ICommand):
    def __init__(self, unit, grid, coord):
        self.unit = unit
        self.grid = grid
        self.coord = coord

    def __repr__(self):
        return f"SUMMON {self.unit} at {self.coord}"

    def execute(self):
        self.grid.summon(self.unit, self.coord)

    def undo(self):
        self.grid.unsummon(self.unit, self.coord)


class CompositeCommand(ICommand):
    def __init__(self, commands):
        self.commands = commands

    def __repr__(self):
        return repr(self.commands)

    def add(self, command):
        self.commands.append(command)

    def extend(self, commands):
        self.commands.extend(commands)

    def execute(self):
        for command in self.commands:
            command.execute()

    def undo(self):
        for command in self.commands[::-1]:
            command.undo()


class PushAwayCommand(CompositeCommand):
    def __init__(self, grid, coord, faces=Compass.FACES):
        commands = []
        x, y = coord
        for dx, dy in faces:
            commands.append(PushCommand(grid, (x + dx, y + dy), (dx, dy)))
        super().__init__(commands)


class SpawnCommand(ICommand):
    def __init__(self, grid, coord, new_unit):
        self.grid = grid
        self.coord = coord
        self.new_unit = new_unit
        self.executed_command = None

    def execute(self):
        tile = self.grid.get_tile(self.coord)
        assert tile.vek_can_emerge(), "vek cannot spawn from this tile"
        if tile.visitor is None:
            self.executed_command = SummonCommand(self.new_unit, self.grid, self.coord)
        else:
            self.executed_command = DamageUnitCommand(tile.visitor, 1)
        self.executed_command.execute()

    def undo(self):
        assert self.executed_command is not None, "SpawnCommand yet to be activated"
        self.executed_command.undo()

    def __repr__(self):
        return f"SPAWNING {self.new_unit} at {self.coord}"


class CommandDecorator(ICommand):
    "Keeps track of whether command has been executed already or not, also updates unit state based on if command has been executed"

    def __init__(self, unit, command):
        self.unit = unit
        self.command = command
        self.executed = False

    def __repr__(self):
        return repr(self.command)

    def execute(self):
        assert not self.executed, f"{self} has already been executed"
        self.command.execute()
        if isinstance(self.command, MoveCommand):
            self.unit.has_moved = True
        else:
            self.unit.has_fired = True
        self.executed = True

    def undo(self):
        assert self.executed, f"Cannot undo unexecuted {self}"
        self.command.undo()
        if isinstance(self.command, MoveCommand):
            self.unit.has_moved = False
        else:
            self.unit.has_fired = False
        self.executed = False
