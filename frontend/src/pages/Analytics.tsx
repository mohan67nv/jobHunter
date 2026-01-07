import { useQuery } from '@tanstack/react-query'
import { BarChart, Bar, PieChart, Pie, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts'
import { analyticsApi } from '../lib/api'
import { TrendingUp, Users, Target, Award, Download, FileSpreadsheet } from 'lucide-react'

export default function Analytics() {
  // Fetch analytics data
  const { data: overview } = useQuery({
    queryKey: ['analytics-overview'],
    queryFn: async () => {
      const response = await analyticsApi.getOverview()
      return response.data
    },
  })

  const { data: timeline } = useQuery({
    queryKey: ['applications-timeline'],
    queryFn: async () => {
      const response = await analyticsApi.getApplicationsTimeline(30)
      return response.data.timeline
    },
  })

  const { data: sourceData } = useQuery({
    queryKey: ['jobs-by-source'],
    queryFn: async () => {
      const response = await analyticsApi.getJobsBySource()
      return response.data.sources
    },
  })

  const { data: matchDistribution } = useQuery({
    queryKey: ['match-distribution'],
    queryFn: async () => {
      const response = await analyticsApi.getMatchScoreDistribution()
      return response.data.distribution
    },
  })

  const { data: topCompanies } = useQuery({
    queryKey: ['top-companies'],
    queryFn: async () => {
      const response = await analyticsApi.getTopCompanies(10)
      return response.data.companies
    },
  })

  const { data: funnel } = useQuery({
    queryKey: ['application-funnel'],
    queryFn: async () => {
      const response = await analyticsApi.getApplicationFunnel()
      return response.data.funnel
    },
  })

  const { data: skillsDemand } = useQuery({
    queryKey: ['skills-demand'],
    queryFn: async () => {
      const response = await analyticsApi.getSkillsDemand(20)
      return response.data.skills
    },
  })

  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#06b6d4', '#84cc16']

  const exportToCSV = (data: any[], filename: string) => {
    if (!data || data.length === 0) return

    const headers = Object.keys(data[0]).join(',')
    const rows = data.map(obj => Object.values(obj).join(','))
    const csv = [headers, ...rows].join('\n')
    
    const blob = new Blob([csv], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${filename}-${new Date().toISOString().split('T')[0]}.csv`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(url)
  }

  return (
    <div className="space-y-4 sm:space-y-6">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 sm:gap-4">
        <div className="flex-1 min-w-0">
          <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Analytics Dashboard
          </h1>
          <p className="text-gray-600 mt-2 text-lg">Track your job search progress and insights</p>
        </div>
        <button
          onClick={() => exportToCSV(
            [overview, ...timeline, ...sourceData, ...matchDistribution, ...funnel, ...topCompanies],
            'analytics-full-export'
          )}
          className="flex items-center space-x-2 px-6 py-3 bg-gradient-to-r from-green-600 to-emerald-600 text-white rounded-lg hover:from-green-700 hover:to-emerald-700 shadow-lg transition-all"
        >
          <FileSpreadsheet className="h-5 w-5" />
          <span>Export All Data</span>
        </button>
      </div>

      {/* Key Metrics - Enhanced */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-gradient-to-br from-blue-500 to-blue-600 text-white rounded-xl shadow-lg p-6 transform hover:scale-105 transition-transform">
          <div className="flex items-center justify-between mb-2">
            <TrendingUp className="h-10 w-10 opacity-80" />
            <span className="text-4xl font-bold">{overview?.total_jobs || 0}</span>
          </div>
          <p className="text-blue-100 font-medium">Total Jobs Scraped</p>
        </div>
        <div className="bg-gradient-to-br from-green-500 to-green-600 text-white rounded-xl shadow-lg p-6 transform hover:scale-105 transition-transform">
          <div className="flex items-center justify-between mb-2">
            <Users className="h-10 w-10 opacity-80" />
            <span className="text-4xl font-bold">{overview?.total_applications || 0}</span>
          </div>
          <p className="text-green-100 font-medium">Total Applications</p>
        </div>
        <div className="bg-gradient-to-br from-yellow-500 to-orange-500 text-white rounded-xl shadow-lg p-6 transform hover:scale-105 transition-transform">
          <div className="flex items-center justify-between mb-2">
            <Target className="h-10 w-10 opacity-80" />
            <span className="text-4xl font-bold">{overview?.high_match_jobs || 0}</span>
          </div>
          <p className="text-yellow-100 font-medium">High Match (80%+)</p>
        </div>
        <div className="bg-gradient-to-br from-purple-500 to-purple-600 text-white rounded-xl shadow-lg p-6 transform hover:scale-105 transition-transform">
          <div className="flex items-center justify-between mb-2">
            <Award className="h-10 w-10 opacity-80" />
            <span className="text-4xl font-bold">{overview?.active_applications || 0}</span>
          </div>
          <p className="text-purple-100 font-medium">Active Pipeline</p>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Applications Timeline */}
        <div className="bg-white rounded-xl border border-gray-200 shadow-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-bold text-gray-900">Applications Over Time</h3>
            <button
              onClick={() => exportToCSV(timeline || [], 'applications-timeline')}
              className="text-sm flex items-center space-x-1 text-blue-600 hover:text-blue-700"
            >
              <Download className="h-4 w-4" />
              <span>CSV</span>
            </button>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={timeline || []}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="date" stroke="#6b7280" />
              <YAxis stroke="#6b7280" />
              <Tooltip 
                contentStyle={{ backgroundColor: '#fff', border: '1px solid #e5e7eb', borderRadius: '8px' }}
              />
              <Legend />
              <Line type="monotone" dataKey="count" stroke="#3b82f6" strokeWidth={3} dot={{ fill: '#3b82f6', r: 4 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Jobs by Source */}
        <div className="bg-white rounded-xl border border-gray-200 shadow-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-bold text-gray-900">Jobs by Source</h3>
            <button
              onClick={() => exportToCSV(sourceData || [], 'jobs-by-source')}
              className="text-sm flex items-center space-x-1 text-blue-600 hover:text-blue-700"
            >
              <Download className="h-4 w-4" />
              <span>CSV</span>
            </button>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={sourceData || []}
                dataKey="count"
                nameKey="source"
                cx="50%"
                cy="50%"
                outerRadius={100}
                label={(entry) => `${entry.source}: ${entry.count}`}
              >
                {(sourceData || []).map((_: any, index: number) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip 
                contentStyle={{ backgroundColor: '#fff', border: '1px solid #e5e7eb', borderRadius: '8px' }}
              />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Match Score Distribution */}
        <div className="bg-white rounded-xl border border-gray-200 shadow-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-bold text-gray-900">Match Score Distribution</h3>
            <button
              onClick={() => exportToCSV(matchDistribution || [], 'match-distribution')}
              className="text-sm flex items-center space-x-1 text-blue-600 hover:text-blue-700"
            >
              <Download className="h-4 w-4" />
              <span>CSV</span>
            </button>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={matchDistribution || []}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="range" stroke="#6b7280" />
              <YAxis stroke="#6b7280" />
              <Tooltip 
                contentStyle={{ backgroundColor: '#fff', border: '1px solid #e5e7eb', borderRadius: '8px' }}
              />
              <Legend />
              <Bar dataKey="count" fill="#10b981" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Application Funnel */}
        <div className="bg-white rounded-xl border border-gray-200 shadow-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-bold text-gray-900">Application Funnel</h3>
            <button
              onClick={() => exportToCSV(funnel || [], 'application-funnel')}
              className="text-sm flex items-center space-x-1 text-blue-600 hover:text-blue-700"
            >
              <Download className="h-4 w-4" />
              <span>CSV</span>
            </button>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={funnel || []} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis type="number" stroke="#6b7280" />
              <YAxis dataKey="stage" type="category" width={120} stroke="#6b7280" />
              <Tooltip 
                contentStyle={{ backgroundColor: '#fff', border: '1px solid #e5e7eb', borderRadius: '8px' }}
              />
              <Bar dataKey="count" fill="#3b82f6" radius={[0, 8, 8, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Skills Demand */}
        {skillsDemand && skillsDemand.length > 0 && (
          <div className="bg-white rounded-xl border border-gray-200 shadow-lg p-6 lg:col-span-2">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-bold text-gray-900">Most In-Demand Skills</h3>
              <button
                onClick={() => exportToCSV(skillsDemand || [], 'skills-demand')}
                className="text-sm flex items-center space-x-1 text-blue-600 hover:text-blue-700"
              >
                <Download className="h-4 w-4" />
                <span>CSV</span>
              </button>
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={skillsDemand || []}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis dataKey="skill" stroke="#6b7280" angle={-45} textAnchor="end" height={100} />
                <YAxis stroke="#6b7280" />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#fff', border: '1px solid #e5e7eb', borderRadius: '8px' }}
                />
                <Legend />
                <Bar dataKey="count" fill="#8b5cf6" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>

      {/* Top Companies */}
      <div className="bg-white rounded-xl border border-gray-200 shadow-lg p-6">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-bold text-gray-900">Top Companies by Job Count</h3>
          <button
            onClick={() => exportToCSV(topCompanies || [], 'top-companies')}
            className="flex items-center space-x-2 px-4 py-2 bg-blue-50 text-blue-600 rounded-lg hover:bg-blue-100 transition-colors"
          >
            <Download className="h-4 w-4" />
            <span>Export CSV</span>
          </button>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead>
              <tr className="bg-gray-50">
                <th className="px-6 py-3 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">
                  Rank
                </th>
                <th className="px-6 py-3 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">
                  Company
                </th>
                <th className="px-6 py-3 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">
                  Job Count
                </th>
                <th className="px-6 py-3 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">
                  Progress
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {(topCompanies || []).map((company: any, index: number) => (
                <tr key={index} className="hover:bg-gray-50 transition-colors">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex items-center justify-center w-8 h-8 rounded-full font-bold text-sm ${
                      index === 0 ? 'bg-yellow-100 text-yellow-700' :
                      index === 1 ? 'bg-gray-100 text-gray-700' :
                      index === 2 ? 'bg-orange-100 text-orange-700' :
                      'bg-blue-50 text-blue-600'
                    }`}>
                      #{index + 1}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {company.company}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-bold text-blue-600">
                    {company.job_count}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap w-64">
                    <div className="w-full bg-gray-200 rounded-full h-3">
                      <div
                        className="bg-gradient-to-r from-blue-600 to-purple-600 h-3 rounded-full transition-all"
                        style={{ width: `${(company.job_count / (topCompanies?.[0]?.job_count || 1)) * 100}%` }}
                      />
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Success Rate Insights */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-gradient-to-br from-green-50 to-emerald-50 border-2 border-green-200 rounded-xl p-6">
          <div className="text-center">
            <div className="text-4xl font-bold text-green-600 mb-2">
              {overview?.total_applications > 0 
                ? ((overview?.active_applications / overview?.total_applications) * 100).toFixed(1) 
                : 0}%
            </div>
            <p className="text-sm font-medium text-gray-700">Application Success Rate</p>
            <p className="text-xs text-gray-600 mt-2">Active / Total Applied</p>
          </div>
        </div>

        <div className="bg-gradient-to-br from-blue-50 to-indigo-50 border-2 border-blue-200 rounded-xl p-6">
          <div className="text-center">
            <div className="text-4xl font-bold text-blue-600 mb-2">
              {overview?.total_jobs > 0 
                ? ((overview?.high_match_jobs / overview?.total_jobs) * 100).toFixed(1) 
                : 0}%
            </div>
            <p className="text-sm font-medium text-gray-700">High Match Rate</p>
            <p className="text-xs text-gray-600 mt-2">80%+ Match / Total Jobs</p>
          </div>
        </div>

        <div className="bg-gradient-to-br from-purple-50 to-pink-50 border-2 border-purple-200 rounded-xl p-6">
          <div className="text-center">
            <div className="text-4xl font-bold text-purple-600 mb-2">
              {overview?.new_today || 0}
            </div>
            <p className="text-sm font-medium text-gray-700">New Jobs Today</p>
            <p className="text-xs text-gray-600 mt-2">Freshly Scraped</p>
          </div>
        </div>
      </div>
    </div>
  )
}
