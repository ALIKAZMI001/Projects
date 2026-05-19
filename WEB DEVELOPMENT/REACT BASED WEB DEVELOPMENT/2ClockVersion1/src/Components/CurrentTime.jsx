let  CurrentTime =() =>{

    let time=new Date();
    return <p>THIS IS THE CURRECT TIME {time.toLocaleDateString()} - {time.toLocaleTimeString()} </p>
}

export default CurrentTime;