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
    # Get data from the form
    try:
        start_r = int(request.form.get('start_row'))
        start_c = int(request.form.get('start_col'))
    except (TypeError, ValueError):
        return jsonify({
                'status': 'error',
                'message': 'Invalid coordinate format'
            }), 400

    # Check game is active
    if not game_board.is_game_active():
        return jsonify({
            'status': 'error',
            'message': 'Game is over.'
        }), 400

    # Calculate legal moves
    piece: Piece = game_board.get_board()[start_r][start_c]
    if piece is None:
        return jsonify({
            'status': 'error',
            'message': 'No piece at the selected coordinates.'
        })

    # Check piece belongs to current player
    if piece.color != game_board.current_player:
        return jsonify({
            'status': 'error',
            'message': f'It is {game_board.current_player}\'s turn.'
        }), 400
    
    valid_moves = piece.get_valid_moves(game_board.get_board())

    # Return the list of (r, c) tuples as JSON
    return jsonify({
        'status': 'success',
        'moves': valid_moves # e.g., [[5, 0], [4, 0]]
    })

@bp.route('/move', methods=['POST'])
def move():
    """Handles POST requests for a piece move."""
    # Get data from the form
    try:
        start_r = int(request.form.get('start_row'))
        start_c = int(request.form.get('start_col'))
        end_r = int(request.form.get('end_row'))
        end_c = int(request.form.get('end_col'))
    except (TypeError, ValueError):
        return jsonify({
                'status': 'error',
                'message': 'Invalid coordinate format'
            }), 400

    start_coords = (start_r, start_c)
    end_coords = (end_r, end_c)

    # Execute the move on the board
    result = game_board.move_piece(start_coords, end_coords)

    if result['success']:
        # Return a success message
        return jsonify({
            'status': 'success',
            'message': result['message'],
            'current_player': result['current_player'],
            'game_state': result['game_state'],
            'new_board': game_board.serialize_board()
        })
    else:
        # Return an error message so the JS can alert the user
        return jsonify({
            'status': 'error', 
            'message': result['message'],
            'reason': result.get('reason', 'unknown')
        }), 400

@bp.route('/reset', methods=['POST'])
def reset_game():
    """Reset the board to starting position."""
    game_board.reset_game()

    return jsonify({
        'status': 'success',
        'message': 'Game reset. White to move.',
        'current_player': game_board.current_player,
        'game_state': game_board.game_state.value,
        'new_board': game_board.serialize_board()
    })