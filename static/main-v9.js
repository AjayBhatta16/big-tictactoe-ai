const resetButton = document.querySelector('.md-button')
const boxes = document.querySelectorAll('.cell')

let gameState = new Array(9).fill(null).map(row => new Array(9).fill(0))
let userTurn = true
let moveNum = 1
let userChar = 'X', botChar = 'O'

resetButton.addEventListener('click', ev => {
    gameState = new Array(9).fill(null).map(row => new Array(9).fill(0))
    userTurn = true
    boxes.forEach(box => {
        box.classList = ["cell"]
        box.textContent = ""
    })
})

boxes.forEach(box => {
    box.addEventListener('click', ev => {
        if(userTurn) {
            moveNum++
            userTurn = false 
            let row = ev.target.dataset.row 
            let col = ev.target.dataset.col 
            if(gameState[row][col] != 0) return
            ev.target.textContent = userChar
            ev.target.classList.add(userChar)
            gameState[row][col] = -1
            body = JSON.stringify({state: gameState, move: moveNum})
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
                })
        }
    })
})

