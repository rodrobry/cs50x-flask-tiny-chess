from .constants import FILES, PIECE_VALUES
from .piece import Bishop, Knight, Monarch, Pawn, Piece, Rook
from .models import GameMode, GameState, Sounds, Move
from typing import List

class Board:
    def __init__(self):
        self.board_array: List[List[Piece]] = self.initialize_board()
        self.game_mode = GameMode.BOT_MEDIUM
        self.game_state = GameState.WHITE_TURN
        self.move_history = []
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
        target_piece = self.board_array[end_rank][end_file]
        piece_to_move.position = end_coords
        if piece_to_move.symbol == 'P' and (end_rank == 0 or end_rank == 7):
            # Pawn promotion
            if piece_to_move.color == 'white':
                promoted_piece = Knight('white', (end_rank, end_file))
            else:
                promoted_piece = Bishop('black', (end_rank, end_file))
            self.board_array[end_rank][end_file] = promoted_piece
            print("Pawn promoted!")
        else:
            self.board_array[end_rank][end_file] = piece_to_move
        self.board_array[start_rank][start_file] = None
        # Switch turn
        self._advance_turn()
        # Capture logic
        if target_piece is not None:
            log_str = f"{piece_to_move.symbol}x{8 - end_rank}{FILES[end_file]}"
            if target_piece.symbol == 'M':
                # Monarch captured - game over
                print(f"Game over! {piece_to_move.color.capitalize()} wins by capturing the Monarch.")
                self.end_game()
                sound = Sounds.GAME_OVER
            else:
                print(f"Captured {target_piece.symbol} at {end_coords}")
                sound = Sounds.CAPTURE
        # Move logic
        else:
            log_str = f"{piece_to_move.symbol}{8 - end_rank}{FILES[end_file]}"
            print(f"Moved {piece_to_move.symbol} from {start_coords} to {end_coords}")
            sound = Sounds.MOVE

        # Log move
        self.move_history.append(log_str)

        return {
                'success': True,
                'message': f'Moved {piece_to_move.symbol} to ({end_rank}, {end_file})',
                'current_player': self.current_player,
                'game_state': self.game_state,
                'sound': sound
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
        self.move_history = []


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


    def get_legal_moves(self, color: str) -> List[Move]:
        """
        Get all legal moves for a side.
        Returns a list of tuple pairs -> (start_rank, start_file), (end_rank, end_file).
        """
        moves: List[Move] = []
        for rank in self.board_array:
            for piece in rank:
                if piece is None or piece.color != color:
                    continue
                for move in piece.get_valid_moves(self.board_array):
                    score = 0
                    target_piece: Piece = self.board_array[move[0]][move[1]]
                    if target_piece is not None:
                        score = PIECE_VALUES.get(target_piece.symbol, 0)
                    moves.append(Move(piece.position, move, piece.symbol, score))
        return moves


    def get_bot_move(self) -> Move:
        """
        Get a legal move.
        Returns a tuple pair -> (start_rank, start_file), (end_rank, end_file).
        """
        import random
        moves = self.get_legal_moves('black')
        if not moves:
            return None
        if self.game_mode == GameMode.BOT_EASY:
            return random.choice(moves)
        elif self.game_mode == GameMode.BOT_MEDIUM:
            white_legal_moves = self.get_legal_moves('white')
            white_targets = {m.end for m in white_legal_moves}

            # Adjust scores
            for move in moves:
                # If the destination is defended, subtract the value of the capturing piece
                if move.end in white_targets:
                    print("base move:", move)
                    move.score -= PIECE_VALUES.get(move.piece, 0)
                    print("adjusted move:", move)

            # Get the best score and all moves with that score
            best_score = max(move.score for move in moves)
            best_moves = [move for move in moves if move.score == best_score]

            return random.choice(best_moves)