import { useEffect, useState } from 'react'
import './App.css'
import Home from './pages/Home'
import Login from './pages/Login'
import jwt_decode from "jwt-decode";

function App() {
  const [user, setUser] = useState(null)
  const getNewTokens = async (user) => {
    try {
      const url = "http://127.0.0.1:8000/api/token/refresh/";
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({"refresh":user.refresh})
      });

      if (response.ok) {
        const newTokens = await response.json()
        const newUser = { ...user,...newTokens }
        setUser(newUser)
        localStorage.setItem('user', JSON.stringify(newUser));

      } else {
        console.log("Error:", response.statusText);
      }
    } catch (error) {
      console.error("Error:", error);
    }
  }

  useEffect(() => {
    const data = localStorage.getItem('user')
    if (data) {
      setUser(JSON.parse(data))
      const user=  JSON.parse(data)
      const decodedToken = jwt_decode(user.access);

      const expirationDate = new Date(decodedToken.exp * 1000);
      const currentDate = new Date()
      const daysUntilExpiration = Math.ceil((expirationDate - currentDate) / (1000 * 60 * 60 * 24));
      console.log("daysUntilExpiration:" + daysUntilExpiration);
      if (daysUntilExpiration > 10) {
        console.log("NOT GET NEW TOKENS")
      } else {
        console.log("GET NEW TOKEN")
        getNewTokens(user)
      }



    } else {
      console.log("Not log in")
    }

  }, [])
  const logout = () => {
    setUser('')
    localStorage.clear('user')
  }
  if (user) {
    return (
      <Home logout={logout} token={user.access} user={user} />
    )
  } else {
    return (
      <Login setUser={setUser} />

    )
  }

}

export default App
