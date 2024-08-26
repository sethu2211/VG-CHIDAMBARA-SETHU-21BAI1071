import unittest
from flask_socketio import SocketIOTestClient
from server.app import app, socketio

class TestWebSocket(unittest.TestCase):

    def setUp(self):
        self.client = SocketIOTestClient(app, socketio)

    def tearDown(self):
        self.client.disconnect()

    def test_connect(self):
        self.assertTrue(self.client.is_connected())

    def test_game_init(self):
        self.client.emit('game_init', {})
        received = self.client.get_received()
        self.assertEqual(len(received), 1)
        self.assertIn('game_state_update', received[0]['name'])
        self.assertIn('grid', received[0]['args'][0])

    def test_player_move(self):
        # Initialize game
        self.client.emit('game_init', {})
        received = self.client.get_received()

        # Player A moves Pawn 1 forward
        self.client.emit('player_move', {'player': 'A', 'character': 'P1', 'move': 'F'})
        received = self.client.get_received()
        self.assertEqual(len(received), 2)
        self.assertIn('game_state_update', received[1]['name'])

        # Check that the move was executed correctly
        grid_update = received[1]['args'][0]['grid']
        self.assertEqual(grid_update[1][0], 'A-P1')
        self.assertEqual(grid_update[0][0], '')

        # Player B tries an invalid move (out of bounds)
        self.client.emit('player_move', {'player': 'B', 'character': 'H1', 'move': 'L'})
        received = self.client.get_received()
        self.assertEqual(len(received), 3)
        self.assertIn('invalid_move', received[2]['name'])

        # Player B makes a valid move
        self.client.emit('player_move', {'player': 'B', 'character': 'P1', 'move': 'F'})
        received = self.client.get_received()
        self.assertEqual(len(received), 4)
        self.assertIn('game_state_update', received[3]['name'])

        # Check that the move was executed correctly
        grid_update = received[3]['args'][0]['grid']
        self.assertEqual(grid_update[3][0], 'B-P1')
        self.assertEqual(grid_update[4][0], '')

    def test_game_over(self):
        # Initialize game
        self.client.emit('game_init', {})
        received = self.client.get_received()

        # Simulate moves leading to a game over
        self.client.emit('player_move', {'player': 'A', 'character': 'H1', 'move': 'F'})
        self.client.emit('player_move', {'player': 'A', 'character': 'H1', 'move': 'F'})
        self.client.emit('player_move', {'player': 'A', 'character': 'H1', 'move': 'R'})
        self.client.emit('player_move', {'player': 'A', 'character': 'H1', 'move': 'R'})

        received = self.client.get_received()
        self.assertIn('game_over', received[-1]['name'])
        self.assertEqual(received[-1]['args'][0]['winner'], 'A')

if __name__ == '__main__':
    unittest.main()
