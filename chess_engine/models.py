from enum import Enum

class GameState(Enum):
    WHITE_TURN = "white_turn"
    BLACK_TURN = "black_turn"
    GAME_OVER = "game_over"

class Sounds(Enum):
    MOVE = "move"
    CAPTURE = "capture"
    GAME_OVER = "gameover"
