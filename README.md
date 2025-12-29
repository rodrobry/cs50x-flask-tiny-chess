# TINY CHESS

#### Video Demo:  [youtube](https://youtu.be/0ftHxGtMjnY)

## Project Overview:

Tiny Chess is a web-based chess-like game implemented with Flask on the backend and JavaScript on the frontend. The game built on the foundations of Chess, but it features a 5×8 board with some simplified piece mechanics designed to keep games brief while maintaining some strategic depth.
Players can play locally - against another person on the same device or challenge themselves - or test their skills against a computer opponent at selectable difficulty levels. This README documents the project structure, explains what each file does, and discusses the design choices made throughout development.

## Game Overview

The game removes traditional chess complexity through a smaller board (5×8 instead of 8x8) and simplified piece set while still requiring meaningful strategic decisions. The win condition is straightforward: capture your opponent's Monarch (the central piece) or advance a Pawn to the opponent's back rank - "Ascension".

## Core Features

The game implements several key features that enhance playability and user experience:

- **Interactive Visual Board**: A click-to-select interface for piece movement with real-time highlighting of valid moves and selected pieces.
- **Server-Side Game Logic**: All move validation, move generation, and game state management occur on the server, ensuring consistency and preventing exploitation.
- **Multiple Game Modes**: Players can choose between local two-player mode, play against themselves, or face an AI bot at easy or medium difficulty levels. Game modes can be switched mid-game to adjust difficulty or force specific bot moves.
- **Move History Tracking**: Every move is logged and displayed, allowing players to review the game progression.
- **Sound Effects and Feedback**: Audio cues for piece movement, captures, and game-over.
- **Smart Move Validation**: Legal move calculation is performed per-piece using object-oriented design, with collision detection and capture rules built into each piece class.

## File Structure and Responsibilities

```
cs50x-flask-tiny-chess/
├── run.py                  # Application entry point
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
│
└── chess_engine/
    ├── __init__.py         # Flask app factory and configuration
    ├── routes.py           # Game endpoints and AJAX request handling
    ├── board.py            # Board state and game rule enforcement
    ├── piece.py            # Piece classes with movement logic
    ├── bot.py              # AI bot evaluation and move selection
    ├── constants.py        # Game constants and configuration
    ├── models.py           # Data models for type safety
    │
    ├── templates/
    │   └── index.html      # Game interface markup
    │
    └── static/
        ├── styles.css      # Board and UI styling
        ├── board.js        # Client-side interaction logic
        └── sounds/         # Audio files for game events
```

### Backend Files

**run.py** — The application entry point. This file imports the Flask app factory from `chess_engine/__init__.py` and starts the development server on localhost:5000.

**chess_engine/__init__.py** — Implements the Flask application factory pattern. Handles app creation, configuration loading, and blueprint registration to keep configuration centralized and testable.

**chess_engine/routes.py** — Defines the Flask blueprint with routes for the main page and AJAX endpoints:
  - `GET /` renders the main game interface
  - `POST /select` receives a piece's coordinates and returns all legal moves for that piece
  - `POST /move` executes a move (validates it server-side, updates game state, and triggers the bot response move if applicable)
  - `POST /reset` resets the board to the starting position
  - `POST /update_mode` changes the current game mode (Local, Bot Easy, or Bot Medium)
  
  These routes act as the bridge between the interactive frontend and the backend state.

**chess_engine/board.py** — The heart of game logic. The `Board` class maintains the 2D board array, current player, move history, and game state. It enforces high-level rules (turn order, game-over conditions, move execution) and coordinates with piece classes to validate moves. All game state lives here, ensuring a single source of truth.

**chess_engine/piece.py** — Defines piece classes (`Pawn`, `Rook`, `Knight`, `Bishop`, `Monarch`) each inheriting from a base `Piece` class. Every piece class implements `get_valid_moves()`, encapsulating that piece's movement rules, collision detection, and capture behavior. This object-oriented design makes it easy to add new pieces or modify existing ones without touching the core board logic.

**chess_engine/bot.py** — Implements AI opponent logic. The bot evaluates candidate moves using a simple heuristic based on piece values (material gain/loss) and makes decisions accordingly. At easy difficulty, it selects moves randomly; at medium difficulty, it picks higher-scoring moves, creating a noticeable skill difference.

**chess_engine/constants.py** — A small utility file defining game constants such as board files, piece value mappings used for move evaluation, and other configuration constants.

**chess_engine/models.py** — Holds model classes (`GameMode`, `GameState`, `Move`) to isolate them, creating a more mantainable code and helping avoid circular dependencies.

### Frontend Files

**chess_engine/templates/index.html** — The main HTML template containing the board grid, move history display, game mode selector, and a reset game button. It also includes a footer with an overview of the rules.

**chess_engine/static/board.js** — Client-side JavaScript handling user interaction. Listens for piece clicks, requests legal moves from the server, highlights valid moves and selected pieces, sends move requests, and updates the displayed board.

**chess_engine/static/styles.css** — CSS styling for the board squares, pieces, highlights, and UI controls.

**chess_engine/static/sounds/** — Audio files triggered on moves, captures, and game-over events, enhancing user feedback.

## Design Choices and Rationale

**Server-Side Authoritative State** — All game logic and validation happens on the server in the `Board` class. This prevents the frontend from submitting invalid moves, ensures game state consistency.

**Client as Thin Layer** — The frontend only displays state and sends user input; the server makes all decisions. This separation keeps the client simple and prevents inconsistencies.

**Object-Oriented Piece Architecture** — Using a base `Piece` class with subclasses keeps movement rules encapsulated and isolated. Each piece is responsible for its own valid moves, making the code modular and extensible. Adding a new piece type requires only a new class; the board logic remains unchanged.

**Compact 5×8 Board with Custom Rules** — Rather than a full chess board, the 5×8 board reduces code complexity.
The `Monarch` piece unifies the king/queen role into a single piece type. It is the strongest piece, but also one you need to keep protected.
Capturing the opponent's Monarch was initially intended as the only win condition, but after testing it became evident that capturing a piece that moves like a queen in the end game is very difficult, so a sedcond win condition was added.
Advancing a Pawn to the back rank - "Ascension" - also wins you the game, instead of the tradition pawn promotion. This accelerates games and adds strategic depth since there are more ways to win a game.

## Running the Project

1. Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python run.py
   ```

4. Open your browser to `http://localhost:5000` and start playing.

## Future Enhancements

Possible extensions include persistent game saves to a database, online multiplayer support and a richer AI using minimax.
