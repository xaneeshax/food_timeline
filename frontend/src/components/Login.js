import React, { useContext, useState } from 'react'

const API = process.env.REACT_APP_API;

export const Login = () => {
    
    // const {store, actions} = useContext(Context);
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const token = sessionStorage.getItem("token");

    const handleClick = () => {
        const opts = {
            method: 'POST',
            headers: {
                "Content-Type" : "application/json"
            },
            body: JSON.stringify({
                "email" : email,
                "password" : password
            })
        }

        fetch(`${API}/token`, opts)
        .then(resp => {
            if(resp.status === 200) return resp.json();
            else alert("There has been an error")
        })
        .then(data => {
            sessionStorage.setItem("token", data.access_token);
        })
        .catch(error => {
            console.error("Error: ", error)
        })

    }

    return (
        <div>
            <h1>Login Page</h1>
            {token && token !== "" && token !== undefined ? (
                "You are Logged In"
            ) : (
                <div>
                    <input 
                        type="text" 
                        placeholder="email" 
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                    <input 
                        type="password" 
                        placeholder="password"
                        value={password} 
                        onChange={(e) => setPassword(e.target.value)}
                    />
                    <button onClick={handleClick}>Login</button> 
                </div>
            )}  
        </div>
    )
        
}