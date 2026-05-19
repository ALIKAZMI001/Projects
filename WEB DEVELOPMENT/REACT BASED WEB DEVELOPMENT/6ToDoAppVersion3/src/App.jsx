
import AppName from "./Components/AppName.jsx";
import AddTodo from "./Components/AddTodo.jsx";
import TodoItems from "./Components/TodoItems.jsx";
import 'bootstrap/dist/css/bootstrap.min.css'
import "./App.css";
import {useState} from "react"

function App() {

  const INITIALtodoItems= [
    {
      name : "Buy Milk",
      dueDate :'4/10/2023',
    },

    {
      name : 'Go To College' ,
      dueDate :'4/10/2023',
    }
  ];

  const [todoItems,settodoItems] = useState(INITIALtodoItems)
  const onNewItem = (todoName,todoDate) => {

    console.log(todoName,todoDate)
    const  newTodoItems=[...todoItems, {
      name : todoName,
      dueDate :todoDate,
    }]
    settodoItems( newTodoItems)

    // settodoItems( (currValu)=>{

    //   const  newTodoItems=[...todoItems, {
    //     name : todoName,
    //     dueDate :todoDate,
    //   ];
    //   retun newTodoItems;

    // })

  }


  return <center className='TODO'>
            <AppName/>
            <AddTodo onNewItem={onNewItem}> </AddTodo>
            <TodoItems todoItems={todoItems}>  </TodoItems>
             
        </center>

  
}

export default App
