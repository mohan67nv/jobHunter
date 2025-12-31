import { useState } from 'react'
import { useQuery, useMutation } from '@tanstack/react-query'
import { Search, Filter, Briefcase, Star, TrendingUp, Clock, Play, Loader2, X, ChevronDown } from 'lucide-react'
import { analyticsApi, scrapersApi } from '../lib/api'
import { useJobs } from '../hooks/useJobs'
import { useAnalysis } from '../hooks/useAnalysis'
import { useStore } from '../store/useStore'
import JobCard from '../components/JobCard'
import JobDetailModal from '../components/JobDetailModal'
import StatsCard from '../components/StatsCard'

// Top 10 job sources
const JOB_SOURCES = [
  { value: 'all', label: 'All Sources' },
  { value: 'LinkedIn', label: 'LinkedIn' },
  { value: 'Indeed', label: 'Indeed' },
  { value: 'StepStone', label: 'StepStone' },
  { value: 'Glassdoor', label: 'Glassdoor' },
  { value: 'Monster', label: 'Monster' },
  { value: 'Xing', label: 'Xing' },
  { value: 'Arbeitsagentur', label: 'Arbeitsagentur' },
  { value: 'CareerBuilder', label: 'CareerBuilder' },
  { value: 'ZipRecruiter', label: 'ZipRecruiter' },
  { value: 'SimplyHired', label: 'SimplyHired' },
]

const JOB_TYPES = [
  { value: 'all', label: 'All Types' },
  { value: 'full-time', label: 'Full-time' },
  { value: 'part-time', label: 'Part-time' },
  { value: 'contract', label: 'Contract' },
  { value: 'freelance', label: 'Freelance' },
  { value: 'internship', label: 'Internship' },
]

const REMOTE_TYPES = [
  { value: 'all', label: 'All Locations' },
  { value: 'remote', label: 'Remote' },
  { value: 'hybrid', label: 'Hybrid' },
  { value: 'on-site', label: 'On-site' },
]

const EXPERIENCE_LEVELS = [
  { value: 'all', label: 'All Levels' },
  { value: 'entry', label: 'Entry Level' },
  { value: 'mid', label: 'Mid Level' },
  { value: 'senior', label: 'Senior' },
  { value: 'lead', label: 'Lead' },
]

const DATE_RANGES = [
  { value: 'all', label: 'Any Time' },
  { value: '1', label: 'Last 24 Hours' },
  { value: '7', label: 'Last 7 Days' },
  { value: '14', label: 'Last 14 Days' },
  { value: '30', label: 'Last 30 Days' },
]

export default function Dashboard() {
  const [page, setPage] = useState(1)
  const [searchTerm, setSearchTerm] = useState('')
  const [showFilters, setShowFilters] = useState(false)
  const [scrapeKeyword, setScrapeKeyword] = useState('')
  const [scrapeLocation, setScrapeLocation] = useState('Germany')
  const [isScrapingOpen, setIsScrapingOpen] = useState(false)
  const [scrapeStatus, setScrapeStatus] = useState<{ running: boolean; message: string } | null>(null)
  
  const { filters, setFilters, removeFilter } = useStore()
  
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
  const { data: jobsData, isLoading, refetch } = useJobs(page, {
    ...filters,
    search: searchTerm || undefined,
  })

  // Fetch analysis for selected job
  const { data: analysis } = useAnalysis(selectedJob?.id || null)

  // Scrape mutation
  const scrapeMutation = useMutation({
    mutationFn: async () => {
      const response = await scrapersApi.scrape(scrapeKeyword, scrapeLocation)
      return response.data
    },
    onSuccess: (data) => {
      setScrapeStatus({ running: true, message: `Scraping started: ${data.keyword} in ${data.location}` })
      setTimeout(() => {
        setScrapeStatus(null)
        refetch()
      }, 5000)
    },
    onError: () => {
      setScrapeStatus({ running: false, message: 'Failed to start scraping' })
    }
  })

  const handleStartScrape = () => {
    if (scrapeKeyword.trim()) {
      scrapeMutation.mutate()
      setIsScrapingOpen(false)
    }
  }

  const handleJobClick = (job: any) => {
    setSelectedJob(job)
    setJobDetailModalOpen(true)
  }

  const handleCloseModal = () => {
    setJobDetailModalOpen(false)
    setTimeout(() => setSelectedJob(null), 300)
  }

  // Filter handlers
  const applyFilter = (key: string, value: string) => {
    if (value === 'all') {
      const newFilters = { ...filters }
      delete newFilters[key]
      setFilters(newFilters)
    } else if (key === 'posted_after' && value !== 'all') {
      const days = parseInt(value)
      const date = new Date()
      date.setDate(date.getDate() - days)
      setFilters({ ...filters, [key]: date.toISOString().split('T')[0] })
    } else {
      setFilters({ ...filters, [key]: value })
    }
  }

  const clearAllFilters = () => {
    console.log('Clearing all filters...')
    setPage(1)
    setFilters({})
    setSearchTerm('')
  }

  const activeFilterCount = Object.keys(filters).filter(k => filters[k] !== undefined).length

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Job Dashboard
          </h1>
          <p className="text-gray-600 mt-2 text-lg">Find your next opportunity with AI-powered insights</p>
        </div>
        <button
          onClick={() => setIsScrapingOpen(true)}
          className="mt-4 md:mt-0 flex items-center space-x-2 px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all shadow-lg"
        >
          <Play className="h-5 w-5" />
          <span>Start New Scrape</span>
        </button>
      </div>

      {/* Scrape Status Alert */}
      {scrapeStatus && (
        <div className={`flex items-center justify-between p-4 rounded-lg ${
          scrapeStatus.running ? 'bg-blue-50 border border-blue-200' : 'bg-red-50 border border-red-200'
        }`}>
          <div className="flex items-center space-x-3">
            {scrapeStatus.running ? (
              <Loader2 className="h-5 w-5 text-blue-600 animate-spin" />
            ) : (
              <X className="h-5 w-5 text-red-600" />
            )}
            <span className={scrapeStatus.running ? 'text-blue-800' : 'text-red-800'}>
              {scrapeStatus.message}
            </span>
          </div>
          <button onClick={() => setScrapeStatus(null)} className="text-gray-500 hover:text-gray-700">
            <X className="h-5 w-5" />
          </button>
        </div>
      )}

      {/* Stats Grid - Enhanced with gradients */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-gradient-to-br from-blue-500 to-blue-600 text-white rounded-xl shadow-lg p-6 transform hover:scale-105 transition-transform">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-blue-100 text-sm font-medium">Total Jobs</p>
              <p className="text-4xl font-bold mt-2">{stats?.total_jobs || 0}</p>
            </div>
            <Briefcase className="h-12 w-12 opacity-30" />
          </div>
        </div>

        <div className="bg-gradient-to-br from-green-500 to-green-600 text-white rounded-xl shadow-lg p-6 transform hover:scale-105 transition-transform">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-green-100 text-sm font-medium">New Today</p>
              <p className="text-4xl font-bold mt-2">{stats?.new_today || 0}</p>
            </div>
            <Clock className="h-12 w-12 opacity-30" />
          </div>
        </div>

        <div className="bg-gradient-to-br from-yellow-500 to-orange-500 text-white rounded-xl shadow-lg p-6 transform hover:scale-105 transition-transform">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-yellow-100 text-sm font-medium">High Match</p>
              <p className="text-4xl font-bold mt-2">{stats?.high_match_jobs || 0}</p>
            </div>
            <Star className="h-12 w-12 opacity-30" />
          </div>
        </div>

        <div className="bg-gradient-to-br from-purple-500 to-purple-600 text-white rounded-xl shadow-lg p-6 transform hover:scale-105 transition-transform">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-purple-100 text-sm font-medium">Applications</p>
              <p className="text-4xl font-bold mt-2">{stats?.total_applications || 0}</p>
            </div>
            <TrendingUp className="h-12 w-12 opacity-30" />
          </div>
        </div>
      </div>

      {/* Search and Quick Actions */}
      <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6">
        <div className="flex flex-col md:flex-row gap-4">
          {/* Search */}
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search jobs, companies, or locations..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          {/* Filter Button */}
          <button
            onClick={() => setShowFilters(!showFilters)}
            className={`flex items-center space-x-2 px-6 py-3 border rounded-lg transition-colors ${
              showFilters
                ? 'bg-blue-600 text-white border-blue-600'
                : 'border-gray-300 hover:bg-gray-50'
            }`}
          >
            <Filter className="h-5 w-5" />
            <span>Filters</span>
            {activeFilterCount > 0 && (
              <span className="ml-2 px-2 py-0.5 bg-white text-blue-600 rounded-full text-xs font-bold">
                {activeFilterCount}
              </span>
            )}
          </button>
        </div>

        {/* Advanced Filters Panel */}
        {showFilters && (
          <div className="mt-6 pt-6 border-t border-gray-200">
            <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
              {/* Source Filter */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Source</label>
                <select
                  value={filters.source || 'all'}
                  onChange={(e) => applyFilter('source', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                  {JOB_SOURCES.map((src) => (
                    <option key={src.value} value={src.value}>{src.label}</option>
                  ))}
                </select>
              </div>

              {/* Job Type Filter */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Job Type</label>
                <select
                  value={filters.job_type || 'all'}
                  onChange={(e) => applyFilter('job_type', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                  {JOB_TYPES.map((type) => (
                    <option key={type.value} value={type.value}>{type.label}</option>
                  ))}
                </select>
              </div>

              {/* Remote Type Filter */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Location Type</label>
                <select
                  value={filters.remote_type || 'all'}
                  onChange={(e) => applyFilter('remote_type', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                  {REMOTE_TYPES.map((type) => (
                    <option key={type.value} value={type.value}>{type.label}</option>
                  ))}
                </select>
              </div>

              {/* Experience Level Filter */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Experience</label>
                <select
                  value={filters.experience_level || 'all'}
                  onChange={(e) => applyFilter('experience_level', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                  {EXPERIENCE_LEVELS.map((level) => (
                    <option key={level.value} value={level.value}>{level.label}</option>
                  ))}
                </select>
              </div>

              {/* Date Posted Filter */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Date Posted</label>
                <select
                  value={filters.posted_after ? '7' : 'all'}
                  onChange={(e) => applyFilter('posted_after', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                  {DATE_RANGES.map((range) => (
                    <option key={range.value} value={range.value}>{range.label}</option>
                  ))}
                </select>
              </div>
            </div>
          </div>
        )}

        {/* Quick Match Score Filters */}
        <div className="flex flex-wrap gap-3 mt-4">
          <button
            onClick={() => {
              setPage(1)
              removeFilter('min_match_score')
            }}
            className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
              !filters.min_match_score
                ? 'bg-gray-600 text-white shadow-lg'
                : 'bg-gray-50 text-gray-700 hover:bg-gray-100'
            }`}
          >
            All Jobs
          </button>
          <button
            onClick={() => {
              setPage(1)
              setFilters({ min_match_score: 60 })
            }}
            className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
              filters.min_match_score === 60
                ? 'bg-green-600 text-white shadow-lg'
                : 'bg-green-50 text-green-700 hover:bg-green-100'
            }`}
          >
            60%+ Match
          </button>
          <button
            onClick={() => {
              setPage(1)
              setFilters({ min_match_score: 70 })
            }}
            className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
              filters.min_match_score === 70
                ? 'bg-blue-600 text-white shadow-lg'
                : 'bg-blue-50 text-blue-700 hover:bg-blue-100'
            }`}
          >
            70%+ Match
          </button>
          <button
            onClick={() => {
              setPage(1)
              setFilters({ min_match_score: 80 })
            }}
            className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
              filters.min_match_score === 80
                ? 'bg-purple-600 text-white shadow-lg'
                : 'bg-purple-50 text-purple-700 hover:bg-purple-100'
            }`}
          >
            80%+ Match
          </button>
          {activeFilterCount > 0 && (
            <button
              onClick={clearAllFilters}
              className="px-4 py-2 bg-red-100 text-red-700 rounded-full text-sm font-medium hover:bg-red-200 transition-all"
            >
              ✕ Clear All Filters
            </button>
          )}
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

      {/* Scrape Configuration Modal */}
      {isScrapingOpen && (
        <div className="fixed inset-0 z-50 overflow-y-auto">
          <div className="fixed inset-0 bg-black bg-opacity-50" onClick={() => setIsScrapingOpen(false)} />
          <div className="relative min-h-screen flex items-center justify-center p-4">
            <div className="relative bg-white rounded-xl shadow-2xl max-w-lg w-full p-6">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-2xl font-bold text-gray-900">Start New Scrape</h3>
                <button
                  onClick={() => setIsScrapingOpen(false)}
                  className="p-2 hover:bg-gray-100 rounded-lg"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Job Title / Keyword *
                  </label>
                  <input
                    type="text"
                    value={scrapeKeyword}
                    onChange={(e) => setScrapeKeyword(e.target.value)}
                    placeholder="e.g., Data Scientist, Software Engineer"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Location *
                  </label>
                  <input
                    type="text"
                    value={scrapeLocation}
                    onChange={(e) => setScrapeLocation(e.target.value)}
                    placeholder="e.g., Germany, Berlin"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <p className="text-sm text-blue-800">
                    <strong>Note:</strong> Scraping will fetch jobs from all available sources (LinkedIn, Indeed, StepStone, etc.). This process may take a few minutes.
                  </p>
                </div>

                <div className="flex space-x-3 mt-6">
                  <button
                    onClick={handleStartScrape}
                    disabled={!scrapeKeyword.trim() || scrapeMutation.isPending}
                    className="flex-1 flex items-center justify-center space-x-2 px-4 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {scrapeMutation.isPending ? (
                      <>
                        <Loader2 className="h-5 w-5 animate-spin" />
                        <span>Starting...</span>
                      </>
                    ) : (
                      <>
                        <Play className="h-5 w-5" />
                        <span>Start Scraping</span>
                      </>
                    )}
                  </button>
                  <button
                    onClick={() => setIsScrapingOpen(false)}
                    className="px-6 py-3 border border-gray-300 rounded-lg hover:bg-gray-50"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
