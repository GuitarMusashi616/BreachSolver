import unittest

from command import CommandDecorator
from dfs import DFS
from dfs_viewer import DFSViewer
from grid_parser import GridParser
from main import *
from unit_parser import UnitParser


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
        self.assertEqual(3, grid.get_tile((2, 3)).visitor.health)

    def test_vek_beam(self):
        grid = reset_grid3()

        self.execute(CommandDecorator(grid.find("Beetle"), grid.end_commands[4]), "VekBeam at (5, 4) heading EAST")
        self.assertEqual(0, grid.get_tile((5,6)).health)

    def test_vek_web(self):
        grid = reset_grid4()

        self.assertEqual({}, grid.find("Boulder Mech").gen_actions())

        act = grid.find("Artillery Mech").gen_actions()[19]
        act.execute()

        shoot = grid.find("Artillery Mech").gen_actions()[4]
        shoot.execute()

        self.assertNotEqual({}, grid.find("Boulder Mech").gen_actions())

        shoot.undo()

        self.assertEqual({}, grid.find("Boulder Mech").gen_actions())

        shoot.execute()

        self.assertNotEqual({}, grid.find("Boulder Mech").gen_actions())

        shoot.undo()

        self.assertEqual({}, grid.find("Boulder Mech").gen_actions())

        shoot = grid.find("Artillery Mech").gen_actions()[5]
        shoot.execute()

        self.assertNotEqual({}, grid.find("Boulder Mech").gen_actions())

        shoot.undo()

        self.assertEqual({}, grid.find("Boulder Mech").gen_actions())

        shoot.execute()

        self.assertNotEqual({}, grid.find("Boulder Mech").gen_actions())

        shoot.undo()

        self.assertEqual({}, grid.find("Boulder Mech").gen_actions())

    def test_broken_sequence(self):
        grid = reset_grid3()
        dfs = DFS(grid, 3)

    def test_heal(self):
        # heal when full health
        pass

    def test_death_mechs(self):
        def renfield2():
            grid = GridParser.from_string("2w2g=m2w/gw=4gw/7gm/7g=/wg=5g/=5gmg/4g=g=w/mw5gw")
            return UnitParser(grid).from_string("""
            /
            ov(Alpha Hornet_4_4_#5_E)od-m(Artillery Mech_5_5_4)/
            6od-m(Siege Mech_5_5_3)/
            d-m(Boulder Mech_5_5_4)3om(Renfield Bomb_4_4_0)/
            7os/
            2ov(Hornet_2_2_#4_N)fv(Hornet_2_2_#7_S)s/
            3ov(Beetle Leader_6_6_#3_N)ov(Psion Tyrant_2_2_#6)
            """)
        grid = renfield2()
        dfs = DFS(grid, 5)


if __name__ == '__main__':
    # unittest.main()
    TestGrid().test_death_mechs()