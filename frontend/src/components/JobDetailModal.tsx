import { X, ExternalLink, Download, FileText, Briefcase, TrendingUp, AlertCircle, Loader2, CheckCircle2 } from 'lucide-react'
import { Job, JobAnalysis } from '../types'
import { formatDate, getMatchScoreBadgeColor, cn } from '../lib/utils'
import { useAnalyzeJob } from '../hooks/useAnalysis'
import { useState } from 'react'

interface JobDetailModalProps {
  job: Job
  analysis?: JobAnalysis | null
  isOpen: boolean
  onClose: () => void
}

export default function JobDetailModal({ job, analysis, isOpen, onClose }: JobDetailModalProps) {
  const analyzeJobMutation = useAnalyzeJob()
  const [showSuccessMessage, setShowSuccessMessage] = useState(false)
  const [isAnalyzing, setIsAnalyzing] = useState(false)

  if (!isOpen) return null

  const handleAnalyze = () => {
    // Prevent double-clicks
    if (isAnalyzing || analyzeJobMutation.isPending) {
      console.log('⏳ Analysis already in progress, please wait...')
      return
    }

    console.log('🚀 Starting AI Analysis for job:', job.id)
    setIsAnalyzing(true)
    setShowSuccessMessage(true)
    
    analyzeJobMutation.mutate(
      { jobId: job.id, generateMaterials: true },
      {
        onSuccess: () => {
          console.log('✅ Analysis API call successful')
          // Keep analyzing state true until results appear
          setTimeout(() => {
            setIsAnalyzing(false)
          }, 45000) // Reset after 45 seconds
        },
        onError: (error) => {
          console.error('❌ Analysis failed:', error)
          setShowSuccessMessage(false)
          setIsAnalyzing(false)
          alert('Failed to start analysis. Please try again.')
        }
      }
    )
  }

  const matchScore = analysis?.match_score || 0
  
  // Check if we have FULL analysis (with tailored materials) or just basic match score
  const hasFullAnalysis = analysis && (
    analysis.tailored_resume || 
    analysis.tailored_cover_letter || 
    (analysis.recommendations && Object.keys(analysis.recommendations).length > 0)
  )

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
                  
                  {/* Salary */}
                  {job.salary && (
                    <div className="mb-3 flex items-center">
                      <span className="text-2xl mr-2">💰</span>
                      <div>
                        <span className="font-medium text-gray-700">Salary: </span>
                        <span className="text-gray-900 font-semibold">{job.salary}</span>
                      </div>
                    </div>
                  )}
                  
                  {/* Languages */}
                  {job.languages && job.languages.length > 0 && (
                    <div className="mb-3 flex items-center">
                      <span className="text-2xl mr-2">🗣️</span>
                      <div>
                        <span className="font-medium text-gray-700">Languages: </span>
                        <span className="text-gray-900">{job.languages.join(', ')}</span>
                      </div>
                    </div>
                  )}
                  
                  {/* Tags */}
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
                {hasFullAnalysis ? (
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
                        <p className="text-sm text-gray-600 mt-2">Overall Match</p>
                      </div>
                    </div>

                    {/* Detailed ATS Score Section */}
                    <div className="bg-white border-2 border-purple-200 rounded-lg p-6">
                      <h3 className="text-lg font-bold text-purple-900 mb-4 flex items-center">
                        <svg className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        ATS Compatibility Score
                      </h3>
                      
                      {/* ATS Score Breakdown */}
                      <div className="space-y-4">
                        {/* Overall ATS Score */}
                        <div className="flex items-center justify-between">
                          <span className="text-sm font-medium text-gray-700">Overall ATS Score</span>
                          <span className={cn(
                            'text-2xl font-bold',
                            (analysis.ats_score || 0) >= 75 ? 'text-green-600' :
                            (analysis.ats_score || 0) >= 60 ? 'text-yellow-600' : 'text-red-600'
                          )}>
                            {(analysis.ats_score || 0).toFixed(0)}%
                          </span>
                        </div>
                        <p className="text-xs text-gray-500 -mt-2">
                          {(analysis.ats_score || 0) >= 75 ? '✅ Excellent! Strong chance of passing ATS' :
                           (analysis.ats_score || 0) >= 60 ? '⚠️ Good, but could be improved' : 
                           '❌ Needs improvement to pass ATS screening'}
                        </p>

                        {/* Keyword Match */}
                        <div>
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-sm text-gray-700">Keyword Match Rate</span>
                            <span className="text-sm font-bold text-blue-600">
                              {((analysis as any).keyword_analysis?.keyword_match_rate || 0).toFixed(1)}%
                            </span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2 mb-1">
                            <div
                              className={cn(
                                'h-2 rounded-full',
                                ((analysis as any).keyword_analysis?.keyword_match_rate || 0) >= 75 ? 'bg-green-500' :
                                ((analysis as any).keyword_analysis?.keyword_match_rate || 0) >= 50 ? 'bg-yellow-500' : 'bg-red-500'
                              )}
                              style={{ width: `${Math.min(((analysis as any).keyword_analysis?.keyword_match_rate || 0), 100)}%` }}
                            ></div>
                          </div>
                          <p className="text-xs text-gray-600">
                            {((analysis as any).keyword_analysis?.found_in_resume || 0)} of {((analysis as any).keyword_analysis?.total_jd_keywords || 0)} JD keywords found
                            {((analysis as any).keyword_analysis?.exact_matches || 0) > 0 && 
                              ` (${((analysis as any).keyword_analysis?.exact_matches || 0)} exact matches)`
                            }
                          </p>
                        </div>

                        {/* Hard Skills Match */}
                        {((analysis as any).keyword_analysis?.hard_skills_match !== undefined) && (
                          <div>
                            <div className="flex items-center justify-between mb-2">
                              <span className="text-sm text-gray-700">Hard Skills Match</span>
                              <span className="text-sm font-bold text-purple-600">
                                {((analysis as any).keyword_analysis?.hard_skills_match || 0).toFixed(0)}%
                              </span>
                            </div>
                            <div className="w-full bg-gray-200 rounded-full h-2">
                              <div
                                className="bg-purple-600 h-2 rounded-full"
                                style={{ width: `${((analysis as any).keyword_analysis?.hard_skills_match || 0)}%` }}
                              ></div>
                            </div>
                          </div>
                        )}

                        {/* Action Verbs & Achievements */}
                        {(((analysis as any).keyword_analysis?.action_verbs_count || 0) > 0 || 
                          ((analysis as any).keyword_analysis?.quantifiable_achievements_count || 0) > 0) && (
                          <div className="grid grid-cols-2 gap-4 pt-2 border-t">
                            <div className="text-center">
                              <p className="text-2xl font-bold text-indigo-600">
                                {((analysis as any).keyword_analysis?.action_verbs_count || 0)}
                              </p>
                              <p className="text-xs text-gray-600">Action Verbs</p>
                            </div>
                            <div className="text-center">
                              <p className="text-2xl font-bold text-emerald-600">
                                {((analysis as any).keyword_analysis?.quantifiable_achievements_count || 0)}
                              </p>
                              <p className="text-xs text-gray-600">Quantified Results</p>
                            </div>
                          </div>
                        )}

                        {/* Missing Sections Alert */}
                        {analysis.missing_skills.length > 0 && (
                          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3 mt-4">
                            <p className="text-xs font-semibold text-yellow-800 mb-2">
                              ⚠️ Missing Key Elements:
                            </p>
                            <ul className="text-xs text-yellow-700 space-y-1">
                              {analysis.missing_skills.slice(0, 3).map((skill, idx) => (
                                <li key={idx}>• {skill}</li>
                              ))}
                            </ul>
                          </div>
                        )}

                        {/* Improvement Suggestions */}
                        {analysis.recommendations?.resume && (
                          <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 mt-4">
                            <p className="text-xs font-semibold text-blue-800 mb-2">
                              💡 Improvement Suggestions:
                            </p>
                            <ul className="text-xs text-blue-700 space-y-1">
                              {analysis.recommendations.resume.slice(0, 3).map((rec, idx) => (
                                <li key={idx}>• {rec}</li>
                              ))}
                            </ul>
                          </div>
                        )}

                        {/* Generate Button */}
                        <button
                          onClick={handleAnalyze}
                          className="w-full mt-4 px-4 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg hover:from-purple-700 hover:to-blue-700 transition-all shadow-lg font-medium text-sm"
                        >
                          🚀 Generate Tailored Resume & Cover Letter
                        </button>
                      </div>
                    </div>

                    {/* Matching Skills */}
                    {analysis.matching_skills.length > 0 && (
                      <div>
                        <h4 className="flex items-center text-sm font-semibold text-gray-900 mb-3">
                          <TrendingUp className="h-4 w-4 mr-2 text-green-600" />
                          Your Matching Skills ({analysis.matching_skills.length})
                        </h4>
                        <div className="flex flex-wrap gap-2">
                          {analysis.matching_skills.map((skill, index) => (
                            <span
                              key={index}
                              className="px-2 py-1 bg-green-50 text-green-700 text-xs rounded border border-green-200"
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
                          Skills to Develop ({analysis.missing_skills.length})
                        </h4>
                        <div className="flex flex-wrap gap-2">
                          {analysis.missing_skills.map((skill, index) => (
                            <span
                              key={index}
                              className="px-2 py-1 bg-yellow-50 text-yellow-700 text-xs rounded border border-yellow-200"
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
                  <div className="text-center p-8">
                    {showSuccessMessage && (
                      <div className="mb-4 p-4 bg-green-50 border border-green-200 rounded-lg">
                        <div className="flex items-center justify-center space-x-2 text-green-800">
                          <CheckCircle2 className="h-5 w-5" />
                          <p className="font-medium">Analysis running in background</p>
                        </div>
                        <p className="text-sm text-green-700 mt-2">
                          Results will appear in 30-45 seconds. You can close this and check back later.
                        </p>
                      </div>
                    )}
                    
                    {analyzeJobMutation.isPending ? (
                      <div className="space-y-4">
                        <Loader2 className="h-12 w-12 text-blue-600 animate-spin mx-auto" />
                        <p className="text-lg font-semibold text-gray-900">Processing AI Analysis...</p>
                        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 text-left">
                          <p className="text-sm font-medium text-blue-900 mb-2">
                            🤖 Running 5 AI Agents:
                          </p>
                          <div className="text-xs text-blue-800 space-y-1">
                            <div>• Job Description Analyzer</div>
                            <div>• Resume Matcher (42-point ATS check)</div>
                            <div>• Enhanced ATS Scorer</div>
                            <div>• Application Optimizer</div>
                            <div>• Company Researcher</div>
                          </div>
                        </div>
                        <p className="text-sm text-gray-600">
                          ⏱️ Processing... typically takes 30-45 seconds
                        </p>
                        <p className="text-xs text-gray-500">
                          Feel free to close this modal. Analysis continues in background.
                        </p>
                      </div>
                    ) : (
                      <>
                        <div className="mb-4">
                          {job.match_score !== null && job.match_score !== undefined && job.match_score > 0 ? (
                            <div className="mb-4 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border-2 border-blue-200">
                              <div className="flex items-center justify-center space-x-4 mb-2">
                                <div className={cn(
                                  'px-6 py-3 rounded-full text-white font-bold text-3xl shadow-lg',
                                  getMatchScoreBadgeColor(job.match_score)
                                )}>
                                  {job.match_score.toFixed(0)}%
                                </div>
                                <div className="text-left">
                                  <p className="text-sm font-bold text-gray-800">Resume Match Score</p>
                                  <p className="text-xs text-gray-600">Keywords & skills matching</p>
                                </div>
                              </div>
                              <div className="border-t border-blue-200 pt-2 mt-2">
                                <p className="text-xs text-gray-700">
                                  ⚡ Click below for detailed ATS score & tailored materials
                                </p>
                              </div>
                            </div>
                          ) : (
                            <p className="text-gray-600 mb-4">No match score available yet</p>
                          )}
                          <button
                            onClick={handleAnalyze}
                            disabled={isAnalyzing || analyzeJobMutation.isPending}
                            className="w-full px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-lg hover:from-blue-700 hover:to-indigo-700 transition-all shadow-lg disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
                          >
                            <TrendingUp className="h-5 w-5" />
                            <span className="font-semibold">
                              {isAnalyzing ? 'Starting Analysis...' : 'Run Full AI Analysis'}
                            </span>
                          </button>
                          <p className="text-xs text-gray-500 mt-2 text-center">
                            🤖 5 AI Agents • 42-Point ATS • Tailored Materials • 30-45s
                          </p>
                        </div>
                      </>
                    )}
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
