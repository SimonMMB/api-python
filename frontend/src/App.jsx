// 🏠 APLICACIÓN PRINCIPAL - Solo maneja la navegación
import { useState, useEffect } from 'react'
import Login from './components/Login.jsx'
import Register from './components/Register.jsx'
import Dashboard from './components/Dashboard.jsx'
import './App.css'

function App() {
  const [user, setUser] = useState(null)
  const [isLoading, setIsLoading] = useState(true)
  const [showRegister, setShowRegister] = useState(false)

  // Al cargar la app, verificar si hay un usuario logueado
  useEffect(() => {
    const savedUser = localStorage.getItem('user')
    if (savedUser) {
      try {
        setUser(JSON.parse(savedUser))
      } catch (err) {
        // Si hay error parseando, limpiar localStorage
        localStorage.removeItem('user')
        localStorage.removeItem('token')
      }
    }
    setIsLoading(false)
  }, [])

  // Función para manejar el login exitoso
  const handleLoginSuccess = (userData) => {
    setUser(userData)
    setShowRegister(false) // Asegurar que estamos en modo login
  }

  // Función para cerrar sesión
  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setUser(null)
    setShowRegister(false)
  }

  // Función para cambiar entre login y registro
  const handleShowRegister = () => {
    setShowRegister(true)
  }

  const handleBackToLogin = () => {
    setShowRegister(false)
  }

  const handleRegisterSuccess = () => {
    setShowRegister(false) // Volver al login después del registro
  }

  // Mostrar pantalla de carga mientras verificamos la sesión
  if (isLoading) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '100vh',
        fontSize: '18px'
      }}>
        Cargando...
      </div>
    )
  }

  // Si hay usuario logueado, mostrar Dashboard
  if (user) {
    return <Dashboard user={user} onLogout={handleLogout} />
  }

  // Si no hay usuario logueado, mostrar Login o Register
  if (showRegister) {
    return (
      <Register 
        onBack={handleBackToLogin}
        onRegisterSuccess={handleRegisterSuccess}
      />
    )
  }

  return (
    <Login 
      onLoginSuccess={handleLoginSuccess} 
      onShowRegister={handleShowRegister}
    />
  )
}

export default App