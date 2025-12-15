let selectedSquare = null; // Stores the <td> element of the first click

function handleSquareClick(squareElement) {
    const row = squareElement.dataset.row;
    const col = squareElement.dataset.col;

    // --- First Click (Selecting the piece to move) ---
    if (selectedSquare === null) {
        // Store the starting square
        selectedSquare = squareElement;
        
        // Add a visual highlight (you'll need to define this CSS class)
        squareElement.classList.add('selected');
        
    } 
    // --- Second Click (Selecting the destination) ---
    else {
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
}