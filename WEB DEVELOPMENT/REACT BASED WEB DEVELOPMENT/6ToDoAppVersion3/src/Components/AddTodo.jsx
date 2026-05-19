import {useState , useRef} from "react" // USEREF HAR BAR LETER ENTE KRTE WKT REPAINT BAR BAR NI KRTA
import { IoIosAddCircleOutline } from "react-icons/io";

function AddTodo ({onNewItem}){

  let [todoName,setTodoName] = useState();
  let [todoDate,setTodoDate] = useState();

  const noOfUpdates=useRef(0)
  const todoNameElements=useRef();
  const todoDateElements=useRef();

  const handleNAMEChange = (event) => {

    setTodoName(event.target.value)
    noOfUpdates.current +=1;

  }

  const handleDATEChange = (event) => {
     setTodoDate(event.target.value)
     console.log( noOfUpdates.current)
    
  }

  const handleAddbutton = () => {
    // const todoName =  todoNameElements.current.value     FROM INPUTS REMOVE ALL OTHER FUNCTIONS ;UST HANDLEADDBUTTON FUN WILL DO ITS ;OB
    // const todoDate=todoDateElements.current.value
    onNewItem(todoName,todoDate)

  }

    return (
     <div className="container">
         <form className="row kgRow">               
           <div className="col-6">
             {<input type="text" /* ref={todoNameElements}*/ placeholder="Enter Todo Here" onClick={handleNAMEChange} /> }
           </div>
           <div className="col-4">
             <input type="date" ref={todoDateElements} onClick={handleDATEChange} />
           </div>
           <div className="col-2">
           <button type="button" className="btn btn-success kgbutton"
           onClick={handleAddbutton}>
            <IoIosAddCircleOutline /></button>
           </div>
         </form>
     </div>
    );
}

export default AddTodo