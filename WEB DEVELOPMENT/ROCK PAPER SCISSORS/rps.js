let userscore = 0
let compscore = 0

let a = document.querySelectorAll(".gg")
let b = document.querySelector("#msg")
let c = document.querySelector("#you")
let d = document.querySelector("#computer")

const generatecompchoice = () => {
    const options = ["rock", "paper", "scissor"]
    q = Math.floor(Math.random() * 3)
    return options[q]
}

const showwinner = (userwin) => {
    if (userwin === true) {
        console.log("your win")
        b.innerText = "you win!"
        b.style.backgroundColor = "green"
        s = ++userscore
        c.innerText = s
    }
    else {
        console.log("computers win")
        b.innerText = "you loss!"
        b.style.backgroundColor = "red"
        g = ++compscore
        d.innerText = g
    }
}

const playgame = (userid) => {
    console.log("your choice", userid)
    const compchoice = generatecompchoice()
    console.log("computers choice", compchoice)

    if (userid === compchoice) {
        console.log("game was a draw")
        b.innerText = "DRAW"
        b.style.backgroundColor = "grey"
    }
    else {
        let userwin = true
        if (userid === "rock") {
            userwin = compchoice === "paper" ? false : true
        }
        else if (userid === "paper") {
            userwin = compchoice === "scissor" ? false : true
        }
        else {
            userwin = compchoice === "rock" ? false : true
        }

        showwinner(userwin)
    }
}

a.forEach((choice) => {
    choice.addEventListener('click', () => {
        const userid = choice.getAttribute("id")
        playgame(userid)
    })
})