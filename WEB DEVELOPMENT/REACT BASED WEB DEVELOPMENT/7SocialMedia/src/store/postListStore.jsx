import { createContext, useState } from "react";

export const PostList = createContext({
    postList: [],
    addPost: () => {},
    deletePost: () => {}
});



const PostListProvider = ({ children }) => {
    const [postList, setPostList] = useState(DEFAULT_POST_LIST);

    const addPost = (userId, postTitle, postBody, reactions, tags) => {
        setPostList((prevPostList) => [
            ...prevPostList,  // Keep existing posts
            {
                id: Date.now(), // Generate a unique ID
                title: postTitle,
                body: postBody,
                reactions: reactions,
                userId: userId,
                tags: tags,
            }
        ]);
    };
    
    const deletePost = (postId) => {
        setPostList((prevPostList) => prevPostList.filter((post) => post.id !== postId));
    };

    return (
        <PostList.Provider value={{ postList, addPost, deletePost }}>
            {children}
        </PostList.Provider>
    );
};

export default PostListProvider;


const DEFAULT_POST_LIST = [
  {
      id: "1",
      title: "Going to Mumbai",
      body: "Hi Friends, I am going to Mumbai for my vacations. Hope to enjoy a lot. Peace out.",
      reactions: 2,
      userId: "user-9",
      tags: ["vacation", "Mumbai", "Enjoying"]
  },
  {
      id: "2",
      title: "Paas ho bhai",
      body: "4 saal ki masti k baad bhi ho gaye hain paas. Hard to believe.",
      reactions: 15,
      userId: "user-12",
      tags: ["Graduating", "Unbelievable"]
  }
];
