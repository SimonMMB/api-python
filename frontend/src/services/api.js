// ARCHIVO DE CONEXION CON LA API
// Aqui estan TODAS las funciones que hablan con tu FastAPI

const API_BASE_URL = 'http://localhost:8000'

// Funcion auxiliar para hacer peticiones con token
const fetchWithAuth = async (url, options = {}) => {
  const token = localStorage.getItem('token')
  
  return fetch(`${API_BASE_URL}${url}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': token ? `Bearer ${token}` : '',
      ...options.headers,
    },
  })
}

// FUNCIONES DE AUTENTICACION
export const authAPI = {
  // Registrar nuevo usuario
  register: async (username, email, password) => {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, email, password }),
    })
    
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Error al registrar usuario')
    }
    
    return response.json()
  },

  // Iniciar sesion (usa username, no email)
  login: async (username, password) => {
    // Tu backend usa OAuth2PasswordRequestForm, que requiere form-data
    const formData = new FormData()
    formData.append('username', username)
    formData.append('password', password)

    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      body: formData, // No JSON, sino form-data
    })
    
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Credenciales incorrectas')
    }
    
    return response.json()
  }
}

// FUNCIONES DE LIBROS
export const booksAPI = {
  // Obtener todos los libros del usuario
  getAll: async () => {
    const response = await fetchWithAuth('/books/')
    
    if (!response.ok) {
      throw new Error('Error al cargar libros')
    }
    
    return response.json()
  },

  // Crear un nuevo libro
  create: async (bookData) => {
    const response = await fetchWithAuth('/books/', {
      method: 'POST',
      body: JSON.stringify(bookData),
    })
    
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Error al crear libro')
    }
    
    return response.json()
  },

  // Obtener un libro especifico
  getById: async (id) => {
    const response = await fetchWithAuth(`/books/${id}`)
    
    if (!response.ok) {
      throw new Error('Error al cargar libro')
    }
    
    return response.json()
  },

  // Actualizar un libro
  update: async (id, bookData) => {
    const response = await fetchWithAuth(`/books/${id}`, {
      method: 'PUT',
      body: JSON.stringify(bookData),
    })
    
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Error al actualizar libro')
    }
    
    return response.json()
  },

  // Eliminar un libro
  delete: async (id) => {
    const response = await fetchWithAuth(`/books/${id}`, {
      method: 'DELETE',
    })
    
    if (!response.ok) {
      throw new Error('Error al eliminar libro')
    }
    
    return response.json()
  },

  // Obtener recomendaciones para un libro
  getRecommendations: async (id) => {
    const response = await fetchWithAuth(`/books/${id}/recommend`, {
      method: 'POST',
    })
    
    if (!response.ok) {
      throw new Error('Error al obtener recomendaciones')
    }
    
    return response.json()
  }
}

// FUNCIONES DE IA - RECOMENDACIONES
export const aiAPI = {
  // Obtener recomendaciones basadas en series
  getRecommendations: async (seriesName, maxBooks = 5, userPreferences = null) => {
    const response = await fetchWithAuth('/ai/recommend-books', {
      method: 'POST',
      body: JSON.stringify({
        series_name: seriesName,
        max_books: maxBooks,
        user_preferences: userPreferences,
      }),
    })
    
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Error al obtener recomendaciones')
    }
    
    return response.json()
  },

  // Analizar una serie especifica
  analyzeSeries: async (seriesName) => {
    const response = await fetchWithAuth('/ai/analyze-series', {
      method: 'POST',
      body: JSON.stringify({
        series_name: seriesName,
      }),
    })
    
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Error al analizar serie')
    }
    
    return response.json()
  },

  // Guardar una recomendacion como libro personal
  saveRecommendation: async (recommendedBook) => {
    const response = await fetchWithAuth('/ai/save-recommendation', {
      method: 'POST',
      body: JSON.stringify(recommendedBook),
    })
    
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Error al guardar recomendacion')
    }
    
    return response.json()
  },

  // Obtener series soportadas
  getSupportedSeries: async () => {
    const response = await fetchWithAuth('/ai/supported-series')
    
    if (!response.ok) {
      throw new Error('Error al cargar series soportadas')
    }
    
    return response.json()
  }
}