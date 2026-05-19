import styles from './Display.module.css'


const Display = ({calvalue}) => {
    return (
        <input className={styles.display} type="text" value={calvalue} readOnly />
    
    )
}

export default Display;