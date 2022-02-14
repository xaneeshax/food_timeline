import React, { useState } from 'react';

const Post = ({post_id, item, pic_url, location, timestamp, review, rating}) => {
  const [readMore, setReadMore] = useState(false);
  return (
    <article className="single-item">
      <h4 class="title">{item}</h4>
      <img src={pic_url} alt="" /> 
      <footer>
        <div class="item-info" >
          <h5>{location}</h5>
          <h5>{timestamp}</h5>
        </div>
        <div class="background">
          <h5 className="item-price">Would Go Again? {rating}</h5>
        
          <p>
            {readMore ? review : `Review: ${review.substring(0, 200)}...`}
            <button onClick={() => setReadMore(!readMore)}>
              {readMore ? 'show less' : '  read more'}
            </button>
          </p>
        </div>
      </footer>
    </article>
  );
};

export default Post;