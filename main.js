const socket = io();

socket.on('game_state_update', function(gameState) {
    console.log('Game state updated:', gameState);
    updateGameBoard(gameState);
});

socket.on('game_over', function(data) {
    alert('Game Over! Winner: ' + data.winner);
});

function updateGameBoard(gameState) {
    const board = document.getElementById('game-board');
    board.innerHTML = ''; // Clear existing board
    gameState.grid.forEach(row => {
        row.forEach(cell => {
            const div = document.createElement('div');
            div.className = 'cell';
            div.textContent = cell;
            board.appendChild(div);
        });
    });
}

// Example of emitting a move (this would be triggered by user actions)
function makeMove(player, character, move) {
    socket.emit('player_move', { player, character, move });
}
