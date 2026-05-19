
import 'bootstrap/dist/css/bootstrap.min.css'

import Display from './Components/Display.jsx'
import ButtonContainer from './Components/ButtonContainer.jsx'
import styles from './App.module.css'

function App() {

  return (
   <div className={styles.calculator}>
      <Display></Display>
      <ButtonContainer></ButtonContainer>
      
   </div>
  )
}

export default App
