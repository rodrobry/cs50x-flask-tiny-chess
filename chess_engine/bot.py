from .board import Board
from .constants import PIECE_VALUES
from .models import GameMode, Move
from .piece import Piece
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
    # TODO: Either find a way to add sliding moves that stop being blocked,
    # or implement ability to simulate/undo moves to validate their value.
    # Also need to account for pawn diagonal captures that are only possible
    # after other pieces move.

    # Calculate scores
    for move in moves:
        move.score = 0
        # If the destination has an enemy piece, add its value to the score
        target_piece: Piece = board.board_array[move.end[0]][move.end[1]]
        if target_piece is not None:
            move.score = PIECE_VALUES.get(target_piece.symbol, 0)
        # If the destination is defended, subtract the value of the sacrificed piece
        if move.end in enemy_targets:
            move.score -= PIECE_VALUES.get(move.piece, 0)
        # If the move removes a piece from an attacked square, make it more valuable
        start_attacked = any(m.end == move.start for m in enemy_legal_moves)
        end_attacked = any(m.end == move.end for m in enemy_legal_moves)
        if start_attacked and not end_attacked:
            move.score += PIECE_VALUES.get(move.piece, 0)
        print(f"Move: {move.start} -> {move.end}, Score: {move.score}")

    # Get the best score and all moves with that score
    best_score = max(move.score for move in moves)
    best_moves = [move for move in moves if move.score == best_score]

    return best_moves
