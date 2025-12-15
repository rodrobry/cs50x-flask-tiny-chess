# app.py

from flask import Flask, render_template
from board import get_initial_board

app = Flask(__name__)

@app.route("/")
def index():
    """Renders the main chess game page."""
    
    board_state = get_initial_board()
    files = ['a', 'b', 'c', 'd', 'e']

    return render_template("index.html", board=board_state, files=files)