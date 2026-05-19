import { useContext } from "react";
import  Post from "./Post.jsx"
import { PostList as PostListData } from "../store/postListStore.jsx";



const  PostList= () => {

   const {postList}= useContext(PostListData);


    return <>{postList.map((post)=>(<Post key={post.id} post={post}/>

    ))}</>
}

export default PostList;