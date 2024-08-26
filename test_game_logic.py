import unittest
from server.game_logic import Game

class TestGameLogic(unittest.TestCase):

    def test_initialization(self):
        game = Game()
        game.initialize_game()
        self.assertEqual(game.grid[0], ['A-P1', 'A-H1', 'A-P2', 'A-H2', 'A-P3'])
        self.assertEqual(game.grid[4], ['B-P1', 'B-H1', 'B-P2', 'B-H2', 'B-P3'])

    def test_move_character(self):
        game = Game()
        game.initialize_game()

        # Test moving a Pawn forward (valid move)
        self.assertTrue(game.move_character('A', 'P1', 'F'))
        self.assertEqual(game.grid[1][0], 'A-P1')
        self.assertEqual(game.grid[0][0], '')

        # Test moving a Hero1 right (valid move)
        self.assertTrue(game.move_character('B', 'H1', 'R'))
        self.assertEqual(game.grid[4][2], 'B-H1')
        self.assertEqual(game.grid[4][1], '')

        # Test invalid move (out of bounds)
        self.assertFalse(game.move_character('A', 'P1', 'L'))  # Out of bounds
        self.assertEqual(game.grid[1][0], 'A-P1')

        # Test invalid move (moving opponent's piece)
        self.assertFalse(game.move_character('A', 'H1', 'L'))  # 'A' trying to move 'B' piece

        # Test capturing opponent's piece
        game.move_character('A', 'P1', 'F')
        self.assertTrue(game.move_character('A', 'H1', 'R'))
        self.assertTrue(game.move_character('B', 'P1', 'F'))
        self.assertTrue(game.move_character('A', 'H2', 'FR'))  # Capture B's P1
        self.assertEqual(game.grid[3][3], 'A-H2')
        self.assertEqual(game.grid[4][3], '')

        # Test winning condition
        game.grid[4] = ['', '', '', '', '']  # Remove all of B's pieces
        game.check_winner()
        self.assertTrue(game.game_over)
        self.assertEqual(game.winner, 'A')

    def test_hero2_diagonal_movement(self):
        game = Game()
        game.initialize_game()

        # Test Hero2 diagonal movement (valid)
        self.assertTrue(game.move_character('A', 'H2', 'FL'))
        self.assertEqual(game.grid[2][1], 'A-H2')
        self.assertEqual(game.grid[0][3], '')

        # Test Hero2 diagonal movement (invalid, out of bounds)
        self.assertFalse(game.move_character('A', 'H2', 'FL'))  # Out of bounds
        self.assertEqual(game.grid[2][1], 'A-H2')

    def test_turn_order(self):
        game = Game()
        game.initialize_game()

        # Test that turns alternate correctly
        self.assertTrue(game.move_character('A', 'P1', 'F'))
        self.assertEqual(game.current_turn, 'B')
        self.assertTrue(game.move_character('B', 'P1', 'F'))
        self.assertEqual(game.current_turn, 'A')

    def test_friendly_fire_prevention(self):
        game = Game()
        game.initialize_game()

        # Test that a player cannot move onto their own piece
        self.assertFalse(game.move_character('A', 'P1', 'R'))  # A-P1 tries to move onto A-H1
        self.assertEqual(game.grid[0][0], 'A-P1')
        self.assertEqual(game.grid[0][1], 'A-H1')

if __name__ == '__main__':
    unittest.main()
