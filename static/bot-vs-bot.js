const resetButton = document.querySelector('.reset-btn')
const nextTurnButton = document.querySelector('.next-turn-btn')
const boxes = document.querySelectorAll('.cell')

let gameState = new Array(7).fill(null).map(row => new Array(7).fill(0))
let userTurn = true
let moveNum = 1
let userChar = 'X', botChar = 'O'

function gameOver(winner) {
    setTimeout(() => {
        alert(winner == "tie" ? "Tie Game" : `${winner} won`)
        boxes.forEach(box => {
            box.classList = ["cell"]
            box.textContent = ""
        })
    }, 300)
    gameState = new Array(7).fill(null).map(row => new Array(7).fill(0))
    userTurn = true
    return true
}

function checkGameOver(board) {
    for (let i = 0; i < 7; i++) {
        for (let j = 0; j < 4; j++) {
            // Check rows
            if (
                board[i][j] === 1 &&
                board[i][j + 1] === 1 &&
                board[i][j + 2] === 1 &&
                board[i][j + 3] === 1
            ) {
                return gameOver("Brockport Bot");
            } else if (
                board[i][j] === -1 &&
                board[i][j + 1] === -1 &&
                board[i][j + 2] === -1 &&
                board[i][j + 3] === -1
            ) {
                return gameOver("RIT Bot");
            }
            // Check columns
            if (
                board[j][i] === 1 &&
                board[j + 1][i] === 1 &&
                board[j + 2][i] === 1 &&
                board[j + 3][i] === 1
            ) {
                return gameOver("Brockport Bot");
            } else if (
                board[j][i] === -1 &&
                board[j + 1][i] === -1 &&
                board[j + 2][i] === -1 &&
                board[j + 3][i] === -1
            ) {
                return gameOver("RIT Bot");
            }
        }
    }
    // diagonals
    for (let i = 0; i < 4; i++) {
        for (let j = 0; j < 4; j++) {
            // Check diagonals from top-left to bottom-right
            if (
                board[i][j] === 1 &&
                board[i + 1][j + 1] === 1 &&
                board[i + 2][j + 2] === 1 &&
                board[i + 3][j + 3] === 1
            ) {
                return gameOver("Brockport Bot");
            } else if (
                board[i][j] === -1 &&
                board[i + 1][j + 1] === -1 &&
                board[i + 2][j + 2] === -1 &&
                board[i + 3][j + 3] === -1
            ) {
                return gameOver("RIT Bot");
            }
            // bottom right to top left
            if (
                board[i][j + 3] === 1 &&
                board[i + 1][j + 2] === 1 &&
                board[i + 2][j + 1] === 1 &&
                board[i + 3][j] === 1
            ) {
                return gameOver("Brockport Bot");
            } else if (
                board[i][j + 3] === -1 &&
                board[i + 1][j + 2] === -1 &&
                board[i + 2][j + 1] === -1 &&
                board[i + 3][j] === -1
            ) {
                return gameOver("RIT Bot")
            }
        }
    }
    if(!board.some(arr => arr.some(x => x == 0))) {
        return gameOver("tie")
    }
    return false
}

resetButton.addEventListener('click', ev => {
    gameState = new Array(7).fill(null).map(row => new Array(7).fill(0))
    userTurn = true
    boxes.forEach(box => {
        box.classList = ["cell"]
        box.textContent = ""
    })
})

nextTurnButton.addEventListener('click', ev => {
    body = JSON.stringify({state: gameState, move: moveNum})
    if(userTurn) {
        fetch('/rit-move', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: body
        }).then(res => res.json())
            .then(res => {
                let row = res.row 
                let col = res.col 
                gameState[row][col] = 1 
                let el = document.querySelector(`div[data-row="${row}"][data-col="${col}"]`)
                el.textContent = userChar
                el.classList.add(userChar)
                moveNum++
                userTurn = false
                checkGameOver(gameState)
            })
    } else {
        fetch('/move', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: body
        }).then(res => res.json())
            .then(res => {
                let row = res.row 
                let col = res.col 
                gameState[row][col] = 1 
                let el = document.querySelector(`div[data-row="${row}"][data-col="${col}"]`)
                el.textContent = botChar
                el.classList.add(botChar)
                moveNum++
                userTurn = true
                checkGameOver(gameState)
            })
    }
})

