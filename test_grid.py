import unittest

from command import CommandDecorator
from dfs import DFS
from dfs_viewer import DFSViewer
from main import reset_grid, reset_grid3


class TestGrid(unittest.TestCase):
    def execute(self, action, name):
        self.assertEqual(name, repr(action))
        choice_before = action.command.__dict__  # relies on using command decorator
        action.execute()
        undo_before = action.command.__dict__
        action.undo()
        self.assertEqual(choice_before, action.command.__dict__)
        action.execute()
        self.assertEqual(undo_before, action.command.__dict__)

    def test_psy_and_artillery_kill_revive(self):
        grid = reset_grid()
        sm = grid.find('Siege Mech')
        move22 = sm.gen_actions()[9]
        self.execute(move22, "MOVE (3, 2) to (2, 2)")
        self.assertEqual(True, grid.find('Psy').is_alive)
        self.assertEqual(True, grid.find('Artillery Mech').is_alive)
        self.assertEqual(grid.find('Psy'), grid.get_tile((4, 2)).visitor)
        self.assertEqual(grid.find('Artillery Mech'), grid.get_tile((5, 3)).visitor)

        shell52 = sm.gen_actions()[4]
        self.execute(shell52, "CLUSTER SHELL at (5, 2)")  # blow up ally and psy
        self.assertEqual(False, grid.find('Psy').is_alive)
        self.assertEqual(False, grid.find('Artillery Mech').is_alive)
        self.assertEqual(None, grid.get_tile((4, 2)).visitor)
        self.assertEqual(None, grid.get_tile((5, 3)).visitor)

        shell52.undo()
        self.assertEqual(True, grid.find('Psy').is_alive)
        self.assertEqual(True, grid.find('Artillery Mech').is_alive)
        self.assertEqual(grid.find('Psy'), grid.get_tile((4, 2)).visitor)
        self.assertEqual(grid.find('Artillery Mech'), grid.get_tile((5, 3)).visitor)

    def test_scarab_kill_revive(self):
        grid = reset_grid()
        sm = grid.find('Siege Mech')
        move02 = sm.gen_actions()[4]
        self.execute(move02, "MOVE (3, 2) to (0, 2)")
        self.assertEqual(True, grid.find('Scarab').is_alive)
        self.assertEqual(grid.find('Scarab'), grid.get_tile((6, 1)).visitor)

        shell62 = sm.gen_actions()[6]
        self.execute(shell62, "CLUSTER SHELL at (6, 2)")  # blow up ally and psy
        self.assertEqual(False, grid.find('Scarab').is_alive)
        self.assertEqual(None, grid.get_tile((6, 1)).visitor)

        shell62.undo()
        self.assertEqual(True, grid.find('Scarab').is_alive)
        self.assertEqual(grid.find('Scarab'), grid.get_tile((6, 1)).visitor)

    def test_summon_boulder(self):
        grid = reset_grid()
        sm = grid.find('Boulder Mech')
        move = sm.gen_actions()[10]
        self.execute(move, "MOVE (7, 3) to (7, 2)")
        shoot = sm.gen_actions()[7]
        self.execute(shoot, "BOULDER SHELL at (5, 2)")
        self.assertEqual(True, grid.find('Boulder 2').is_alive)
        self.assertEqual(grid.find('Boulder 2'), grid.get_tile((5, 2)).visitor)
        shoot.undo()
        self.assertRaises(KeyError, grid.find, 'Boulder 2')
        self.assertEqual(None, grid.get_tile((5, 2)).visitor)
        shoot.execute()
        self.assertEqual(True, grid.find('Boulder 2').is_alive)
        self.assertEqual(grid.find('Boulder 2'), grid.get_tile((5, 2)).visitor)

    def test_vek_charge(self):
        grid = reset_grid3()
        grid.end_commands[7].execute()
        self.assertEqual(grid.find("Beetle"), grid.get_tile((3,3)).visitor)
        self.assertEqual(grid.find("Boulder Mech"), grid.get_tile((2, 3)).visitor)
        self.assertEqual(4, grid.get_tile((2, 3)).visitor.health)

    def test_vek_beam(self):
        grid = reset_grid3()

        self.execute(CommandDecorator(grid.find("Beetle"), grid.end_commands[4]), "VekBeam at (5, 4) heading EAST")
        self.assertEqual(0, grid.get_tile((5,6)).health)

    def test_broken_sequence(self):
        grid = reset_grid3()
        dfs = DFS(grid, 3)

    def test_heal(self):
        # heal when full health
        pass


if __name__ == '__main__':
    unittest.main()