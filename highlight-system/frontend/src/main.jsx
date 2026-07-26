import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { Toaster } from 'react-hot-toast'
import './index.css'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
    <Toaster
      position="top-right"
      toastOptions={{
        duration: 3000,
        style: {
          background: '#16171f',
          color: '#fff',
          border: '1px solid #2a2b35',
          fontSize: '13px',
        },
        success: {
          iconTheme: { primary: '#4ade80', secondary: '#16171f' },
        },
        error: {
          iconTheme: { primary: '#f87171', secondary: '#16171f' },
        },
      }}
    />
  </StrictMode>,
)