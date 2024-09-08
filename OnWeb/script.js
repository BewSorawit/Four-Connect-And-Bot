const ROWS = 6;
const COLUMNS = 7;
let currentPlayer = 1;
let board = Array(ROWS).fill(null).map(() => Array(COLUMNS).fill(0));
let gameOver = false;

const gameBoard = document.getElementById("gameBoard");
const message = document.getElementById("message");
const resetButton = document.getElementById("resetButton");

function createBoard() {
    gameBoard.innerHTML = '';
    for (let r = 0; r < ROWS; r++) {
        for (let c = 0; c < COLUMNS; c++) {
            const cell = document.createElement('div');
            cell.classList.add('cell', 'empty');
            cell.dataset.row = r;
            cell.dataset.column = c;
            cell.addEventListener('click', handleClick);
            gameBoard.appendChild(cell);
        }
    }
}

function handleClick(event) {
    if (gameOver) return;

    const col = event.target.dataset.column;
    const row = getNextOpenRow(col);

    if (row !== -1) {
        board[row][col] = currentPlayer;
        const cell = document.querySelector(`.cell[data-row="${row}"][data-column="${col}"]`);
        const piece = document.createElement('div');
        piece.classList.add('piece', `player${currentPlayer}`);
        cell.appendChild(piece);
        cell.classList.remove('empty');

        if (checkWin(currentPlayer)) {
            message.textContent = `Player ${currentPlayer} wins!`;
            gameOver = true;
        } else {
            currentPlayer = currentPlayer === 1 ? 2 : 1;
            message.textContent = `Player ${currentPlayer}'s turn`;
        }
    }
}

function getNextOpenRow(col) {
    for (let r = ROWS - 1; r >= 0; r--) {
        if (board[r][col] === 0) {
            return r;
        }
    }
    return -1;
}

function checkWin(player) {
    // Check horizontal, vertical, and diagonal wins
    // Horizontal
    for (let r = 0; r < ROWS; r++) {
        for (let c = 0; c < COLUMNS - 3; c++) {
            if (board[r][c] === player && board[r][c+1] === player && board[r][c+2] === player && board[r][c+3] === player) {
                return true;
            }
        }
    }

    // Vertical
    for (let c = 0; c < COLUMNS; c++) {
        for (let r = 0; r < ROWS - 3; r++) {
            if (board[r][c] === player && board[r+1][c] === player && board[r+2][c] === player && board[r+3][c] === player) {
                return true;
            }
        }
    }

    // Diagonal (positive slope)
    for (let r = 0; r < ROWS - 3; r++) {
        for (let c = 0; c < COLUMNS - 3; c++) {
            if (board[r][c] === player && board[r+1][c+1] === player && board[r+2][c+2] === player && board[r+3][c+3] === player) {
                return true;
            }
        }
    }

    // Diagonal (negative slope)
    for (let r = 3; r < ROWS; r++) {
        for (let c = 0; c < COLUMNS - 3; c++) {
            if (board[r][c] === player && board[r-1][c+1] === player && board[r-2][c+2] === player && board[r-3][c+3] === player) {
                return true;
            }
        }
    }

    return false;
}

resetButton.addEventListener('click', () => {
    board = Array(ROWS).fill(null).map(() => Array(COLUMNS).fill(0));
    currentPlayer = 1;
    gameOver = false;
    message.textContent = `Player ${currentPlayer}'s turn`;
    createBoard();
});

createBoard();
message.textContent = `Player ${currentPlayer}'s turn`;
