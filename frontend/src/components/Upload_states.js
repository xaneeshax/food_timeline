import React, {useState} from 'react'

const API = process.env.REACT_APP_API;

export const Upload = () => {

    const [user_id, setUserID] = useState('')
    const [location, setLocation] = useState('')
    const [review, setReview] = useState('')
    const [rating, setRating] = useState('')
    const [pic, setPic] = useState('')

    console.log(pic)

    const handleSubmit = async (e) => {
        e.preventDefault();

        const res = await fetch(`${API}/foodies`, {
            method: 'POST',
            headers: {
                "Content-Type" : "application/json"
            },
            body : JSON.stringify({
                user_id,
                location,
                review,
                rating,
                pic
            })
        })
    
        const data = await res.json();
        console.log(data)
    }

    return (
        <div className='col-md-4'>
            <form onSubmit={handleSubmit} className="card card-body"  encType="multipart/form-data">  
                <div className='form-group'>
                    <input 
                        type="text" 
                        onChange={e => setUserID(e.target.value)} 
                        className="form-control"
                        placeholder="Name"
                        
                    />

                    <input 
                        type="text" 
                        onChange={e => setLocation(e.target.value)} 
                        className="form-control"
                        placeholder="Location"
                    />

                    <input 
                        type="text" 
                        onChange={e => setReview(e.target.value)} 
                        className="form-control"
                        placeholder="Review" 
                    />

                    <input 
                        type="text" 
                        onChange={e => setRating(e.target.value)} 
                        className="form-control"
                        placeholder="Rating" 
                    />

                    <input 
                        type="file" 
                        name="file" 
                        onChange={e => setPic(e.target.files[0])}
                    />

                </div>
                <button className="btn btn-primary btn" > 
                    {'Create'}
                </button>

            </form>
        </div>
    )

}

const[image, setImage] = useState('')
    const [loading, setLoading] = useState(false)
    

    const uploadImage = async e => {
        const files = e.target.files
        const data = new FormData()
        data.append('file', files[0])
        data.append('upload_preset', 'food_pics')
        setLoading(true)
        const res = await fetch(
            "https://api.cloudinary.com/v1_1/aneeshasreerama/image/upload/c_fill,h_300,w_300",
            {
                method: "POST",
                body: data
            }
        )

        const file = await res.json()
        setImage(file.secure_url)
        setLoading(false)