
import AppName from "./Components/AppName.jsx";
import AddTodo from "./Components/AddTodo.jsx";
import TodoItems from "./Components/TodoItems.jsx";
import 'bootstrap/dist/css/bootstrap.min.css'
import "./App.css";

function App() {

  const todoItems= [
    {
      name : "Buy Milk",
      dueDate :'4/10/2023',
    },

    {
      name : 'Go To College' ,
      dueDate :'4/10/2023',
    }
  ];

  return <center className='TODO'>
            <AppName/>
            <AddTodo/>
            <TodoItems todoItems={todoItems}>  </TodoItems>
             
        </center>

  
}

export default App
