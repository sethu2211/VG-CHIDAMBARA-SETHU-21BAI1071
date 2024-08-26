const socket = io('http://localhost:5000');

socket.on('connect', () => {
    console.log('Connected to server');
    socket.emit('game_init', {});
});

socket.on('game_state_update', (data) => {
    if (data.error) {
        alert(data.error);
    } else {
        updateGameState(data);
    }
});

// Example: send a move
function sendMove(player, character, move) {
    socket.emit('player_move', { player, character, move });
}
