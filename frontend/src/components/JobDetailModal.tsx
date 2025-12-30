import { X, ExternalLink, Download, FileText, Briefcase, TrendingUp, AlertCircle } from 'lucide-react'
import { Job, JobAnalysis } from '../types'
import { formatDate, getMatchScoreBadgeColor, cn } from '../lib/utils'
import { useAnalyzeJob } from '../hooks/useAnalysis'

interface JobDetailModalProps {
  job: Job
  analysis?: JobAnalysis | null
  isOpen: boolean
  onClose: () => void
}

export default function JobDetailModal({ job, analysis, isOpen, onClose }: JobDetailModalProps) {
  const analyzeJobMutation = useAnalyzeJob()

  if (!isOpen) return null

  const handleAnalyze = () => {
    analyzeJobMutation.mutate({ jobId: job.id, generateMaterials: true })
  }

  const matchScore = analysis?.match_score || 0

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      {/* Backdrop */}
      <div className="fixed inset-0 bg-black bg-opacity-50" onClick={onClose} />

      {/* Modal */}
      <div className="relative min-h-screen flex items-center justify-center p-4">
        <div className="relative bg-white rounded-xl shadow-2xl max-w-6xl w-full max-h-[90vh] overflow-hidden flex flex-col">
          {/* Header */}
          <div className="flex items-start justify-between p-6 border-b border-gray-200">
            <div className="flex-1 pr-4">
              <h2 className="text-2xl font-bold text-gray-900 mb-2">{job.title}</h2>
              <div className="flex items-center space-x-4 text-sm text-gray-600">
                <span className="flex items-center">
                  <Briefcase className="h-4 w-4 mr-1" />
                  {job.company}
                </span>
                <span>📍 {job.location}</span>
                <span>📅 {formatDate(job.posted_date)}</span>
              </div>
            </div>
            <button
              onClick={onClose}
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <X className="h-6 w-6" />
            </button>
          </div>

          {/* Content */}
          <div className="flex-1 overflow-y-auto">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 p-6">
              {/* Left: Job Description (2/3) */}
              <div className="lg:col-span-2 space-y-6">
                {/* Job Details */}
                <div>
                  <h3 className="text-lg font-semibold mb-3">Job Details</h3>
                  {job.salary && (
                    <div className="mb-2">
                      <span className="font-medium">Salary:</span> {job.salary}
                    </div>
                  )}
                  <div className="flex flex-wrap gap-2 mb-4">
                    {job.job_type && (
                      <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm">
                        {job.job_type}
                      </span>
                    )}
                    {job.remote_type && (
                      <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm">
                        {job.remote_type}
                      </span>
                    )}
                    {job.experience_level && (
                      <span className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm">
                        {job.experience_level}
                      </span>
                    )}
                  </div>
                </div>

                {/* Description */}
                <div>
                  <h3 className="text-lg font-semibold mb-3">Description</h3>
                  <div className="prose prose-sm max-w-none text-gray-700 whitespace-pre-wrap">
                    {job.description}
                  </div>
                </div>

                {/* Requirements */}
                {job.requirements && (
                  <div>
                    <h3 className="text-lg font-semibold mb-3">Requirements</h3>
                    <div className="prose prose-sm max-w-none text-gray-700 whitespace-pre-wrap">
                      {job.requirements}
                    </div>
                  </div>
                )}

                {/* Benefits */}
                {job.benefits && (
                  <div>
                    <h3 className="text-lg font-semibold mb-3">Benefits</h3>
                    <div className="prose prose-sm max-w-none text-gray-700 whitespace-pre-wrap">
                      {job.benefits}
                    </div>
                  </div>
                )}

                {/* Apply Button */}
                <div className="flex space-x-3">
                  <a
                    href={job.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center space-x-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                  >
                    <span>Apply on {job.source}</span>
                    <ExternalLink className="h-4 w-4" />
                  </a>
                </div>
              </div>

              {/* Right: AI Analysis (1/3) */}
              <div className="space-y-6">
                {/* Match Score */}
                {analysis ? (
                  <>
                    <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg p-6">
                      <h3 className="text-lg font-semibold mb-4">AI Analysis</h3>
                      
                      {/* Match Score Gauge */}
                      <div className="text-center mb-6">
                        <div className={cn(
                          'inline-flex items-center justify-center w-24 h-24 rounded-full text-white text-3xl font-bold',
                          getMatchScoreBadgeColor(matchScore)
                        )}>
                          {matchScore.toFixed(0)}%
                        </div>
                        <p className="text-sm text-gray-600 mt-2">Match Score</p>
                      </div>

                      {/* ATS Score */}
                      {analysis.ats_score && (
                        <div className="text-center mb-6">
                          <div className="text-2xl font-bold text-gray-700">
                            {analysis.ats_score.toFixed(0)}%
                          </div>
                          <p className="text-sm text-gray-600">ATS Score</p>
                        </div>
                      )}
                    </div>

                    {/* Matching Skills */}
                    {analysis.matching_skills.length > 0 && (
                      <div>
                        <h4 className="flex items-center text-sm font-semibold text-gray-900 mb-3">
                          <TrendingUp className="h-4 w-4 mr-2 text-green-600" />
                          Matching Skills
                        </h4>
                        <div className="flex flex-wrap gap-2">
                          {analysis.matching_skills.map((skill, index) => (
                            <span
                              key={index}
                              className="px-2 py-1 bg-green-50 text-green-700 text-xs rounded"
                            >
                              ✓ {skill}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Missing Skills */}
                    {analysis.missing_skills.length > 0 && (
                      <div>
                        <h4 className="flex items-center text-sm font-semibold text-gray-900 mb-3">
                          <AlertCircle className="h-4 w-4 mr-2 text-yellow-600" />
                          Skills to Develop
                        </h4>
                        <div className="flex flex-wrap gap-2">
                          {analysis.missing_skills.map((skill, index) => (
                            <span
                              key={index}
                              className="px-2 py-1 bg-yellow-50 text-yellow-700 text-xs rounded"
                            >
                              ○ {skill}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Actions */}
                    <div className="space-y-2">
                      {analysis.tailored_resume && (
                        <button className="w-full flex items-center justify-center space-x-2 px-4 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                          <Download className="h-4 w-4" />
                          <span className="text-sm">Download Tailored Resume</span>
                        </button>
                      )}
                      {analysis.tailored_cover_letter && (
                        <button className="w-full flex items-center justify-center space-x-2 px-4 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                          <FileText className="h-4 w-4" />
                          <span className="text-sm">View Cover Letter</span>
                        </button>
                      )}
                    </div>
                  </>
                ) : (
                  <div className="text-center p-6">
                    <p className="text-gray-600 mb-4">No AI analysis yet</p>
                    <button
                      onClick={handleAnalyze}
                      disabled={analyzeJobMutation.isPending}
                      className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
                    >
                      {analyzeJobMutation.isPending ? 'Analyzing...' : 'Run AI Analysis'}
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
