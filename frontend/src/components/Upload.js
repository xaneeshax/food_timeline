import React from 'react'

const API = process.env.REACT_APP_API;

export const Upload = () => {

    return (
         <article>
             <h1>Create a Post</h1>
             
             <form method="POST" action={`${API}/create_post`}  encType="multipart/form-data" id="post-form" className="single-item">
                 <div className='title'>
                     <input 
                         type="text" 
                         name="username" 
                         className="form-control"
                         placeholder="Username"
                     />
                </div>
                <div className="title">
 
                     <input 
                         type="text"
                         name="item" 
                         className="form-control"
                         placeholder="Item"
                     />
                </div>
                <div className="title">
 
                     <input 
                         type="text"
                         name="location"   
                         className="form-control"
                         placeholder="Location"
                     />
                </div>
                <div className="title">
 
                     <input
                         type="text" 
                         name="review"   
                         className="form-control"
                         placeholder="Review"
                     />
                </div>
                <div className="title">
                     <input 
                         type="text" 
                         name="rating"   
                         className="form-control"
                         placeholder="Yes or No"
                     />

                </div>
                <div className="title">
                     
                     <input 
                         type="file" 
                         className="form-control"
                         name="profile_image" />

                </div>
                <div className="title">
                     
                     <input 
                         type="submit" 
                         className="form-control"
                     />
                 </div> 
             </form>
         </article>
    )
 }

/*
export const Upload = () => {

   return (
        <div>
            <h1>Upload Image</h1>
            
            <form method="POST" action={`${API}/cloud_upload`}  encType="multipart/form-data" id="post-form" className="card card-body">
                <div className='form-group'>
                    <input 
                        type="text" 
                        name="username" 
                        className="form-control"
                        placeholder="Username"
                    />

                    <input 
                        type="text"
                        name="location"   
                        className="form-control"
                        placeholder="Location"
                    />

                    <input
                        type="text" 
                        name="review"   
                        className="form-control"
                        placeholder="Review"
                    />

                    <input 
                        type="number" 
                        id="rating" 
                        name="rating"
                        placeholder="Rating" 
                        className="form-control"
                        min="1.0" 
                        max="5.0"
                    />
                    
                    <input 
                        type="file" 
                        className="form-control"
                        name="profile_image" />
                    
                    <input 
                        type="submit" 
                        className="form-control"
                    />
                </div> 
            </form>
        </div>
   )
}
*/