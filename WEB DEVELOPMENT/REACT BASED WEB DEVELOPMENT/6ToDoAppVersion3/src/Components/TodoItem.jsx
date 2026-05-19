import { FaDeleteLeft } from "react-icons/fa6";

function TodoItem ({todoName,todoDate}){

    return (
     <div className="container">
        <div className="row kgRow">               
          <div className="col-6">
            {todoName}
          </div>
          <div className="col-4">
            {todoDate}
          </div>
          <div className="col-2">
             <button type="button" className="btn btn-danger kgbutton"><FaDeleteLeft />
             </button>
          </div>
        </div>
      </div>
     
    );
}

export default TodoItem