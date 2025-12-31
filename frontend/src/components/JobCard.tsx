import { MapPin, Building2, Calendar, ExternalLink, TrendingUp } from 'lucide-react'
import { Job, JobAnalysis } from '../types'
import { formatRelativeTime, formatSalary, getMatchScoreBadgeColor, truncateText } from '../lib/utils'
import { cn } from '../lib/utils'

interface JobCardProps {
  job: Job
  analysis?: JobAnalysis | null
  onClick?: () => void
}

export default function JobCard({ job, analysis, onClick }: JobCardProps) {
  const matchScore = analysis?.match_score || 0
  const atsScore = analysis?.ats_score || 0

  return (
    <div
      onClick={onClick}
      className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-lg transition-shadow cursor-pointer animate-fadeIn"
    >
      {/* Header */}
      <div className="flex justify-between items-start mb-3">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-900 mb-1">
            {job.title}
          </h3>
          <div className="flex items-center space-x-2 text-sm text-gray-600">
            <Building2 className="h-4 w-4" />
            <span>{job.company}</span>
          </div>
        </div>

        {/* Match Score Badge */}
        {analysis && (
          <div className="flex flex-col items-end space-y-1">
            <div
              className={cn(
                'px-3 py-1 rounded-full text-white font-bold text-sm',
                getMatchScoreBadgeColor(matchScore)
              )}
            >
              {matchScore.toFixed(0)}% Match
            </div>
            {atsScore > 0 && (
              <div className="text-xs text-gray-500">
                ATS: {atsScore.toFixed(0)}%
              </div>
            )}
          </div>
        )}
      </div>

      {/* Details */}
      <div className="space-y-2 mb-4">
        <div className="flex items-center text-sm text-gray-600">
          <MapPin className="h-4 w-4 mr-2" />
          <span>{job.location}</span>
          {job.remote_type && (
            <span className="ml-2 px-2 py-0.5 bg-green-100 text-green-800 rounded text-xs">
              {job.remote_type}
            </span>
          )}
        </div>

        {job.salary && (
          <div className="text-sm text-gray-700 font-medium">
            💰 {formatSalary(job.salary)}
          </div>
        )}

        {job.languages && job.languages.length > 0 && (
          <div className="text-sm text-gray-600">
            🗣️ {job.languages.join(', ')}
          </div>
        )}

        <div className="flex items-center text-sm text-gray-500">
          <Calendar className="h-4 w-4 mr-2" />
          <span>Posted {formatRelativeTime(job.posted_date)}</span>
        </div>
      </div>

      {/* Description Preview */}
      <p className="text-sm text-gray-600 mb-4 line-clamp-2">
        {truncateText(job.description, 150)}
      </p>

      {/* Footer */}
      <div className="flex items-center justify-between pt-4 border-t border-gray-100">
        <div className="flex items-center space-x-2">
          <span className="text-xs px-2 py-1 bg-gray-100 text-gray-700 rounded">
            {job.source}
          </span>
          {job.job_type && (
            <span className="text-xs px-2 py-1 bg-blue-100 text-blue-700 rounded">
              {job.job_type}
            </span>
          )}
        </div>

        <a
          href={job.url}
          target="_blank"
          rel="noopener noreferrer"
          onClick={(e) => e.stopPropagation()}
          className="flex items-center space-x-1 text-sm text-blue-600 hover:text-blue-800"
        >
          <span>View Job</span>
          <ExternalLink className="h-4 w-4" />
        </a>
      </div>

      {/* Matching Skills (if available) */}
      {analysis && analysis.matching_skills.length > 0 && (
        <div className="mt-4 pt-4 border-t border-gray-100">
          <div className="flex items-center space-x-2 mb-2">
            <TrendingUp className="h-4 w-4 text-green-600" />
            <span className="text-xs font-medium text-gray-700">Matching Skills</span>
          </div>
          <div className="flex flex-wrap gap-1">
            {analysis.matching_skills.slice(0, 5).map((skill, index) => (
              <span
                key={index}
                className="text-xs px-2 py-1 bg-green-50 text-green-700 rounded"
              >
                {skill}
              </span>
            ))}
            {analysis.matching_skills.length > 5 && (
              <span className="text-xs px-2 py-1 bg-gray-50 text-gray-600 rounded">
                +{analysis.matching_skills.length - 5} more
              </span>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
