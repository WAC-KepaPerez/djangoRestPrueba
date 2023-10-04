import { useEffect, useState } from 'react'
import './App.css'

function App() {
  const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk3NzEzNjA5LCJpYXQiOjE2OTY0MTc2MDksImp0aSI6ImY3ZDg3MDExMjg5MDQxMzZhYjVmNjExN2RmOTQ5NGRkIiwidXNlcl9pZCI6MX0.5aiY756CdOvO1gYcBVCDagQMMOYeFA6C3WiQ-_TH1n8"
  const [notas, setNotas] = useState([])
  const [value, setValue] = useState('')
  const [error, setError] = useState()


  useEffect(() => {
    const getData = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/api/notas/");
        if (response.ok) {
          const data = await response.json();
          console.log(data)// Await the JSON parsing
          data.sort((b, a) => new Date(a.created) - new Date(b.created));
          setNotas(data)
        } else {
          console.log("Error:", response.statusText);
        }
      } catch (error) {
        console.error("Error:", error);
      }
    };

    getData();
  }, [])
  const changeCheck = (id) => {

  }

  const deleteNote = async (id) => {
    try {
      const url = `http://127.0.0.1:8000/api/notas/${id}`;
      const response = await fetch(url, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        console.log("Note deleted successfully");
        const newNotes = notas.filter(nota => nota.id !== id)
        setNotas(newNotes)
        alert("Note deleted successfully")

      } else {
        console.log("Error:", response.statusText);
      }
    } catch (error) {
      console.error("Error:", error);
    }
  }
  const createNote = async () => {
    if (value) {

      try {
        const url = `http://127.0.0.1:8000/api/notas/add`;
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ value })
        });

        if (response.ok) {
          setError()
          setValue('')
          const data = await response.json(); // Await the JSON parsing
          setNotas(prev => [data, ...prev])

        } else {
          console.log("Error:", response.statusText);
          setError("Error:" + response.statusText)
        }
      } catch (error) {
        console.error("Error:", error);

      }
    } else {
      setError("Add text for the note")
    }

  }
  const updateState = async (nota) => {
    nota.done = "true"
    const id = nota.id
    try {
      const url = `http://127.0.0.1:8000/api/notas/${id}`;
      const response = await fetch(url, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(nota)
      });

      if (response.ok) {
        console.log("Note updated successfully");
        const newNotes = notas.map((nota) => {
          if (nota.id === id) {
            return { ...nota, done: true };
          }
          return nota
        })
        setNotas(newNotes)

      } else {
        console.log("Error:", response.statusText);
      }
    } catch (error) {
      console.error("Error:", error);
    }
  }

  return (
    <>
      <h1>Mis Notas</h1>
      <div>
        <input type='text' onChange={(e) => setValue(e.target.value)} value={value} />
        <div style={{ color: 'red' }}>{error}</div>
        <button onClick={createNote}>Create Neww</button>
      </div>
      <div className='notasCtn'>
        {notas && notas.map((nota) =>
          <div key={nota.id} className='notaCtn'>
            <div>
              <div className='notaTitle'>{nota.value}</div>
              <p className='notaFecha'>{nota.created}</p>
            </div>
            <div className='btnCtn'>
              {
                nota.done ? <span style={{ color: 'green', fontWeight: 'bold' }}>Done ✅</span>
                  :
                  <button onClick={() => updateState(nota)}>Done </button>
              }

              <button onClick={() => deleteNote(nota.id)}>Delete </button>
            </div>

          </div>
        )

        }
      </div>

    </>
  )
}

export default App
