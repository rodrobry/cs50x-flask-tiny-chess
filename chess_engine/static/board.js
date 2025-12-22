let selectedSquare = null; // Stores the <td> element of the first click

const Sounds = {
    MOVE: 'move',
    CAPTURE: 'capture',
    GAMEOVER: 'gameover'
};

function handleSquareClick(squareElement) {
    const row = squareElement.dataset.row;
    const col = squareElement.dataset.col;

    // --- First Click (Selecting the piece to move) ---
    if (selectedSquare === null) {
        selectPiece(squareElement);
    } 
    // --- Second Click (Selecting the destination) ---
    else {
        movePiece(row, col);
    }
}

async function selectPiece(squareElement) {
    clearHighlights();
    const startRow = squareElement.dataset.row;
    const startCol = squareElement.dataset.col;

    // Store the starting square
    selectedSquare = squareElement;
    // Add a visual highlight
    squareElement.classList.add('selected');

    // AJAX Call to Flask to get valid moves
    const formData = new FormData();
    formData.append('start_row', startRow);
    formData.append('start_col', startCol);

    try {
        // Get valid moves for selected piece
        const response = await fetch('/select', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        validMoves = data.moves;

        // Highlight the valid destination squares
        validMoves.forEach(([r, c]) => {
            // Find the <td> element using the data attributes
            const targetSquare = document.querySelector(`td[data-row="${r}"][data-col="${c}"]`);
            if (targetSquare) {
                targetSquare.classList.add('valid-move');
            }
        });

    } catch (error) {
        console.error("Error fetching valid moves:", error);
    }
}

async function movePiece(row, col) {
    // Get the start coordinates from the first click
    const startRow = selectedSquare.dataset.row;
    const startCol = selectedSquare.dataset.col;

    // Get the end coordinates from the second click
    const endRow = row;
    const endCol = col;

    // AJAX Call to Flask to make the move 
    const formData = new FormData();
    formData.append('start_row', startRow);
    formData.append('start_col', startCol);
    formData.append('end_row', endRow);
    formData.append('end_col', endCol);

    const response = await fetch('/move', {
        method: 'POST',
        body: formData
    });
    const result = await response.json();

    if (result.status === 'success') {
        // Find the <td> element for the destination
        const targetSquare = document.querySelector(
            `td[data-row="${endRow}"][data-col="${endCol}"]`
        );
        piece = result.new_board[endRow][endCol];

        // Execute move
        renderBoard(result.new_board);
        playMoveSound(result.is_capture);
        updateMoveLog(result.move_history);
        // Update game status
        if (result.game_state === "game_over") {
            winner = piece.color === 'white' ? 'White' : 'Black';
            document.querySelector('#status').innerText = winner + " wins!";
        } else {
            playerTurn = result.game_state === "white_turn" ? "White" : "Black";
            document.querySelector('#status').innerText = playerTurn + "'s Turn";
        }

        console.log("UI Updated successfully!");
    } else {
        console.log("Move failed: " + result.message);
    }
    
    // Reset for the next move
    currentValidMoves = [];
    clearHighlights();
    selectedSquare = null;
}

function clearHighlights() {
    // Remove the 'selected' class from the old piece
    if (selectedSquare) {
        selectedSquare.classList.remove('selected');
    }
    // Remove the 'valid-move' class from all previously highlighted squares
    document.querySelectorAll('.valid-move').forEach(el => {
        el.classList.remove('valid-move');
    });
}

async function resetGame() {
    try {
        const response = await fetch('/reset', {
            method: 'POST'
        });
        const result = await response.json();
        if (result.status === 'success') {
            // Reload the page to reset the board
            location.reload();
        }
    } catch (error) {
        console.error("Error resetting the game:", error);
    }
}

function updateMoveLog(history) {
    const list = document.getElementById('move-list');
    list.innerHTML = ''; // Clear the old list

    history.forEach(move => {
        const entry = document.createElement('li');
        entry.innerText = move;
        list.appendChild(entry);
    });
}

function playMoveSound(soundName) {
    const soundKey = Object.values(Sounds).find(val => val === soundName);
    const sound = document.getElementById(`sound-${soundKey}`);

    sound.currentTime = 0; // Reset sound to start (in case of rapid moves)
    sound.play();
}

function renderBoard(boardArray) {
    const squareElements = document.querySelectorAll('#chess-board td');

    squareElements.forEach((square, index) => {
        const r = Math.floor(index / 5);
        const c = index % 5;
        const piece = boardArray[r][c];
        square.innerHTML = '';
        if (piece) {
            square.innerText = piece.symbol;
            square.classList.remove('white', 'black');
            square.classList.add(piece.color);
        }
    });
}

function updateGameMode() {
    const modeSelect = document.getElementById('game-mode');
    const selectedMode = modeSelect.value;
    fetch('/update_mode', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ mode: selectedMode })
    });
}