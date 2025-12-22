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
    BOT_EASY = "bot_easy"
    BOT_MEDIUM = "bot_medium"

@dataclass
class Move:
    start: tuple
    end: tuple
    score: int = 0