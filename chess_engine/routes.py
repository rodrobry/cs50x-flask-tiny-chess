from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from .board import Board
from .piece import Piece

bp = Blueprint('main', __name__)

# NOTE: The Board instance should be managed by your app
# For simplicity, we'll initialize it here for now.
game_board = Board()


@bp.route('/')
def index():
    """Renders the main chess board display."""
    
    board_data = game_board.get_board()
    files = ['a', 'b', 'c', 'd', 'e']

    return render_template("index.html", board=board_data, files=files)


@bp.route('/select', methods=['POST'])
def select():
    """Compute valid moves for a piece move."""
    # Get move data from the form
    start_r = int(request.form.get('start_row'))
    start_c = int(request.form.get('start_col'))
    
    # Calculate legal moves
    piece: Piece = game_board.get_board()[start_r][start_c]
    if piece is None:
        return jsonify({
            'status': 'error',
            'message': 'No piece at the selected coordinates.'
        })
    valid_moves = piece.get_valid_moves(game_board.get_board())
    
    # Return the list of (r, c) tuples as JSON
    return jsonify({
        'status': 'success',
        'moves': valid_moves # e.g., [[5, 0], [4, 0]]
    })

@bp.route('/move', methods=['POST'])
def move():
    """Handles POST requests for a piece move."""
    # Logic to get move data from the form
    start_r = int(request.form.get('start_row'))
    start_c = int(request.form.get('start_col'))
    end_r = int(request.form.get('end_row'))
    end_c = int(request.form.get('end_col'))

    start_coords = (start_r, start_c)
    end_coords = (end_r, end_c)
    game_board.move_piece(start_coords, end_coords)
    
    return redirect(url_for('main.index'))