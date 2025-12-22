from enum import StrEnum
from dataclasses import dataclass

class GameState(StrEnum):
    WHITE_TURN = "white_turn"
    BLACK_TURN = "black_turn"
    GAME_OVER = "game_over"

class Sounds(StrEnum):
    MOVE = "move"
    CAPTURE = "capture"
    GAME_OVER = "gameover"

class GameMode(StrEnum):
    LOCAL = "local"
    BOT = "bot"

@dataclass
class Move:
    start: tuple
    end: tuple