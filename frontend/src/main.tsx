import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import App from './App'
import ErrorBoundary from './components/ErrorBoundary'
import './index.css'

// Show loading message
const root = document.getElementById('root')
if (root) {
  root.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;height:100vh;font-family:system-ui;font-size:18px;color:#666;">Loading SmartJobHunter Pro...</div>'
}

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
})

// Add error listener
window.addEventListener('error', (e) => {
  console.error('💥 Global error:', e.error)
  const root = document.getElementById('root')
  if (root && !root.querySelector('.app-loaded')) {
    root.innerHTML = `<div style="padding:50px;font-family:system-ui;">
      <h1 style="color:#e11d48;margin-bottom:20px;">⚠️ Application Error</h1>
      <p style="color:#666;margin-bottom:10px;">${e.message}</p>
      <pre style="background:#f5f5f5;padding:15px;border-radius:8px;overflow:auto;font-size:12px;">${e.error?.stack || 'No stack trace'}</pre>
      <button onclick="location.reload()" style="margin-top:20px;padding:10px 20px;background:#3b82f6;color:white;border:none;border-radius:6px;cursor:pointer;font-size:14px;">Reload Page</button>
    </div>`
  }
})

try {
  ReactDOM.createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
      <ErrorBoundary>
        <QueryClientProvider client={queryClient}>
          <BrowserRouter>
            <div className="app-loaded">
              <App />
            </div>
          </BrowserRouter>
        </QueryClientProvider>
      </ErrorBoundary>
    </React.StrictMode>,
  )
  console.log('✅ React app rendered successfully')
} catch (error) {
  console.error('💥 Failed to render React app:', error)
  const root = document.getElementById('root')
  if (root) {
    root.innerHTML = `<div style="padding:50px;font-family:system-ui;">
      <h1 style="color:#e11d48;margin-bottom:20px;">⚠️ Failed to Initialize</h1>
      <p style="color:#666;margin-bottom:10px;">${error instanceof Error ? error.message : 'Unknown error'}</p>
      <pre style="background:#f5f5f5;padding:15px;border-radius:8px;overflow:auto;font-size:12px;">${error instanceof Error ? error.stack : JSON.stringify(error)}</pre>
      <button onclick="location.reload()" style="margin-top:20px;padding:10px 20px;background:#3b82f6;color:white;border:none;border-radius:6px;cursor:pointer;font-size:14px;">Reload Page</button>
    </div>`
  }
}
