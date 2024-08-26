from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

from game_logic import Game

game = Game()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('game_init')
def handle_game_init():
    game.initialize_game()
    emit('game_state_update', game.get_game_state(), broadcast=True)

@socketio.on('player_move')
def handle_player_move(data):
    player = data.get('player')
    character = data.get('character')
    move = data.get('move')
    
    valid, message = game.move_character(player, character, move)
    if valid:
        emit('game_state_update', game.get_game_state(), broadcast=True)
        if game.game_over:
            emit('game_over', {'winner': game.winner})
    else:
        emit('invalid_move', {'message': message})

if __name__ == '__main__':
    socketio.run(app, debug=True)
