import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { CheckSquare, Calendar, FileText, TrendingUp, Filter, Search } from 'lucide-react'
import { applicationsApi } from '../lib/api'
import { getStatusColor, getStatusLabel, formatDate } from '../lib/utils'

export default function Applications() {
  const [statusFilter, setStatusFilter] = useState<string>('all')
  const [searchTerm, setSearchTerm] = useState('')

  const { data: applications, isLoading } = useQuery({
    queryKey: ['applications', statusFilter],
    queryFn: async () => {
      const response = await applicationsApi.list(statusFilter === 'all' ? undefined : statusFilter)
      return response.data
    },
  })

  const { data: stats } = useQuery({
    queryKey: ['application-stats'],
    queryFn: async () => {
      const response = await applicationsApi.getStats()
      return response.data
    },
  })

  const statuses = [
    { value: 'all', label: 'All Applications', color: 'gray' },
    { value: 'saved', label: 'Saved', color: 'gray' },
    { value: 'applied', label: 'Applied', color: 'blue' },
    { value: 'phone_screen', label: 'Phone Screen', color: 'purple' },
    { value: 'interview', label: 'Interview', color: 'indigo' },
    { value: 'technical', label: 'Technical', color: 'cyan' },
    { value: 'offer', label: 'Offer', color: 'green' },
    { value: 'rejected', label: 'Rejected', color: 'red' },
  ]

  return (
    <div className="min-h-screen">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 flex items-center gap-3">
          <CheckSquare className="h-10 w-10 text-green-600" />
          Application Tracker
        </h1>
        <p className="text-gray-600 mt-2 text-lg">
          Track your job applications through the entire process
        </p>
      </div>

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-xl shadow-lg p-6 border-l-4 border-blue-600">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Total Applications</p>
              <p className="text-3xl font-bold text-gray-900">{stats?.total_applications || 0}</p>
            </div>
            <FileText className="h-12 w-12 text-blue-600 opacity-20" />
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6 border-l-4 border-purple-600">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Active</p>
              <p className="text-3xl font-bold text-gray-900">{stats?.status_counts?.applied || 0}</p>
            </div>
            <TrendingUp className="h-12 w-12 text-purple-600 opacity-20" />
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6 border-l-4 border-indigo-600">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Interviews</p>
              <p className="text-3xl font-bold text-gray-900">
                {(stats?.status_counts?.interview || 0) + (stats?.status_counts?.technical || 0)}
              </p>
            </div>
            <Calendar className="h-12 w-12 text-indigo-600 opacity-20" />
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6 border-l-4 border-green-600">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Offers</p>
              <p className="text-3xl font-bold text-gray-900">{stats?.status_counts?.offer || 0}</p>
            </div>
            <CheckSquare className="h-12 w-12 text-green-600 opacity-20" />
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
        <div className="flex flex-col md:flex-row gap-4">
          {/* Search */}
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search by company or position..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
            />
          </div>

          {/* Status Filter */}
          <div className="flex gap-2 overflow-x-auto">
            {statuses.map((status) => (
              <button
                key={status.value}
                onClick={() => setStatusFilter(status.value)}
                className={`px-4 py-2 rounded-lg text-sm font-medium whitespace-nowrap transition ${
                  statusFilter === status.value
                    ? 'bg-green-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {status.label}
                {status.value !== 'all' && stats?.status_counts?.[status.value] && (
                  <span className="ml-2 px-2 py-0.5 bg-white/20 rounded-full text-xs">
                    {stats.status_counts[status.value]}
                  </span>
                )}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Applications List */}
      {isLoading ? (
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mb-4"></div>
          <p className="text-gray-600">Loading applications...</p>
        </div>
      ) : applications && applications.length > 0 ? (
        <div className="bg-white rounded-xl shadow-lg overflow-hidden">
          <table className="w-full">
            <thead className="bg-gradient-to-r from-green-50 to-blue-50 border-b border-gray-200">
              <tr>
                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase">Position</th>
                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase">Company</th>
                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase">Status</th>
                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase">Applied</th>
                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase">Interview</th>
                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {applications.map((app: any) => (
                <tr key={app.id} className="hover:bg-gray-50 transition">
                  <td className="px-6 py-4">
                    <div className="font-medium text-gray-900">{app.job?.title || 'N/A'}</div>
                  </td>
                  <td className="px-6 py-4 text-gray-700">{app.job?.company || 'N/A'}</td>
                  <td className="px-6 py-4">
                    <span className={`px-3 py-1 text-xs font-semibold rounded-full ${getStatusColor(app.status)}`}>
                      {getStatusLabel(app.status)}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-600">
                    {app.applied_date ? formatDate(app.applied_date) : '-'}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-600">
                    {app.interview_date ? formatDate(app.interview_date) : '-'}
                  </td>
                  <td className="px-6 py-4">
                    <button className="px-4 py-2 text-sm bg-green-600 text-white rounded-lg hover:bg-green-700">
                      Update
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="bg-white rounded-xl shadow-lg p-12 text-center">
          <CheckSquare className="h-16 w-16 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">No Applications Yet</h3>
          <p className="text-gray-600 mb-6">Start applying to jobs from the Dashboard</p>
        </div>
      )}

      {/* Upcoming Interviews */}
      {stats?.upcoming_interviews && stats.upcoming_interviews.length > 0 && (
        <div className="mt-8 bg-gradient-to-r from-indigo-50 to-purple-50 rounded-xl p-6 border border-indigo-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <Calendar className="h-5 w-5 text-indigo-600" />
            Upcoming Interviews
          </h3>
          <div className="space-y-3">
            {stats.upcoming_interviews.map((interview: any) => (
              <div key={interview.id} className="bg-white rounded-lg p-4 shadow-sm">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-semibold text-gray-900">{interview.job?.company}</p>
                    <p className="text-sm text-gray-600">{interview.job?.title}</p>
                  </div>
                  <div className="text-right">
                    <p className="font-semibold text-indigo-600">{formatDate(interview.interview_date)}</p>
                    <p className="text-sm text-gray-600">{interview.interview_type}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
