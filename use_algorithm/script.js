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
    if (gameOver || currentPlayer !== 1) return;

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
        } else if (checkDraw()) {
            message.textContent = "It's a draw!";
            gameOver = true;
        } else {
            currentPlayer = 2;
            message.textContent = `Player 2 (AI)'s turn`;
            setTimeout(aiMove, 500);
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
    // Horizontal, Vertical, and Diagonal checks
    for (let r = 0; r < ROWS; r++) {
        for (let c = 0; c < COLUMNS - 3; c++) {
            if (board[r][c] === player && board[r][c + 1] === player && board[r][c + 2] === player && board[r][c + 3] === player) {
                return true;
            }
        }
    }

    for (let c = 0; c < COLUMNS; c++) {
        for (let r = 0; r < ROWS - 3; r++) {
            if (board[r][c] === player && board[r + 1][c] === player && board[r + 2][c] === player && board[r + 3][c] === player) {
                return true;
            }
        }
    }

    for (let r = 0; r < ROWS - 3; r++) {
        for (let c = 0; c < COLUMNS - 3; c++) {
            if (board[r][c] === player && board[r + 1][c + 1] === player && board[r + 2][c + 2] === player && board[r + 3][c + 3] === player) {
                return true;
            }
        }
    }

    for (let r = 3; r < ROWS; r++) {
        for (let c = 0; c < COLUMNS - 3; c++) {
            if (board[r][c] === player && board[r - 1][c + 1] === player && board[r - 2][c + 2] === player && board[r - 3][c + 3] === player) {
                return true;
            }
        }
    }

    return false;
}

function checkDraw() {
    return board.every(row => row.every(cell => cell !== 0));
}

function evaluateBoard(board, player) {
    let score = 0;

    for (let r = 0; r < ROWS; r++) {
        for (let c = 0; c < COLUMNS - 3; c++) {
            let window = [board[r][c], board[r][c + 1], board[r][c + 2], board[r][c + 3]];
            score += evaluateWindow(window, player);
        }
    }

    for (let c = 0; c < COLUMNS; c++) {
        for (let r = 0; r < ROWS - 3; r++) {
            let window = [board[r][c], board[r + 1][c], board[r + 2][c], board[r + 3][c]];
            score += evaluateWindow(window, player);
        }
    }

    for (let r = 0; r < ROWS - 3; r++) {
        for (let c = 0; c < COLUMNS - 3; c++) {
            let window = [board[r][c], board[r + 1][c + 1], board[r + 2][c + 2], board[r + 3][c + 3]];
            score += evaluateWindow(window, player);
        }
    }

    for (let r = 3; r < ROWS; r++) {
        for (let c = 0; c < COLUMNS - 3; c++) {
            let window = [board[r][c], board[r - 1][c + 1], board[r - 2][c + 2], board[r - 3][c + 3]];
            score += evaluateWindow(window, player);
        }
    }

    return score;
}

function evaluateWindow(window, player) {
    let score = 0;
    let opponent = player === 1 ? 2 : 1;

    const playerCount = window.filter(x => x === player).length;
    const emptyCount = window.filter(x => x === 0).length;
    const opponentCount = window.filter(x => x === opponent).length;

    if (playerCount === 4) {
        score += 100;
    } else if (playerCount === 3 && emptyCount === 1) {
        score += 5;
    } else if (playerCount === 2 && emptyCount === 2) {
        score += 2;
    }

    if (opponentCount === 3 && emptyCount === 1) {
        score -= 4;
    }

    return score;
}

function minimax(board, depth, alpha, beta, maximizingPlayer) {
    if (checkWin(1)) {
        return { score: -1000 };
    } else if (checkWin(2)) {
        return { score: 1000 };
    } else if (checkDraw() || depth === 0) {
        return { score: evaluateBoard(board, 2) };
    }

    if (maximizingPlayer) {
        let maxEval = -Infinity;
        let bestColumn = null;

        for (let c = 0; c < COLUMNS; c++) {
            const row = getNextOpenRow(c);
            if (row !== -1) {
                const newBoard = board.map(arr => arr.slice());
                newBoard[row][c] = 2;
                const eval = minimax(newBoard, depth - 1, alpha, beta, false).score;
                if (eval > maxEval) {
                    maxEval = eval;
                    bestColumn = c;
                }
                alpha = Math.max(alpha, eval);
                if (beta <= alpha) break;
            }
        }
        return { score: maxEval, column: bestColumn };
    } else {
        let minEval = Infinity;
        let bestColumn = null;

        for (let c = 0; c < COLUMNS; c++) {
            const row = getNextOpenRow(c);
            if (row !== -1) {
                const newBoard = board.map(arr => arr.slice());
                newBoard[row][c] = 1;
                const eval = minimax(newBoard, depth - 1, alpha, beta, true).score;
                if (eval < minEval) {
                    minEval = eval;
                    bestColumn = c;
                }
                beta = Math.min(beta, eval);
                if (beta <= alpha) break;
            }
        }
        return { score: minEval, column: bestColumn };
    }
}

function aiMove() {
    if (gameOver) return;

    const { column } = minimax(board, 5, -Infinity, Infinity, true);
    if (column !== null) {
        const row = getNextOpenRow(column);
        board[row][column] = 2;
        const cell = document.querySelector(`.cell[data-row="${row}"][data-column="${column}"]`);
        const piece = document.createElement('div');
        piece.classList.add('piece', 'player2');
        cell.appendChild(piece);
        cell.classList.remove('empty');

        if (checkWin(2)) {
            message.textContent = `Player 2 (AI) wins!`;
            gameOver = true;
        } else if (checkDraw()) {
            message.textContent = "It's a draw!";
            gameOver = true;
        } else {
            currentPlayer = 1;
            message.textContent = `Player 1's turn`;
        }
    }
}

resetButton.addEventListener('click', () => {
    board = Array(ROWS).fill(null).map(() => Array(COLUMNS).fill(0));
    currentPlayer = 1;
    gameOver = false;
    createBoard();
    message.textContent = `Player 1's turn`;
});

createBoard();
message.textContent = `Player 1's turn`;
