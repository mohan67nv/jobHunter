import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Search, Filter, Briefcase, Star, TrendingUp, Clock } from 'lucide-react'
import { analyticsApi } from '../lib/api'
import { useJobs } from '../hooks/useJobs'
import { useAnalysis } from '../hooks/useAnalysis'
import { useStore } from '../store/useStore'
import JobCard from '../components/JobCard'
import JobDetailModal from '../components/JobDetailModal'
import StatsCard from '../components/StatsCard'

export default function Dashboard() {
  const [page, setPage] = useState(1)
  const [searchTerm, setSearchTerm] = useState('')
  const { filters, setFilters } = useStore()
  
  const { selectedJob, setSelectedJob, jobDetailModalOpen, setJobDetailModalOpen } = useStore()

  // Fetch stats
  const { data: stats } = useQuery({
    queryKey: ['stats'],
    queryFn: async () => {
      const response = await analyticsApi.getOverview()
      return response.data
    },
  })

  // Fetch jobs
  const { data: jobsData, isLoading } = useJobs(page, {
    ...filters,
    search: searchTerm || undefined,
  })

  // Fetch analysis for selected job
  const { data: analysis } = useAnalysis(selectedJob?.id || null)

  const handleJobClick = (job: any) => {
    setSelectedJob(job)
    setJobDetailModalOpen(true)
  }

  const handleCloseModal = () => {
    setJobDetailModalOpen(false)
    setTimeout(() => setSelectedJob(null), 300)
  }

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Job Dashboard</h1>
        <p className="text-gray-600 mt-1">Find your next opportunity with AI-powered insights</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatsCard
          title="Total Jobs"
          value={stats?.total_jobs || 0}
          icon={Briefcase}
          color="blue"
        />
        <StatsCard
          title="New Today"
          value={stats?.new_today || 0}
          icon={Clock}
          color="green"
        />
        <StatsCard
          title="High Match"
          value={stats?.high_match_jobs || 0}
          icon={Star}
          color="yellow"
        />
        <StatsCard
          title="Applications"
          value={stats?.total_applications || 0}
          icon={TrendingUp}
          color="purple"
        />
      </div>

      {/* Search and Filters */}
      <div className="bg-white rounded-lg border border-gray-200 p-4">
        <div className="flex flex-col md:flex-row gap-4">
          {/* Search */}
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search jobs, companies, or locations..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          {/* Filter Button */}
          <button className="flex items-center space-x-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
            <Filter className="h-5 w-5" />
            <span>Filters</span>
          </button>
        </div>

        {/* Quick Filters */}
        <div className="flex flex-wrap gap-2 mt-4">
          <button
            onClick={() => setFilters({ min_match_score: 80 })}
            className="px-3 py-1 bg-green-50 text-green-700 rounded-full text-sm hover:bg-green-100"
          >
            High Match (80%+)
          </button>
          <button
            onClick={() => setFilters({ posted_after: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0] })}
            className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-sm hover:bg-blue-100"
          >
            Last 7 Days
          </button>
          <button
            onClick={() => setFilters({})}
            className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm hover:bg-gray-200"
          >
            Clear Filters
          </button>
        </div>
      </div>

      {/* Job List */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold text-gray-900">
            {jobsData?.total || 0} Jobs Found
          </h2>
          <select className="px-4 py-2 border border-gray-300 rounded-lg">
            <option>Most Recent</option>
            <option>Best Match</option>
            <option>Highest Salary</option>
          </select>
        </div>

        {isLoading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            <p className="text-gray-600 mt-4">Loading jobs...</p>
          </div>
        ) : jobsData?.jobs && jobsData.jobs.length > 0 ? (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {jobsData.jobs.map((job: any) => (
              <JobCard
                key={job.id}
                job={job}
                onClick={() => handleJobClick(job)}
              />
            ))}
          </div>
        ) : (
          <div className="text-center py-12 bg-white rounded-lg border border-gray-200">
            <Briefcase className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600">No jobs found. Try adjusting your filters.</p>
          </div>
        )}

        {/* Pagination */}
        {jobsData && jobsData.total > 50 && (
          <div className="flex justify-center mt-8 space-x-2">
            <button
              onClick={() => setPage(Math.max(1, page - 1))}
              disabled={page === 1}
              className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50"
            >
              Previous
            </button>
            <span className="px-4 py-2">
              Page {page} of {Math.ceil(jobsData.total / 50)}
            </span>
            <button
              onClick={() => setPage(page + 1)}
              disabled={page >= Math.ceil(jobsData.total / 50)}
              className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50"
            >
              Next
            </button>
          </div>
        )}
      </div>

      {/* Job Detail Modal */}
      {selectedJob && (
        <JobDetailModal
          job={selectedJob}
          analysis={analysis}
          isOpen={jobDetailModalOpen}
          onClose={handleCloseModal}
        />
      )}
    </div>
  )
}
