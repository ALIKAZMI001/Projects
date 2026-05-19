
import 'bootstrap/dist/css/bootstrap.min.css'

import Display from './Components/Display.jsx'
import ButtonContainer from './Components/ButtonContainer.jsx'
import styles from './App.module.css'
import {useState} from "react"

function App() {

 let [calvalue,setcalvalue] = useState("")
  const onClick =  (buttonText) => {

     if (buttonText === 'c') {
         const Newcalvalue = ""
         setcalvalue(Newcalvalue)
     }
     else if (buttonText === '=') {
           const result = eval(calvalue)
           setcalvalue( result)
     }
     else{
      const newDisplaValue=calvalue + buttonText;
      setcalvalue(newDisplaValue)
     }

  }

  return (
   <div className={styles.calculator}>
      <Display calvalue={calvalue} ></Display>
      <ButtonContainer  onClick={onClick}></ButtonContainer>
      
   </div>
  )
}

export default App
