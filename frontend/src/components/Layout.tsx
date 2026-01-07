import { ReactNode } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { LayoutDashboard, BarChart3, Settings, Menu, Briefcase, GitCompare, FileText, Layers, CheckSquare, Sparkles, Target } from 'lucide-react'
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
    { path: '/manual-prep', label: 'Manual Prep', icon: Target },
    { path: '/resumes', label: 'Resume Versions', icon: FileText },
    { path: '/analytics', label: 'Analytics', icon: BarChart3 },
    { path: '/settings', label: 'Profile', icon: Settings },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-purple-50">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md border-b border-gray-200 sticky top-0 z-50 shadow-sm">
        <div className="w-full max-w-[1920px] mx-auto px-3 sm:px-4 lg:px-6 xl:px-8">
          <div className="flex justify-between items-center h-14 sm:h-16 gap-2 sm:gap-4">
            {/* Logo - Compact */}
            <Link to="/" className="flex items-center space-x-2 hover:opacity-80 transition flex-shrink-0">
              <div className="bg-gradient-to-br from-blue-600 to-purple-600 p-1.5 sm:p-2 rounded-lg sm:rounded-xl shadow-lg">
                <Briefcase className="h-4 w-4 sm:h-5 sm:w-5 lg:h-6 lg:w-6 text-white" />
              </div>
              <div className="hidden sm:block">
                <h1 className="text-sm sm:text-base lg:text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent whitespace-nowrap">
                  SmartJobHunter Pro
                </h1>
                <p className="text-[10px] sm:text-xs text-gray-500 whitespace-nowrap">AI-Powered Job Search</p>
              </div>
              <div className="block sm:hidden">
                <h1 className="text-sm font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  SJH Pro
                </h1>
              </div>
            </Link>

            {/* Navigation - Responsive */}
            <nav className="hidden lg:flex items-center space-x-1 xl:space-x-2 flex-shrink-0">
              {navItems.map((item) => {
                const Icon = item.icon
                const isActive = location.pathname === item.path
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={cn(
                      'flex items-center space-x-1.5 xl:space-x-2 px-2 xl:px-3 py-2 rounded-lg transition-all whitespace-nowrap',
                      isActive
                        ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-md'
                        : 'text-gray-600 hover:bg-white/50 hover:shadow-sm'
                    )}
                  >
                    <Icon className="h-3.5 w-3.5 xl:h-4 xl:w-4 flex-shrink-0" />
                    <span className="font-medium text-xs xl:text-sm">{item.label}</span>
                  </Link>
                )
              })}
            </nav>

            {/* Mobile menu button */}
            <button className="lg:hidden p-2 rounded-lg hover:bg-gray-100 flex-shrink-0">
              <Menu className="h-5 w-5 sm:h-6 sm:w-6" />
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
