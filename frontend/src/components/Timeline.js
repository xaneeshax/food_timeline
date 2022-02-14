import React, { useState } from 'react'
import Posts from "./Posts"

const API = process.env.REACT_APP_API;

export const Timeline = () => {

  // const [loading, setLoading] = useState(true)
  const [username, setUsername] = useState('')
  const [timeline, setTimeline] = useState([])

  const handleSubmit = async (e) => {
    
    e.preventDefault();

    const response = await fetch(`${API}/timeline/${username}`)
    const timeline_posts = await response.json()

    console.log(timeline_posts)
    setTimeline(timeline_posts)

    console.log('passed set timeline')

    setUsername("");
  }



    
  return (
    <main>
      <div className='col-md-4'>
        <form onSubmit={handleSubmit} className="card card-body">  
          <div className='form-group'>
            <input type="text" onChange={e => setUsername(e.target.value)} 
                value={username} className="form-control"
                placeholder="Username"
            />
          </div>
          <button className="btn btn-primary btn" > 
            {'Login'}
          </button>
        </form>
      </div>
      <Posts posts={timeline} />
    </main>
  )
    
}