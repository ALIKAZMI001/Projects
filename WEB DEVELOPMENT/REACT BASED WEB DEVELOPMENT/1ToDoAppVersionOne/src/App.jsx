
import AppName from "./Components/AppName.jsx";
import AddTodo from "./Components/AddTodo.jsx";
import TodoItem1 from "./Components/TodoItem1.jsx";
import TodoItem2 from "./Components/TodoItem2.jsx";
import "./App.css";

function App() {

  return <center className='TODO'>
            <AppName/>
            <AddTodo/>

            <div className="itemsContainer">
              <TodoItem1></TodoItem1>
              <TodoItem2></TodoItem2>

            </div>
           
             
        </center>

  
}

export default App
