from .piece import Bishop, Knight, Monarch, Pawn, Piece, Rook

class Board:
    def __init__(self):
        self.board_array = self.initialize_board()

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
    
    def move_piece(self, start_coords, end_coords):
        start_rank, start_file = start_coords
        end_rank, end_file = end_coords

        piece_to_move: Piece = self.board_array[start_rank][start_file]
        if piece_to_move is None:
            print("Error: Tried to move invalid piece")
            return False

        valid_destinations = piece_to_move.get_valid_moves(self.board_array)
        if end_coords not in valid_destinations:
            print("Invalid move for piece")
            return False

        piece_to_move.position = end_coords
        self.board_array[end_rank][end_file] = piece_to_move 
        self.board_array[start_rank][start_file] = None
        print(f"Moved {piece_to_move.symbol} from {start_coords} to {end_coords}")

        return True

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
    