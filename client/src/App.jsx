import { useEffect, useState } from 'react'
import './App.css'
import Home from './pages/Home'
import Login from './pages/Login'
function App() {
  const [user, setUser] = useState(null)
  useEffect(() => {
    const user = localStorage.getItem('user')
    setUser(user)
  }, [])
  const logout=()=>{
      setUser('')
      localStorage.clear('user')
  }
  if (user) {
    return (
      <Home logout={logout} token={user.access}/>
    )
  } else {
    return (
      <Login setUser={setUser}/>

    )
  }

}

export default App
