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

        # Board dimensions for helper checks (5 files x 8 ranks)
        self.ROWS = 8
        self.COLS = 5

    def _on_board(self, rank, file):
        return 0 <= rank < self.ROWS and 0 <= file < self.COLS

    def _is_enemy_at(self, board, rank, file):
        if not self._on_board(rank, file):
            return False
        target = board[rank][file]
        return target is not None and getattr(target, 'color', None) != self.color

    def _is_ally_at(self, board, rank, file):
        if not self._on_board(rank, file):
            return False
        target = board[rank][file]
        return target is not None and getattr(target, 'color', None) == self.color

    def _is_empty_at(self, board, rank, file):
        if not self._on_board(rank, file):
            return False
        return board[rank][file] is None

    def _sliding_moves(self, board, directions, max_range=7, include_defenses=False):
        """Generic sliding move generator used by Rook/Bishop/Queen-like pieces.

        directions: iterable of (dr, df) tuples.
        Returns a list of (rank, file) tuples.
        """
        moves = []
        rank, file = self.position
        for dr, df in directions:
            for i in range(1, max_range + 1):
                r, f = rank + dr * i, file + df * i
                if not self._on_board(r, f):
                    break
                target = board[r][f]
                if target is None:
                    moves.append((r, f))
                    continue
                # occupied
                if getattr(target, 'color', None) != self.color:
                    moves.append((r, f))
                else:
                    # allied piece encountered
                    if include_defenses:
                        moves.append((r, f))
                break
        return moves

    def get_valid_moves(self, board, include_defenses: bool = False):
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

    def get_valid_moves(self, board, include_defenses: bool = False):
        # Simplified Pawn move logic (only one step forward, no special moves)
        moves = []
        rank, file = self.position
        
        # Determine direction based on color
        direction = -1 if self.color == 'white' else 1
        
        # Compute one square straight ahead and add if empty
        target_rank = rank + direction
        target_pos = (target_rank, file)
        if self._on_board(target_rank, file) and self._is_empty_at(board, target_rank, file):
            moves.append(target_pos)

        # Check diagonally captures
        for offset in (-1, 1):
            target_rank = rank + direction
            target_file = file + offset
            # Pawns 'attack' diagonally; include allied-occupied diagonals when asked
            if self._is_enemy_at(board, target_rank, target_file) or (
                    include_defenses and self._is_ally_at(board, target_rank, target_file)):
                moves.append((target_rank, target_file))

        return moves


class Rook(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = 'R'

    def get_valid_moves(self, board, include_defenses: bool = False):
        # Use generic sliding helper for orthogonal directions
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        return self._sliding_moves(board, directions, include_defenses=include_defenses)


class Knight(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = 'N'

    def get_valid_moves(self, board, include_defenses: bool = False):
        moves = []
        rank, file = self.position
        deltas = [
            (-2, -1), (-2, 1), (2, -1), (2, 1),
            (-1, -2), (-1, 2), (1, -2), (1, 2)
        ]
        for dr, df in deltas:
            r, f = rank + dr, file + df
            if not self._on_board(r, f):
                continue
            target = board[r][f]
            if target is None or getattr(target, 'color', None) != self.color:
                moves.append((r, f))
            elif include_defenses and self._is_ally_at(board, r, f):
                moves.append((r, f))
        return moves
    

class Bishop(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = 'B'

    def get_valid_moves(self, board, include_defenses: bool = False):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        return self._sliding_moves(board, directions, include_defenses=include_defenses)
    

class Monarch(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = 'M'

    def get_valid_moves(self, board, include_defenses: bool = False):
        # Combine rook and bishop directions (like a Queen in standard chess)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]
        return self._sliding_moves(board, directions, include_defenses=include_defenses)