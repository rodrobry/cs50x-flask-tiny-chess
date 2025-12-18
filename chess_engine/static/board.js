let selectedSquare = null; // Stores the <td> element of the first click

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

function movePiece(row, col) {
    // Get the start coordinates from the first click
        const startRow = selectedSquare.dataset.row;
        const startCol = selectedSquare.dataset.col;

        // Get the end coordinates from the second click
        const endRow = row;
        const endCol = col;

        // Populate the hidden form fields
        document.getElementById('start_row').value = startRow;
        document.getElementById('start_col').value = startCol;
        document.getElementById('end_row').value = endRow;
        document.getElementById('end_col').value = endCol;

        // Submit the form to Flask route
        document.getElementById('move-form').submit();

        // Reset the state
        selectedSquare.classList.remove('selected');
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