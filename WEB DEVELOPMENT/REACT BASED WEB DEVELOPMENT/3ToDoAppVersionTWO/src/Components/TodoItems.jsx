
import TodoItem from "./TodoItem"
import styles from "./TodoItems.module.css"

const TodoItems = ({ todoItems}) => {

    return (
        <div className={styles.itemsContainer}>

          {todoItems.map((items) => (<TodoItem todoName={items.name}  todoDate={items.dueDate}></TodoItem>))}

      </div>
     
    )
}

export default TodoItems