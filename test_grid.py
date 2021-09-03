import unittest
from main import reset_grid

class TestGrid(unittest.TestCase):
    def execute(self, action, name):
        self.assertEqual(name, repr(action))
        choice_before = action.command.__dict__.copy()  # relies on using command decorator
        action.execute()
        undo_before = action.command.__dict__.copy()
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


if __name__ == '__main__':
    unittest.main()
