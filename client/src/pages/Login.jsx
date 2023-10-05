import React, { useEffect } from 'react'
import { useState } from 'react';

export default function Login({setUser}) {

    

    const [formData, setFormData] = useState({
        username: '',
        password: '',
    });
    const [error,setError]=useState()

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const url = `http://127.0.0.1:8000/api/token/`;
            const response = await fetch(url, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json', 
              },
              body:JSON.stringify({...formData})
            });

            if (response.ok) {
                const data = await response.json()
                console.log(data)
                localStorage.setItem('user', data);
                setUser(data)
               
            } else {
                console.log("Error:", response.statusText);
                setError(response.statusText)
            }
        } catch (error) {
            console.error("Error:", error);
            setError(error)
        }
    };
    return (
        <>
            <h2 style={{ color: "white" }}>Login</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label style={{ color: 'white' }}>Username:</label>
                    <input
                        type="text"
                        name="username"
                        value={formData.username}
                        onChange={handleChange}
                    />
                </div>
                <div>
                    <label style={{ color: 'white' }}>Password:</label>
                    <input
                        type="password"
                        name="password"
                        value={formData.password}
                        onChange={handleChange}
                    />
                </div>
                <button type="submit">Login</button>
            </form>
            <span style={{color:"red"}}>{error}</span>
        </>

    )
}
