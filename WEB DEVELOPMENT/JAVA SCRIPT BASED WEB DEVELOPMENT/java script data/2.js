// const product={
// title:" Ball Pen ",
// rating:4,
// offer:5,
// price:270
// }
// console.log(product);
// console.log(product.title);



// const profile={
//     username:"ali kazmi",
//     isfollow:false,
//     followers:123,
//     following:123
//     }
//     console.log(profile);
//     console.log(typeof profile["username"])


// //operaters
// let a=5
// let b=3
// console.log("a + b = ",a+b)
// console.log("a ** b = ",a**b)
// console.log("a % b = ",a%b)


// //unery operaters
// let a=1
// let b=2
// // a++
// // a--
// // console.log("a ++ = ",a)
// a+=4//a=a+4
// console.log("a + = 4 ",a)


// // comparison
// let a=1
// let b="1"
// console.log("5==2 ",a==b)
// console.log("5===2 ",a===b)



// // logical oprators
// let a=3
// let b=2
// let cond1=a>b
// let cond2=a===4
// console.log("cond1 && cond2 ",cond1 && cond2)
// console.log("cond1 || cond2 ",cond1 || cond2)
// console.log("!(a<b) ",!(a<b))



// n=0
// if(n>0)
//     console.log(n ,"is positive")
// else if(n<0)
//     console.log(n ,"is negative")
// else
// console.log(n ,"is zero")


// let age=22
// let result=age>=18?"legal":"ilegal"
// console.log(result)


// let a=prompt("enter a number=")
// if(a%5===0)
//     console.log(a,"is multile of 5")
// else
//     console.log(a,"is not multile of 5")





// let a=prompt("enter your score=")
// if (a<=100 && a>=80)
//     console.log(a,"grade for this score is A")
// else if(a<80 && a>=70)
//     console.log(a,"grade for this score is B")
// else if(a<70 && a>=60)
//     console.log(a,"grade for this score is C")
// else if(a<60 && a>=50)
//     console.log(a,"grade for this score is D")
// else   console.log(a,"grade for this score is F")


// for(i=0;i<=5;i++)
//     console.log("ali kazmi manic")


// let a=0
// for(i=1;i<=5;i++)
//     a=i+a
//      console.log(a)



// for(i=0;i<=100;i++)
//     if(i%2===0)
//        console.log("even number is",i)


 
// ok="im ali \n kazmi gg"
// ko=" sale \t"
// console.log(ok)
// console.log(ok.length)
// console.log(ok.toUpperCase())
// console.log(ok.slice(0,6)) 
// console.log(ko+ok+"\t hla") 


// a="hellow"
// console.log(a.replace("w" , "1"))


// a=prompt("enter name bharwe")
// b=a.length
// console.log("@" + a + b)


// arry=["ali","kazmi"]
// arry[0]="ok"
// console.log(arry)



// arry=["ali","kazmi"]
// for (let i=0 ;i<arry.length;i++)
//     console.log(arry[i])



// arry=[12,12,10,10]
// let sum=0 
// for (let i=0 ;i<arry.length;i++)
// {
//     sum=sum+arry[i]
// }
// console.log(sum)
// avg=sum/arry.length
// console.log(avg)



// arry=[250,645,300,900]
// for (let i=0 ;i<arry.length;i++)
// {   
//     a=arry[i] * 0.1
//     b=arry[i] - a
//     console.log(b)
// }


// arry=[1,4,5,6,7,8,5,3,4,5,12,10,10]
// ar=[12,12,12,12]
// arry.push(777)
// console.log(arry)
// arry.pop()
// console.log(arry)
// console.log(arry + ar)
// let a=arry.concat(ar)
// console.log(a)


// arry=[1,4,5,6,7,8,2,3,9]
// b=arry.slice(0,2)
// console.log(b);
// arry=[1,2,3,4,5,6,7]
// arry.splice(2,0,101,102)


// array=["a","b","c","d","e"]
// // array.splice(0,1)
// // array.splice(2,1,'ola')
// array.push("amazon")



// function ali(a,b) {
//     s=a+b
//     console.log(s)
//     return s
// }
// d=ali(1,2);
// console.log("ok g ",d)




//  ali=(a,b) => {
//     s=a+b
//     console.log(s)
    
// }




// function ali(a){
//     let count=0
//     for(const char of a){
//         if (char === "a"||
//             char==="e"||
//             char==="i"||
//             char==="o"||
//             char==="u"){ 
//                 count ++
//             }
//     }       
//     console.log(count)
// }
// ali("abocd")




// const x=(a)=>{
//     let count=0
//     for(const char of a){
//         if (char === "a"||
//             char==="e"||
//             char==="i"||
//             char==="o"||
//             char==="u"){ 
//                 count ++
//             }
//     }       
//     console.log(count)
// }
// x("abocd")




// array=[12,6,3,1]
// array.map((a)=>{
//     console.log(a*a)

// })



// array=[12,6,3,1]
// let ok=array.filter((a)=>{
//     return a===1
// })
// console.log(ok)


// array=[87,62,91,98]
// let ok=array.filter((a)=>{
//     return a>90
// })
// console.log(ok)



