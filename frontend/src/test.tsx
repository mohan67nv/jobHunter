import React from 'react'
import ReactDOM from 'react-dom/client'

// Ultra simple test - no routing, no complex components
const root = document.getElementById('root')

if (!root) {
  document.body.innerHTML = '<div style="padding:50px;font-family:Arial;"><h1 style="color:red;">ERROR: Root element not found!</h1></div>'
} else {
  try {
    ReactDOM.createRoot(root).render(
      <div style={{ padding: '50px', fontFamily: 'Arial' }}>
        <h1 style={{ color: 'green' }}>✅ React is Working!</h1>
        <p>If you see this, React is rendering correctly.</p>
        <p>The issue is with the main app components.</p>
        <button 
          onClick={() => window.location.href = '/'}
          style={{ padding: '10px 20px', fontSize: '16px', cursor: 'pointer' }}
        >
          Load Full App
        </button>
      </div>
    )
  } catch (error) {
    document.body.innerHTML = `<div style="padding:50px;font-family:Arial;">
      <h1 style="color:red;">React Error!</h1>
      <pre>${error.message}\n${error.stack}</pre>
    </div>`
  }
}
