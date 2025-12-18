from enum import Enum
from .piece import Bishop, Knight, Monarch, Pawn, Piece, Rook

class GameState(Enum):
    NOT_STARTED = "not_started"
    WHITE_TURN = "white_turn"
    BLACK_TURN = "black_turn"
    GAME_OVER = "game_over"

class Board:
    def __init__(self):
        self.board_array = self.initialize_board()
        self.game_state = GameState.WHITE_TURN
        self.current_player = 'white'

    def initialize_board(self):
        """
        Initializes the 5x8 board with unique Piece objects.
        Board: board[row][column] where row 0 is rank 8 and row 7 is rank 1.
        """
        # Create an 5x8 list of lists, initialized to None (empty square)
        board = [[None for _ in range(5)] for _ in range(8)]

        # --- Black Pieces (Rank 8 = Row 0) ---
        board[0][0] = Rook('black', (0, 0))
        board[0][1] = Bishop('black', (0, 1))
        board[0][2] = Monarch('black', (0, 2))
        board[0][3] = Bishop('black', (0, 3))
        board[0][4] = Rook('black', (0, 4)) 
        # Black Pawns (Rank 7 = Row 1)
        for col in range(5):
            board[1][col] = Pawn('black', (1, col)) 
            
        # --- White Pieces (Rank 2 = Row 6, Rank 1 = Row 7) ---
        # White Pawns (Rank 2 = Row 6)
        for col in range(5):
            board[6][col] = Pawn('white', (6, col)) 
        # White Back Row (Rank 1 = Row 7)
        board[7][0] = Rook('white', (7, 0))
        board[7][1] = Knight('white', (7, 1))
        board[7][2] = Monarch('white', (7, 2))
        board[7][3] = Knight('white', (7, 3))
        board[7][4] = Rook('white', (7, 4)) 
        
        return board


    def get_board(self):
        return self.board_array
    
    def is_game_active(self):
        """Check if the game is still in progress."""
        return self.game_state in (GameState.WHITE_TURN, GameState.BLACK_TURN)

    def move_piece(self, start_coords, end_coords):
        """
        Attempt to move a piece. Validates game state and player turn.
        Returns a dict with 'success', 'message', and optionally 'reason'.
        """
        # Check if game is over
        if not self.is_game_active():
            return {
                'success': False,
                'message': 'Game is over.',
                'reason': 'game_over'
            }

        start_rank, start_file = start_coords
        end_rank, end_file = end_coords

        piece_to_move: Piece = self.board_array[start_rank][start_file]
        if piece_to_move is None:
            return {
                'success': False,
                'message': 'No piece at the selected coordinates.',
                'reason': 'no_piece'
            }

        # Validate that the moving piece belongs to the current player
        if piece_to_move.color != self.current_player:
            return {
                'success': False,
                'message': f'It is {self.current_player}\'s turn. You cannot move {piece_to_move.color} pieces.',
                'reason': 'wrong_player'
            }

        valid_destinations = piece_to_move.get_valid_moves(self.board_array)
        if end_coords not in valid_destinations:
            return {
                'success': False,
                'message': 'Invalid move for this piece.',
                'reason': 'invalid_move'
            }

        # Execute the move
        piece_to_move.position = end_coords
        self.board_array[end_rank][end_file] = piece_to_move 
        self.board_array[start_rank][start_file] = None
        print(f"Moved {piece_to_move.symbol} from {start_coords} to {end_coords}")

        # Switch turn
        self._advance_turn()

        return {
            'success': True,
            'message': f'Moved {piece_to_move.symbol} to ({end_rank}, {end_file})',
            'current_player': self.current_player,
            'game_state': self.game_state.value
        }

    def _advance_turn(self):
        """Switch to the next player's turn."""
        if self.current_player == 'white':
            self.game_state = GameState.BLACK_TURN
            self.current_player = 'black'
        else:
            self.game_state = GameState.WHITE_TURN
            self.current_player = 'white'

    def end_game(self):
        """End the game (e.g., on checkmate or resignation)."""
        self.game_state = GameState.GAME_OVER

    def reset_game(self):
        """Reset the board to starting position and restart the game."""
        self.board_array = self.initialize_board()
        self.game_state = GameState.WHITE_TURN
        self.current_player = 'white'

    def serialize_board(self):
        """
        Converts the board to a JSON-serializable format.
        Returns a 2D list where each piece is represented as a dict with its properties.
        """
        serialized = []
        for row in self.board_array:
            serialized_row = []
            for piece in row:
                if piece is None:
                    serialized_row.append(None)
                else:
                    serialized_row.append({
                        'symbol': piece.symbol,
                        'color': piece.color,
                        'position': piece.position
                    })
            serialized.append(serialized_row)
        return serialized
    