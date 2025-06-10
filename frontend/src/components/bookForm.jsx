// COMPONENTE PARA AGREGAR/EDITAR LIBROS
import { useState } from 'react'
import { booksAPI } from '../services/api.js'

function BookForm({ onCancel, onBookSaved, editingBook = null }) {
  // Estados para todos los campos del libro
  const [title, setTitle] = useState(editingBook?.title || '')
  const [author, setAuthor] = useState(editingBook?.author || '')
  const [pages, setPages] = useState(editingBook?.pages || '')
  const [seriesInspiration, setSeriesInspiration] = useState(editingBook?.series_inspiration || '')
  const [readingStatus, setReadingStatus] = useState(editingBook?.reading_status || 'pendiente')
  const [userComments, setUserComments] = useState(editingBook?.user_comments || '')
  
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  // Determinar si estamos editando o creando
  const isEditing = editingBook !== null
  const formTitle = isEditing ? 'Editar Libro' : 'Agregar Nuevo Libro'
  const buttonText = isEditing ? 'Actualizar Libro' : 'Agregar Libro'

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')

    try {
      // Preparar datos para enviar (exactamente como tu backend espera)
      const bookData = {
        title: title.trim(),
        author: author.trim(),
        pages: pages ? parseInt(pages) : null,
        series_inspiration: seriesInspiration.trim() || null,
        reading_status: readingStatus,
        user_comments: userComments.trim() || null,
      }

      console.log('📤 Enviando datos:', bookData)

      let savedBook
      if (isEditing) {
        // Actualizar libro existente
        savedBook = await booksAPI.update(editingBook.id, bookData)
        console.log('✅ Libro actualizado:', savedBook)
      } else {
        // Crear nuevo libro
        savedBook = await booksAPI.create(bookData)
        console.log('✅ Libro creado:', savedBook)
      }

      // Notificar al componente padre
      onBookSaved(savedBook)
      
      // Mensaje de éxito
      alert(isEditing ? '¡Libro actualizado correctamente!' : '¡Libro agregado correctamente!')

    } catch (err) {
      console.error('❌ Error:', err)
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div style={{ 
      maxWidth: '600px', 
      margin: '0 auto', 
      padding: '20px',
      backgroundColor: 'white',
      borderRadius: '8px',
      boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
    }}>
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        marginBottom: '30px'
      }}>
        <h2>{formTitle}</h2>
        <button 
          onClick={onCancel}
          style={{
            padding: '8px 16px',
            backgroundColor: '#6c757d',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          ✕ Cancelar
        </button>
      </div>

      <form onSubmit={handleSubmit}>
        <div style={{ display: 'grid', gap: '20px' }}>
          
          {/* Título del libro */}
          <div>
            <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '5px' }}>
              Título del libro *
            </label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
              placeholder="Ej: Cien años de soledad"
              style={{
                width: '100%',
                padding: '10px',
                border: '1px solid #ddd',
                borderRadius: '4px',
                fontSize: '16px'
              }}
            />
          </div>

          {/* Autor */}
          <div>
            <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '5px' }}>
              Autor *
            </label>
            <input
              type="text"
              value={author}
              onChange={(e) => setAuthor(e.target.value)}
              required
              placeholder="Ej: Gabriel García Márquez"
              style={{
                width: '100%',
                padding: '10px',
                border: '1px solid #ddd',
                borderRadius: '4px',
                fontSize: '16px'
              }}
            />
          </div>

          {/* Fila con campos opcionales */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px' }}>
            
            {/* Número de páginas */}
            <div>
              <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '5px' }}>
                Páginas
              </label>
              <input
                type="number"
                value={pages}
                onChange={(e) => setPages(e.target.value)}
                placeholder="Ej: 432"
                min="1"
                style={{
                  width: '100%',
                  padding: '10px',
                  border: '1px solid #ddd',
                  borderRadius: '4px',
                  fontSize: '16px'
                }}
              />
            </div>

            {/* Estado de lectura */}
            <div>
              <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '5px' }}>
                Estado de lectura
              </label>
              <select
                value={readingStatus}
                onChange={(e) => setReadingStatus(e.target.value)}
                style={{
                  width: '100%',
                  padding: '10px',
                  border: '1px solid #ddd',
                  borderRadius: '4px',
                  fontSize: '16px'
                }}
              >
                <option value="pendiente">📚 Pendiente</option>
                <option value="empezado">📖 Empezado</option>
                <option value="acabado">✅ Acabado</option>
              </select>
            </div>
          </div>

          {/* Serie de inspiración */}
          <div>
            <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '5px' }}>
              Serie que te inspiró a leerlo
            </label>
            <input
              type="text"
              value={seriesInspiration}
              onChange={(e) => setSeriesInspiration(e.target.value)}
              placeholder="Ej: Breaking Bad, Game of Thrones, Stranger Things..."
              style={{
                width: '100%',
                padding: '10px',
                border: '1px solid #ddd',
                borderRadius: '4px',
                fontSize: '16px'
              }}
            />
            <small style={{ color: '#666', fontSize: '14px' }}>
              🤖 ¡Perfecto para generar recomendaciones con IA más tarde!
            </small>
          </div>

          {/* Comentarios del usuario */}
          <div>
            <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '5px' }}>
              Tus comentarios
            </label>
            <textarea
              value={userComments}
              onChange={(e) => setUserComments(e.target.value)}
              placeholder="¿Qué te pareció? ¿Por qué lo agregaste? ¿Qué esperas de él?"
              rows="3"
              style={{
                width: '100%',
                padding: '10px',
                border: '1px solid #ddd',
                borderRadius: '4px',
                fontSize: '16px',
                resize: 'vertical'
              }}
            />
          </div>

        </div>

        {/* Mostrar error si existe */}
        {error && (
          <div style={{ 
            color: 'red', 
            marginTop: '15px',
            padding: '10px',
            border: '1px solid red',
            borderRadius: '4px',
            backgroundColor: '#ffeaea'
          }}>
            ❌ {error}
          </div>
        )}

        {/* Botones de acción */}
        <div style={{ 
          display: 'flex', 
          gap: '10px', 
          marginTop: '30px',
          justifyContent: 'flex-end'
        }}>
          <button
            type="button"
            onClick={onCancel}
            style={{
              padding: '12px 24px',
              backgroundColor: '#6c757d',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              fontSize: '16px'
            }}
          >
            Cancelar
          </button>
          
          <button
            type="submit"
            disabled={isLoading}
            style={{
              padding: '12px 24px',
              backgroundColor: isEditing ? '#ffc107' : '#28a745',
              color: isEditing ? '#212529' : 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: isLoading ? 'not-allowed' : 'pointer',
              fontSize: '16px'
            }}
          >
            {isLoading ? '⏳ Guardando...' : buttonText}
          </button>
        </div>

        {/* Nota sobre campos obligatorios */}
        <p style={{ 
          fontSize: '14px', 
          color: '#666', 
          marginTop: '15px',
          textAlign: 'center'
        }}>
          * Campos obligatorios
        </p>
      </form>
    </div>
  )
}

export default BookForm