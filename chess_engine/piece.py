class Piece:
    """
    Base class for all chess pieces. Defines properties shared by all pieces.
    """
    def __init__(self, color, position):
        # Mandatory properties for every piece
        self.color = color         # 'white' or 'black'
        self.position = position   # (row, file) tuple, e.g., (6, 0) for A2

        # Simplification: Use a single letter for rendering in the template
        # e.g., 'P' for Pawn, 'R' for Rook, etc.
        self.symbol = '?'

    def get_valid_moves(self, board):
        """
        Abstract method. Subclasses must override this to return a list of 
        (row, file) tuples representing legal destinations.
        The 'board' argument is needed to check for blocks and captures.
        """
        return []

class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = 'P'

    def get_valid_moves(self, board):
        # Simplified Pawn move logic (only one step forward, no special moves)
        moves = []
        rank, file = self.position
        
        # Determine direction based on color
        direction = -1 if self.color == 'white' else 1
        
        # Compute one square straight ahead
        target_rank = rank + direction
        target_pos = (target_rank, file)
        
        # Check if the target position is on the board
        if 0 <= target_rank < 8:
            # Check if the target square is empty (Pawn can't capture forward)
            # NOTE: For now, we assume the board uses a simple array structure.
            if board[target_rank][file] is None:
                 moves.append(target_pos)

        # Basic capture logic (Needs board access to check if piece is opponent)
        # This is where the logic would get complex, but we will leave it simple for now.
        
        return moves


class Rook(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = 'R'

    def get_valid_moves(self, board):
        # TODO: Rook logic (horizontal and vertical sliding)
        return []

class Knight(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = 'N'

    def get_valid_moves(self, board):
        # TODO: Knight logic (L-shape moves)
        return []
    
class Bishop(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = 'B'

    def get_valid_moves(self, board):
        # TODO: Bishop logic (Diagonal sliding)
        return []
    
class Monarch(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = 'M'

    def get_valid_moves(self, board):
        # TODO: Monarch logic (call valid moves for a Rook and a Bishop)
        return []