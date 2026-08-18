let a = document.querySelectorAll(".box")
let b = document.querySelector("#restbtn")
let c = document.querySelector("#msg")
let d = document.querySelector(".msgc")

let turnO = true
let count = 0

const pattern = [
    [0, 1, 2],
    [0, 3, 6],
    [0, 4, 8],
    [1, 4, 7],
    [2, 5, 8],
    [2, 4, 6],
    [3, 4, 5],
    [6, 7, 8],
]

const resetgame = () => {
    turnO = true;
    enableboxes();
    d.classList.add("hide");
}

a.forEach((box) => {
    box.addEventListener("click", () => {
        if (turnO === true) {
            box.innerText = "O"
            turnO = false
        }
        else {
            box.innerText = "X"
            turnO = true
        }

        box.disabled = true

        count++;

        let isWinner = checkwinner();

        if (count === 9 && !isWinner) {
            gameDraw();
        }
    })
})

const gameDraw = () => {
    c.innerText = `Game was a Draw.`;
    d.classList.remove("hide");
    disableboxes();
};

const disableboxes = () => {
    for (box of a) {
        box.disabled = true
    }
}

const enableboxes = () => {
    for (let box of a) {
        box.disabled = false
        box.innerText = ""
    }
}

const showwinner = (p1) => {
    c.innerText = `Congratulations, Winner is ${p1}`;
    d.classList.remove("hide")
    disableboxes()
}

const checkwinner = () => {
    for (let p of pattern) {
        let p1 = a[p[0]].innerText
        let p2 = a[p[1]].innerText
        let p3 = a[p[2]].innerText

        if (p1 != "" && p2 != "" && p3 != "") {
            if (p1 === p2 && p2 === p3) {
                console.log("winner", p1)
                showwinner(p1)
                return true;
            }
        }
    }
}

b.addEventListener("click", resetgame);