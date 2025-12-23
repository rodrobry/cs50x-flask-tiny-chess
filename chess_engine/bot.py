from .board import Board
from .constants import PIECE_VALUES
from .models import GameMode, Move
import random

side = 'black'

def get_bot_move(board: Board) -> Move:
    """
    Get a legal move.
    Returns a tuple pair -> (start_rank, start_file), (end_rank, end_file).
    """
    moves = board.get_legal_moves(side)
    if not moves:
        return None
    
    # Filter moves based on difficulty
    if board.game_mode == GameMode.BOT_MEDIUM:
        moves = get_best_greedy_moves(board, moves)

    return random.choice(moves)

def get_best_greedy_moves(board: Board, moves: list[Move]) -> list[Move]:
    """
    Get all legal moves with the highest score for the given side.
    Returns a list of Move objects.
    """
    enemy = 'white' if side == 'black' else 'black'
    enemy_legal_moves = board.get_legal_moves(enemy, include_defenses=True)
    enemy_targets = {m.end for m in enemy_legal_moves}

    # Adjust scores
    for move in moves:
        # If the destination is defended, subtract the value of the capturing piece
        if move.end in enemy_targets:
            print("base move:", move)
            move.score -= PIECE_VALUES.get(move.piece, 0)
            print("adjusted move:", move)

    # Get the best score and all moves with that score
    best_score = max(move.score for move in moves)
    best_moves = [move for move in moves if move.score == best_score]

    return best_moves