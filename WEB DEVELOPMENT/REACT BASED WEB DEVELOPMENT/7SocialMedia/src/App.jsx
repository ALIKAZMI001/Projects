
import "bootstrap/dist/css/bootstrap.min.css"
import './App.css'
import Header from "./Components/Header.jsx"
import Footer from "./Components/Footer.jsx"
import Sidebar from "./Components/Sidebar.jsx"
import  CreatePost from "./Components/CreatePost.jsx"
import  Post from "./Components/Post.jsx"
import  PostList from "./Components/PostList.jsx"
import {useState} from "react"
import PostListProvider from "./store/postListStore.jsx"

function App() {

  const [SelectedTab,setSelectedTab] = useState("Home")
 
  return (

    <PostListProvider>
     <div className="appContainer">  
      <Sidebar SelectedTab={SelectedTab}  setSelectedTab={setSelectedTab}></Sidebar>
      <div className="content">
      <Header></Header>
      {SelectedTab === "Home"  ? <PostList></PostList>:<CreatePost></CreatePost>}
      <Footer></Footer>
      </div>
      </div>
    </PostListProvider>
  
      
    

 
  )
}

export default App
