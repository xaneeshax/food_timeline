export const Upload = () => {

    const [image, setImage] = useState('')
    const [loading, setLoading] = useState(false)

    const uploadImage = async e => {
        const files = e.target.files
        console.log(files[0])
        console.log(files[0].name)
        const data = new FormData()
        data.append('file', files[0])
        console.log(data)
        data.append('upload_preset', 'darwin')

        //console.log(files)
        // console.log(data)
        
        setLoading(true)
        const res = await fetch(
            'https://api.cloudinary.com/v1_1/dihifeicm/image/upload',
            {
                method: 'POST',
                body: data
            }
        )
        const file = await res.json()

        setImage(file.secure_url)
        setLoading(false)
    }

    return (
        <div className="App">
            <h1>Upload Image</h1>
            <input
                type="file"
                name="file"
                placeholder="Upload an image"
                onChange={uploadImage}
            />
            {loading ? (
                <h3>Loading...</h3>
            ) : (
                <img src={image} style={{ width: '300px' }} alt="pic" />
            )}
        </div>
    )
}