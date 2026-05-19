
import { useContext } from "react";
import {useRef} from "react"
import { PostList } from "../store/postListStore";

const  CreatePost= () => {

  const {addPost}=useContext(PostList)

  const userIdElement = useRef();
  const postTitleElement = useRef();
  const postBodyElement = useRef();
  const reactionsElement = useRef();
  const tagsElement = useRef();


  const handleSubmit = (event) => {
    event.preventDefault()
    const userId = userIdElement.current.value;
    const postTitle = postTitleElement.current.value;
    const postBody = postBodyElement.current.value;
    const reactions = reactionsElement.current.value;
    const tags = tagsElement.current.value.split(" ");
    
    userIdElement.current.value = "";
    postTitleElement.current.value = "";
    postBodyElement.current.value = "";
    reactionsElement.current.value = "";
    tagsElement.current.value = "";


    addPost(userId, postTitle, postBody, reactions, tags);

  }

    return ( 


        <form className="createpost" onSubmit={handleSubmit}>

          <div className="mb-3">
            <label htmlFor="userId" className="form-label">User ID</label>
            <input ref={userIdElement} type="text" className="form-control" id="userId"  placeholder="Your user ID"/>
          </div>


          <div className="mb-3">
            <label htmlFor="title" className="form-label">Post Title</label>
            <input ref={postTitleElement} type="text"  className="form-control" id="title"  placeholder="How are you feeling today"/>
          </div>

          <div className="mb-3">
            <label htmlFor="body" className="form-label">Post Content</label>
            <textarea rows="4"  ref={postBodyElement}  className="form-control" id="body"  placeholder="Tell us about it"/>
          </div>


          <div className="mb-3">
            <label htmlFor="reactions" className="form-label">Number of Reactions</label>
            <input ref={reactionsElement} type="text" className="form-control" id="reactions"  placeholder="How man people reacted"/>
          </div>


          <div className="mb-3">
            <label htmlFor="tags" className="form-label">Enter your hashtags here</label>
            <input  ref={tagsElement} type="text"  className="form-control" id="tags"  placeholder="Enter tags using space"/>
          </div>

          

    
          <button type="submit" className="btn btn-primary">Post</button>
        </form>  );
}

export default CreatePost;










