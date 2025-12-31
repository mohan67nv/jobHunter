import { ReactNode } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { LayoutDashboard, BarChart3, Settings, Menu, Briefcase, GitCompare, FileText, Layers, CheckSquare, Sparkles } from 'lucide-react'
import { cn } from '../lib/utils'

interface LayoutProps {
  children: ReactNode
}

export default function Layout({ children }: LayoutProps) {
  const location = useLocation()

  const navItems = [
    { path: '/', label: 'Dashboard', icon: LayoutDashboard },
    { path: '/compare', label: 'Compare CV-JD', icon: GitCompare },
    { path: '/applications', label: 'Applications', icon: CheckSquare },
    { path: '/interview-prep', label: 'Interview Prep', icon: Sparkles },
    { path: '/resumes', label: 'Resume Versions', icon: FileText },
    { path: '/templates', label: 'Templates', icon: Layers },
    { path: '/analytics', label: 'Analytics', icon: BarChart3 },
    { path: '/settings', label: 'Settings', icon: Settings },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-purple-50">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md border-b border-gray-200 sticky top-0 z-50 shadow-sm">
        <div className="max-w-[1920px] mx-auto px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <Link to="/" className="flex items-center space-x-3 hover:opacity-80 transition">
              <div className="bg-gradient-to-br from-blue-600 to-purple-600 p-2 rounded-xl shadow-lg">
                <Briefcase className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  SmartJobHunter Pro
                </h1>
                <p className="text-xs text-gray-500">AI-Powered Job Search Platform</p>
              </div>
            </Link>

            {/* Navigation */}
            <nav className="hidden lg:flex items-center space-x-1">
              {navItems.map((item) => {
                const Icon = item.icon
                const isActive = location.pathname === item.path
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={cn(
                      'flex items-center space-x-2 px-4 py-2 rounded-lg transition-all',
                      isActive
                        ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-md'
                        : 'text-gray-600 hover:bg-white/50 hover:shadow-sm'
                    )}
                  >
                    <Icon className="h-4 w-4" />
                    <span className="font-medium text-sm">{item.label}</span>
                  </Link>
                )
              })}
            </nav>

            {/* Mobile menu button */}
            <button className="lg:hidden p-2 rounded-lg hover:bg-gray-100">
              <Menu className="h-6 w-6" />
            </button>
          </div>
        </div>
      </header>

      {/* Main content - Full width */}
      <main className="w-full min-h-[calc(100vh-4rem)]">
        <div className="max-w-[1920px] mx-auto px-6 lg:px-8 py-8">
          {children}
        </div>
      </main>
    </div>
  )
}
