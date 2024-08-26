class Game:
    def __init__(self):
        self.grid = [["" for _ in range(5)] for _ in range(5)]
        self.current_turn = 'A'
        self.game_over = False
        self.winner = None

    def initialize_game(self):
        self.grid[0] = ['A-P1', 'A-H1', 'A-P2', 'A-H2', 'A-P3']
        self.grid[4] = ['B-P1', 'B-H1', 'B-P2', 'B-H2', 'B-P3']

    def get_game_state(self):
        return {
            'grid': self.grid,
            'current_turn': self.current_turn,
            'game_over': self.game_over,
            'winner': self.winner
        }

    def move_character(self, player, character, move):
        if self.game_over:
            return False, "Game is over."

        if player != self.current_turn:
            return False, "Not your turn."

        char_pos = self.find_character_position(character)
        if not char_pos:
            return False, "Character not found."

        move_valid, new_pos = self.validate_move(char_pos, move, player)
        if not move_valid:
            return False, "Invalid move."

        # Capture any opponent's characters in the path
        self.capture_characters(char_pos, new_pos, player)

        # Update the grid
        self.grid[char_pos[0]][char_pos[1]] = ""
        self.grid[new_pos[0]][new_pos[1]] = f"{player}-{character}"
        
        self.check_game_over()
        self.current_turn = 'B' if player == 'A' else 'A'
        return True, ""

    def find_character_position(self, character):
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if cell.endswith(character):
                    return (i, j)
        return None

    def validate_move(self, position, move, player):
        x, y = position
        char = self.grid[x][y]
        char_type = char.split('-')[1]

        if char_type == 'P':
            return self.validate_pawn_move(position, move)
        elif char_type == 'H1':
            return self.validate_hero1_move(position, move)
        elif char_type == 'H2':
            return self.validate_hero2_move(position, move)
        else:
            return False, "Unknown character type."

    def validate_pawn_move(self, position, move):
        x, y = position
        if move == 'L':
            return (x, y - 1) if y - 1 >= 0 else False, "Move out of bounds"
        elif move == 'R':
            return (x, y + 1) if y + 1 < 5 else False, "Move out of bounds"
        elif move == 'F':
            return (x - 1, y) if x - 1 >= 0 else False, "Move out of bounds"
        elif move == 'B':
            return (x + 1, y) if x + 1 < 5 else False, "Move out of bounds"
        else:
            return False, "Invalid move"

    def validate_hero1_move(self, position, move):
        x, y = position
        if move == 'L':
            return (x, y - 2) if y - 2 >= 0 else False, "Move out of bounds"
        elif move == 'R':
            return (x, y + 2) if y + 2 < 5 else False, "Move out of bounds"
        elif move == 'F':
            return (x - 2, y) if x - 2 >= 0 else False, "Move out of bounds"
        elif move == 'B':
            return (x + 2, y) if x + 2 < 5 else False, "Move out of bounds"
        else:
            return False, "Invalid move"

    def validate_hero2_move(self, position, move):
        x, y = position
        if move == 'FL':
            return (x - 2, y - 2) if x - 2 >= 0 and y - 2 >= 0 else False, "Move out of bounds"
        elif move == 'FR':
            return (x - 2, y + 2) if x - 2 >= 0 and y + 2 < 5 else False, "Move out of bounds"
        elif move == 'BL':
            return (x + 2, y - 2) if x + 2 < 5 and y - 2 >= 0 else False, "Move out of bounds"
        elif move == 'BR':
            return (x + 2, y + 2) if x + 2 < 5 and y + 2 < 5 else False, "Move out of bounds"
        else:
            return False, "Invalid move"

    def capture_characters(self, start_pos, end_pos, player):
        x1, y1 = start_pos
        x2, y2 = end_pos

        if self.grid[x2][y2] and self.grid[x2][y2].startswith('B' if player == 'A' else 'A'):
            self.grid[x2][y2] = ""

    def check_game_over(self):
        player_a_has_pieces = any(cell.startswith('A-') for row in self.grid for cell in row)
        player_b_has_pieces = any(cell.startswith('B-') for row in self.grid for cell in row)

        if not player_a_has_pieces:
            self.game_over = True
            self.winner = 'B'
        elif not player_b_has_pieces:
            self.game_over = True
            self.winner = 'A'
