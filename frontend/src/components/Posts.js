import React from 'react';
import Post from './Post';

const Posts = ({ posts }) => {
  return (
    <section>
      <div className="title">
        <h2>Your Items</h2>
        <div className="underline"></div>
      </div>
      <div>
        {posts.map((post) => {
          return <Post key={post.post_id} {...post}/>;
        })}
      </div>
    </section>
  );
};

export default Posts;