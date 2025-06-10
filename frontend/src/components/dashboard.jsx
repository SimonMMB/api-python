// COMPONENTE DEL DASHBOARD
import { useState, useEffect } from 'react'
import { booksAPI } from '../services/api.js'
import BookForm from './BookForm.jsx'  // ¡Descomentado!

function Dashboard({ user, onLogout }) {
  const [books, setBooks] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [showBookForm, setShowBookForm] = useState(false)
  const [editingBook, setEditingBook] = useState(null)

  // Cargar libros cuando el componente se monta
  useEffect(() => {
    loadBooks()
  }, [])

  const loadBooks = async () => {
    try {
      // AQUI SE CONECTA CON LA API
      const data = await booksAPI.getAll()
      setBooks(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  // Funciones para manejar el formulario
  const handleAddBook = () => {
    setEditingBook(null) // No estamos editando
    setShowBookForm(true) // Mostrar formulario
  }

  const handleEditBook = (book) => {
    setEditingBook(book) // Pasamos el libro a editar
    setShowBookForm(true) // Mostrar formulario
  }

  const handleDeleteBook = async (bookId) => {
    if (window.confirm('¿Estás seguro de que quieres eliminar este libro?')) {
      try {
        await booksAPI.delete(bookId)
        // Actualizar la lista quitando el libro eliminado
        setBooks(books.filter(book => book.id !== bookId))
        alert('Libro eliminado correctamente!')
      } catch (err) {
        setError('Error al eliminar libro: ' + err.message)
      }
    }
  }

  const handleBookSaved = (savedBook) => {
    if (editingBook) {
      // Editando: actualizar libro en la lista
      setBooks(books.map(book => 
        book.id === savedBook.id ? savedBook : book
      ))
    } else {
      // Nuevo: agregar a la lista
      setBooks([...books, savedBook])
    }
    
    // Cerrar formulario
    setShowBookForm(false)
    setEditingBook(null)
  }

  const handleCancelForm = () => {
    setShowBookForm(false)
    setEditingBook(null)
  }

  // Si estamos mostrando el formulario
  if (showBookForm) {
    return (
      <BookForm 
        onCancel={handleCancelForm}
        onBookSaved={handleBookSaved}
        editingBook={editingBook}
      />
    )
  }

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
      {/* Header con información del usuario */}
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        marginBottom: '30px'
      }}>
        <h1>📚 Mi Biblioteca</h1>
        <div>
          <span>Hola, {user.username}! </span>
          <button 
            onClick={onLogout} 
            style={{ 
              marginLeft: '10px',
              padding: '8px 16px',
              backgroundColor: '#dc3545',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            Cerrar Sesión
          </button>
        </div>
      </div>

      {/* Mostrar error si existe */}
      {error && (
        <div style={{ 
          color: 'red', 
          marginBottom: '20px',
          padding: '10px',
          border: '1px solid red',
          borderRadius: '4px',
          backgroundColor: '#ffeaea'
        }}>
          {error}
          <button 
            onClick={() => setError('')}
            style={{ marginLeft: '10px', background: 'none', border: 'none', color: 'red', cursor: 'pointer' }}
          >
            ✕
          </button>
        </div>
      )}

      {/* Contenido principal */}
      {isLoading ? (
        <div style={{ textAlign: 'center', padding: '50px' }}>
          <p>Cargando libros...</p>
        </div>
      ) : (
        <div>
          <div style={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center',
            marginBottom: '20px'
          }}>
            <h2>Mis Libros ({books.length})</h2>
            <button 
              onClick={handleAddBook}
              style={{ 
                padding: '10px 20px', 
                backgroundColor: '#28a745', 
                color: 'white', 
                border: 'none', 
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              + Agregar Libro
            </button>
          </div>

          {books.length === 0 ? (
            // Mensaje cuando no hay libros
            <div style={{ 
              textAlign: 'center', 
              padding: '40px',
              border: '2px dashed #ddd',
              borderRadius: '8px',
              backgroundColor: '#f9f9f9'
            }}>
              <h3>¡Tu biblioteca está vacía!</h3>
              <p>Agrega tu primer libro para comenzar a recibir recomendaciones.</p>
              <button 
                onClick={handleAddBook}
                style={{ 
                  padding: '12px 24px', 
                  backgroundColor: '#28a745', 
                  color: 'white', 
                  border: 'none', 
                  borderRadius: '4px',
                  cursor: 'pointer',
                  fontSize: '16px'
                }}
              >
                📖 Agregar mi primer libro
              </button>
            </div>
          ) : (
            // Lista de libros
            <div style={{ display: 'grid', gap: '15px' }}>
              {books.map((book) => (
                <div 
                  key={book.id} 
                  style={{ 
                    border: '1px solid #ddd', 
                    padding: '20px', 
                    borderRadius: '8px',
                    backgroundColor: 'white',
                    boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                    <div style={{ flex: 1 }}>
                      <h3 style={{ margin: '0 0 10px 0', color: '#333' }}>
                        {book.title}
                      </h3>
                      <p style={{ margin: '5px 0', color: '#666' }}>
                        <strong>Autor:</strong> {book.author}
                      </p>
                      {book.pages && (
                        <p style={{ margin: '5px 0', color: '#666' }}>
                          <strong>Páginas:</strong> {book.pages}
                        </p>
                      )}
                      <p style={{ margin: '5px 0', color: '#666' }}>
                        <strong>Estado:</strong> 
                        <span style={{ 
                          marginLeft: '8px',
                          padding: '2px 8px',
                          borderRadius: '12px',
                          backgroundColor: 
                            book.reading_status === 'acabado' ? '#d4edda' :
                            book.reading_status === 'empezado' ? '#fff3cd' : '#f8d7da',
                          color:
                            book.reading_status === 'acabado' ? '#155724' :
                            book.reading_status === 'empezado' ? '#856404' : '#721c24'
                        }}>
                          {book.reading_status === 'pendiente' ? '📚 Pendiente' :
                           book.reading_status === 'empezado' ? '📖 Empezado' : '✅ Acabado'}
                        </span>
                      </p>
                      {book.series_inspiration && (
                        <p style={{ margin: '5px 0', color: '#666' }}>
                          <strong>Inspirado por:</strong> {book.series_inspiration}
                        </p>
                      )}
                      {book.user_comments && (
                        <p style={{ margin: '10px 0 0 0', fontStyle: 'italic', color: '#555' }}>
                          "{book.user_comments}"
                        </p>
                      )}
                    </div>
                    
                    <div style={{ marginLeft: '20px' }}>
                      <button 
                        onClick={() => handleEditBook(book)}
                        style={{
                          padding: '8px 16px',
                          backgroundColor: '#ffc107',
                          color: '#212529',
                          border: 'none',
                          borderRadius: '4px',
                          cursor: 'pointer',
                          marginBottom: '8px',
                          display: 'block',
                          width: '100%'
                        }}
                      >
                        ✏️ Editar
                      </button>
                      
                      <button 
                        onClick={() => handleDeleteBook(book.id)}
                        style={{
                          padding: '8px 16px',
                          backgroundColor: '#dc3545',
                          color: 'white',
                          border: 'none',
                          borderRadius: '4px',
                          cursor: 'pointer',
                          display: 'block',
                          width: '100%'
                        }}
                      >
                        🗑️ Eliminar
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default Dashboard