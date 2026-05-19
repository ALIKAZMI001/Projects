
import styles from './ButtonContainer.module.css'

const ButtonContainer = ({onClick}) => {

    const buttonNames=['c','1','2','+','3','4','-','5','6','*','7','8','/','=','9','0','.']
    return (
        <div className={styles.buttonCont}>

            {buttonNames.map((item)=>(<button className={styles.button} onClick={()=>onClick(item)}>{item}</button>))}
             
           
        </div> 
    )
}

export default ButtonContainer;