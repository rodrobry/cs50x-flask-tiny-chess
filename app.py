# app.py

from flask import Flask, render_template

app = Flask(__name__)

def get_initial_board():
    return [
        ['bR', 'bB', 'bM', 'bB', 'bR'], # Rank 8
        ['bP', 'bP', 'bP', 'bP', 'bP'], # Rank 7
        ['  ', '  ', '  ', '  ', '  '], # Rank 6
        ['  ', '  ', '  ', '  ', '  '], # Rank 5
        ['  ', '  ', '  ', '  ', '  '], # Rank 4
        ['  ', '  ', '  ', '  ', '  '], # Rank 3
        ['wP', 'wP', 'wP', 'wP', 'wP'], # Rank 2
        ['wR', 'wN', 'wM', 'wN', 'wR']  # Rank 1
    ]

@app.route("/")
def index():
    """Renders the main chess game page."""
    
    board_state = get_initial_board()
    files = ['a', 'b', 'c', 'd', 'e']

    return render_template("index.html", board=board_state, files=files)