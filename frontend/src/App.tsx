import { Routes, Route } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import Analytics from './pages/Analytics'
import Settings from './pages/Settings'
import CompareResume from './pages/CompareResume'
import ResumeManager from './pages/ResumeManager'
import Templates from './pages/Templates'
import Applications from './pages/Applications'
import InterviewPrep from './pages/InterviewPrep'
import Layout from './components/Layout'

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/analytics" element={<Analytics />} />
        <Route path="/compare" element={<CompareResume />} />
        <Route path="/resumes" element={<ResumeManager />} />
        <Route path="/templates" element={<Templates />} />
        <Route path="/applications" element={<Applications />} />
        <Route path="/interview-prep" element={<InterviewPrep />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Layout>
  )
}

export default App
