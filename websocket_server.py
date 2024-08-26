from game_logic import Game

game = Game()

def init_game():
    game.initialize_game()

def handle_move(data):
    player = data['player']
    character = data['character']
    move = data['move']

    if game.current_turn != player:
        return {'error': 'Not your turn'}

    if not game.move_character(player, character, move):
        return {'error': 'Invalid move'}

    game.check_winner()

    return {
        'grid': game.grid,
        'current_turn': game.current_turn,
        'game_over': game.game_over,
        'winner': game.winner
    }
