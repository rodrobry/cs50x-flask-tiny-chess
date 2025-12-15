class Board:
    # 1. Use the special constructor name __init__
    # 2. Add 'self' as the first parameter
    def __init__(self): 
        # Store the board array as an instance variable
        self.board_array = [
            ['bR', 'bB', 'bM', 'bB', 'bR'], # Rank 8
            ['bP', 'bP', 'bP', 'bP', 'bP'], # Rank 7
            ['  ', '  ', '  ', '  ', '  '], # Rank 6
            ['  ', '  ', '  ', '  ', '  '], # Rank 5
            ['  ', '  ', '  ', '  ', '  '], # Rank 4
            ['  ', '  ', '  ', '  ', '  '], # Rank 3
            ['wP', 'wP', 'wP', 'wP', 'wP'], # Rank 2
            ['wR', 'wN', 'wM', 'wN', 'wR']  # Rank 1
        ]

    # You might want a separate method to return the array later
    def get_board(self):
        return self.board_array