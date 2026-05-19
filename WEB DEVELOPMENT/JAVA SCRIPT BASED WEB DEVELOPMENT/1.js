// document.body.childNodes[3].innerText= "abcd"


// let a=document.getElementById("ok")
// console.dir(a);
// console.log(a)


// let b =document.getElementsByClassName("o")
// console.dir(b);
// console.log(b);



// let c =document.getElementsByTagName("p")
// console.dir(c);
// console.log(c);


// let d=document.querySelector("p")
// console.dir(d);
// console.log(d);


// let e=document.querySelectorAll("p")
// console.dir(e);
// console.log(e);


// let d=document.querySelector("p")
// console.dir(d);
// console.log(d);


// let e=document.querySelectorAll(".ok")
// console.dir(e);
// console.log(e);



// console.dir(document.body.firstChild);


// let a=document.querySelector("div")
// console.dir(a)
// a.innerText
// a.innerText="ok"
// a.innerHTML="<i>ok<i>"


//////////////////////////////////////////////////////////////////////////////////////


// let a=document.querySelector("h1").append(" from Apna College")

// let a=document.querySelector("h1")
// console.dir(a.innerText)
// a.innerText=a.innerText+" from Apna College"



// let a=document.querySelectorAll(".ok")
// console.dir(a)
// a[0].innerText="ali"
// a[1].innerText="kazmi"
// a[2].innerText="g"


// let a=document.querySelectorAll(".ok")
// let x=1
// for (i of a){
//     i.innerText='number is' + x
//     x++
// }
    

///////////////////////////////////////////////////////////////////////////////////////////

// let a=document.querySelector("div")
// console.log(a)
// let id=a.getAttribute("id")
// console.log(id)


// let a=document.querySelector("div")
// console.log(a.setAttribute("class" , "kk"))



// let a=document.querySelector("div")
// a.style.backgroundColor="red"
// a.style.textDecoration="underline"
// a.style.color="pink"
// a.innerText="ali"


// let a=document.createElement("button")
// a.innerText="click me"
// console.log(a)
// let b=document.querySelector("div")
// b.append(a)
// b.prepend(a)
// b.before(a)
// b.after(a)


// let a=document.createElement("h1")
// a.innerHTML="<i>ali g</i>"
// b=document.querySelector("div")
// b.before(a)
// a.style.backgroundColor="yellow"


// let a=document.querySelector("p")
// a.remove()



// let a=document.createElement("button")
// a.innerText="click me"
// a.style.backgroundColor="red"
// a.style.color="white"
// let b=document.querySelector("body")
// b.prepend(a)



// let b=document.querySelector("p")
// b.classList.add("newclass")



/////////////////////////////////////EVENTS/////////////////////////////////////////////////////////


// let a=document.querySelector("#btn1")
// a.onclick=(e)=>{
//     console.log(e)
//     console.log(e.type)
//      console.log(e.target)   
//     console.log("button was clicked")
// }


// let b=document.querySelector("#btn2")
// b.ondblclick=()=>{
//     console.log("button was clicked 2 times")
//     alert('hellow')
// }


// let c=document.querySelector("div ")
// c.onmouseover=()=>{
//     console.log("ur in div")
   
// }


// let a=document.querySelector("#btn1")
// a.addEventListener("click",()=>{
//     console.log("button")
// })


// a.addEventListener("dblclick",()=>{
//     console.log("button2")
// })




// let a=document.querySelector("#btn1")
// let b=document.querySelector("body")
// let mode="light"
// a.addEventListener("click",()=>{
//     if(mode === "light"){
//         mode="dark"
//         b.classList.add("dark")
//         b.classList.remove("light")
//         }
//     else
//     {
//         mode="light"
//         b.classList.add("light")
//         b.classList.remove("dark")

//     }
//     console.log(mode)
// })




//////////////////////////////////////tic tak to game///////////////////////////////////////////////

// let a=document.querySelectorAll(".box")
// let b=document.querySelector("#restbtn")
// let c=document.querySelector("#msg")
// let d=document.querySelector(".msgc")

// let turnO=true
// let count = 0; //To Track Draw

// const pattern=[
//     [0,1,2],
//     [0,3,6],
//     [0,4,8],
//     [1,4,7],
//     [2,5,8],
//     [2,4,6],
//     [3,4,5],
//     [6,7,8],
// ]



// const resetgame=()=>{
//     turnO=true;
//     enableboxes();
//     d.classList.add("hide");

// }



// a.forEach((box)=>{
//     box.addEventListener("click",()=>{

//         if (turnO === true){
//             box.innerText="O"
//             turnO=false
//         }
//         else
//         {
//             box.innerText="X"
//             turnO=true
//         }

//         box.disabled=true

//         count++;

//         let isWinner = checkwinner();
    
//         if (count === 9 && !isWinner) {
//           gameDraw();
//        }
//     })
// })



// const gameDraw = () => {
//     c.innerText = `Game was a Draw.`;
//     d.classList.remove("hide");
//     disableboxes();
//   };


// const disableboxes=()=>{
//     for (box of a){
//         box.disabled=true
//     }
// }


// const enableboxes=()=>{
//     for (let box of a){
//         box.disabled=false
//         box.innerText= ""
//     }
// }


// const showwinner=(p1)=>{
//     c.innerText = `Congratulations, Winner is ${p1}`;
//     d.classList.remove("hide")
//     disableboxes()
// }


// const checkwinner=()=>{
//     for (let p of pattern){
//         let p1=a[p[0]].innerText
//         let p2=a[p[1]].innerText
//         let p3=a[p[2]].innerText

//     if(p1 != "" &&   p2 != ""  &&  p3 != ""){

//         if(p1===p2 &&  p2===p3){
//             console.log("winner",p1)
//             showwinner(p1)
//             return true;
//         }
//     }
//  }  
// }

// b.addEventListener("click", resetgame);





//////////////////////////////////////////////////ROCK PAPER SICCOR///////////////////////////////////////////////////////////////

// let userscore=0
// let compscore=0

// let a=document.querySelectorAll(".gg")
// let b=document.querySelector("#msg")
// let c=document.querySelector("#you")
// let d=document.querySelector("#computer")


// const generatecompchoice=()=>{

//     const options=["rock" ,"paper" ,"scissor"]
//     q=Math.floor(Math.random()*3)
//     return options[q]

// }


// const showwinner=(userwin)=>{

//     if(userwin === true){
//         console.log("your win")
//         b.innerText="you win!"
//         b.style.backgroundColor="green"
//         s=++userscore
//         c.innerText=s
//     }
//     else{
//         console.log("computers win")
//         b.innerText="you loss!"
//         b.style.backgroundColor="red"
//         g=++compscore
//         d.innerText=g
//     }

// }


// const playgame=(userid)=>{

//     console.log("your choice",userid)
//     const compchoice=generatecompchoice()
//     console.log("computers choice",compchoice)


//     if(userid === compchoice){
//         console.log("game was a draw")
//         b.innerText="DRAW"
//         b.style.backgroundColor="grey"
//     }

//     else{
//         let userwin=true
//         if(userid==="rock"){
//             userwin= compchoice === "paper" ? false : true
//         }
//         else if(userid==="paper"){
//             userwin= compchoice === "scissor" ? false : true
//         }
//         else {
//             userwin= compchoice === "rock" ? false : true
//         }

//         showwinner(userwin)
//     }

// }


// a.forEach((choice)=>
// {
//     choice.addEventListener('click',()=>{

//         const userid=choice.getAttribute("id")
//         playgame(userid)



//     })
// })







///////////////////////////////////////////////class and object/////////////////////////////////////////////////


// const student={
//     fullName :"ali",
//     marks: 21,
//     paramiter:function () {
//         console.log(this.marks)   
//     },
// }



// const employ={
//     tax(){
//         console.log("10% ktoti")
//     }

// }
// const ali ={
//     slarey : 5000,
// }
// ali.__proto__=employ





// class car {
//     constructor(brand,speed){

//         console.log("constructor bhn cho")
//         this.brand = brand
//         this.speed=speed
//     }

//     start(){
//         console.log("start")
//     }


//     stop(){
//         console.log("stop")
//     }

// }
// let fortuner= new car("fortuner",2100);
// console.log(fortuner)
// let lexus = new car("lexus",561);
// console.log(lexus)









// class car {


//     constructor(name){

//                 console.log("constructor paret bhn cho")
//                 this.specie="homospecie"
//                 this.name=name
//             }

//     stop(){
//         console.log("stop")
//     }

// }


// class ali extends car {

    
//     constructor(name,age){


//         console.log("constructor chld en")
//         super(name)
//         this.age = age
//         console.log("constructor chld bahir")
    
//     }

//     run(){
//         super.stop()
//         console.log("run bhj")
//     }


// }

// obj=new ali("hla",112)







// class user {

//     constructor(name,email){

//         this.name=name
//         this.email=email
//     }

//     viewData(){
//         console.log("view website")
//     }
// }


// class admin extends user{


//     constructor(name,email){
//         super(name,email)
//     }

//     editdata(){
//         super.viewData()
//         console.log("edit data")
        
//     }
// }

// a=new user("ali","ali984kazmi@gmail.com")
// a.viewData()

// let ad=new admin("ahmed","ali984kazmi@gmail.com")
// ad.editdata()



/////////////////////////////////////////Asyncronus////////////////////////////////////////////////////


// console.log("one")
// console.log("one")
// setTimeout(()=>{
//     console.log("hellow")
//  },1000)
// console.log("one")
// console.log("one")




// function sum(a,b){
//     console.log(a+b)
// }

// function ali(a,b,ab){
//     ab(a,b)
// }
// ali(1,2,sum)



// function getData(dataID){

//     setTimeout(()=>{
//         console.log("data",dataID)
//     },2000)
// }


//////////////call BACK/////////////////////////////////

// function getData(dataID,nextID){

//     setTimeout(()=>{
//         console.log("data",dataID)
//         if(nextID){
//             nextID()
//         }
//     },2000)
// }

// getData(1,()=>{
//     getData(2,()=>{
//         getData(3)
//     })
// })


//////////////Promise/////////////////////////////////



// const getPromise=()=>{
//     return new Promise((resolve ,reject)=>{
//         console.log("promise hun")
//         reject("success")
//     })
// }

// let promise=getPromise()
// promise.then((res)=>{

//     console.log("promise fullfiled")

// })

// promise.catch((err)=>{

//     console.log("promise rejected",err)

// })
    
    







// function getData(dataID,nextID){

//     return new Promise((resolve,reject)=>{

//         setTimeout(()=>{
//             console.log("data",dataID)
//             resolve("success")
//             if(nextID){
//                 nextID()
//             }
//         },5000)
//     })
// }






// function asyncFunc(){

//     return new Promise((resolve,reject)=>{

//                 setTimeout(()=>{
//                     console.log("some data1")
//                     resolve("success")
//                 },4000)
//             })
// }


// function asyncFunc2(){

//     return new Promise((resolve,reject)=>{

//                 setTimeout(()=>{
//                     console.log("some data2")
//                     resolve("success")
//                 },4000)
//             })
// }



// console.log("fetching data1......")
// let p1= asyncFunc()
// p1.then((res)=>{
//     console.log(res)
//     console.log("fetching data2......")
//    let p2= asyncFunc2()
//    p2.then((res)=>{
//    console.log(res)
// })
// })


// function getData(dataID){

//     return new Promise((resolve,reject)=>{
//         setTimeout(()=>{
//             console.log("data",dataID)
//             resolve("success")
//         },5000)
//     })
// }


// let p1=getData(1)
// p1.then((res)=>{
//     console.log(res)
// })


/////////////////////////////////////Async Function//////////////////////////////////


// function api(){

//     return new Promise((resolve,reject)=>{
//         setTimeout(()=>{
//             console.log("weather data")
//             resolve("200")
//         },2000)
//     })
// }

// async function getweatherdata(){
//     await api()
//     await api()
// }




// function getData(dataID){

//     return new Promise((resolve,reject)=>{
//         setTimeout(()=>{
//             console.log("data",dataID)
//             resolve("success")
//         },2000)
//     })
// }
// async function data (){
//     await getData(1)
//     await getData(2)
//     await getData(3)
// }



///IFFI/ KHUS KAM KRE GA NO CALL//

// (async function(){
//     await getData(1)
//     await getData(2)
//     await getData(3)
// })()







//////////////////////////////////////API//////////////////////////////////////////////////////


// let a=document.querySelector(".ok")
// let b=document.querySelector(".gg")


// const URL="https://cat-fact.herokuapp.com/facts"

// const  getfacts = async ()=>{

//     let promise= await fetch(URL)
//     console.log(promise)
//     let data =await promise.json()
//     let c= data[0].text
//     b.innerText=c
// }

// a.addEventListener("click",getfacts)






// let a=document.querySelector(".ok")
// let b=document.querySelector(".gg")


// const URL="https://cat-fact.herokuapp.com/facts"

// const  getfacts =  ()=>{

//     fetch(URL)
//     .then((res)=>{
//       return res.json()

//     })

//     .then((data)=>{

//         console.log(data)
//         let c= data[0].text
//         b.innerText=c
//     })

// }

// a.addEventListener("click",getfacts)




/////////////////////////////////CURRENCY CONVERTER///////////////////////////////////////





const dropdowns = document.querySelectorAll(".to select, .from select");
const btn = document.querySelector("form button");
const msgDiv = document.querySelector(".msg");
const amountInput = document.querySelector(".amount input"); // Getting the amount input field
const apiKey = '06c0ec13b49a9dc974ce6405';
let fromCurrency = 'USD';
let toCurrency = 'PKR';

// Function to update the flag based on the selected currency
const updateFlag = (element) => {
    let currencyCode = element.value;
    let countryCode = countryList[currencyCode];
    let newSrc = `https://flagsapi.com/${countryCode}/flat/64.png`;
    let img = element.parentElement.querySelector("img");
    img.src = newSrc;
};

const fetchExchangeRate = async () => {
    try {
        const apiURL = `https://v6.exchangerate-api.com/v6/${apiKey}/latest/${fromCurrency}`;
        const amount = amountInput.value; // Get the entered amount

        const response = await fetch(apiURL); // Wait for the fetch response
        const data = await response.json(); // Wait for the JSON conversion

        const conversionRate = data.conversion_rates[toCurrency];
        const convertedAmount = (amount * conversionRate).toFixed(2); // Calculate the converted amount

        msgDiv.innerText = `${amount} ${fromCurrency} = ${convertedAmount} ${toCurrency}`; // Display result
    } catch (error) {
        console.error('Error fetching the exchange rate:', error); // Handle any errors
    }
};

// Populate dropdowns with currency options
for (let select of dropdowns) {
    for (let currencyCode in countryList) {
        let newOption = document.createElement("option");
        newOption.innerText = currencyCode;
        newOption.value = currencyCode;

        if (select.name === "from" && currencyCode === "USD") {
            newOption.selected = "selected";
        } else if (select.name === "to" && currencyCode === "PKR") {
            newOption.selected = "selected";
        }

        select.append(newOption);
    }

    select.addEventListener("change", (evt) => {
        updateFlag(evt.target);

        if (evt.target.name === "from") {
            fromCurrency = evt.target.value;
        } else if (evt.target.name === "to") {
            toCurrency = evt.target.value;
        }

       
    });
}

// Event listener for the form button (when clicked)
btn.addEventListener("click", (evt) => {
    evt.preventDefault();

    let amount = amountInput.value;

    if (amount === "" || amount < 1) {
        amount = 1;
        amountInput.value = "1"; // Set the amount input to 1 if it's invalid
    }

    fetchExchangeRate(); // Update rate when button is clicked
});


