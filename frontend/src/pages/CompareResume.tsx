import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { FileText, Sparkles, AlertCircle, CheckCircle, TrendingUp, Upload } from 'lucide-react'
import { analysisApi } from '../lib/api'

export default function CompareResume() {
  const [resumeText, setResumeText] = useState('')
  const [jdText, setJdText] = useState('')
  const [analysis, setAnalysis] = useState<any>(null)
  const [pdfFile, setPdfFile] = useState<File | null>(null)

  // PDF upload mutation
  const uploadPdfMutation = useMutation({
    mutationFn: async (file: File) => {
      const formData = new FormData()
      formData.append('file', file)
      
      const response = await fetch('http://localhost:8000/api/analysis/parse-resume-pdf', {
        method: 'POST',
        body: formData
      })
      
      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Failed to parse PDF')
      }
      
      return response.json()
    },
    onSuccess: (data) => {
      setResumeText(data.resume_text)
      // Success message shown in UI, no alert needed
    },
    onError: (error: any) => {
      alert(`❌ Failed to parse PDF: ${error.message}`)
    }
  })

  const analyzeMutation = useMutation({
    mutationFn: async () => {
      if (!resumeText.trim()) throw new Error('Please enter your resume text or upload PDF')
      if (!jdText.trim()) throw new Error('Please enter job description')
      
      const response = await analysisApi.analyzeCustom(resumeText, jdText)
      return response.data
    },
    onSuccess: (data) => {
      setAnalysis(data)
      console.log('✅ CV-JD comparison completed with multi-layer ATS', data)
    },
    onError: (error: any) => {
      const errorMsg = error.response?.data?.detail || error.message || 'Analysis failed'
      console.error('❌ Analysis error:', errorMsg)
      alert(`❌ ${errorMsg}`)
    },
  })

  const handlePdfUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file && file.type === 'application/pdf') {
      setPdfFile(file)
      uploadPdfMutation.mutate(file)
    } else {
      alert('Please select a valid PDF file')
    }
  }

  const handleLoadFromProfile = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/user/profile')
      const data = await response.json()
      if (data.resume_text) {
        setResumeText(data.resume_text)
        alert('✅ Resume loaded from profile')
      } else {
        alert('⚠️ No resume found. Please upload your resume in Settings first.')
      }
    } catch (error) {
      alert('❌ Failed to load resume from profile')
      console.error(error)
    }
  }

  const handleClearResume = () => {
    setResumeText('')
  }

  const handleClearJD = () => {
    setJdText('')
  }

  const handleAnalyze = () => {
    if (!resumeText || !jdText) {
      alert('Please enter both resume and job description')
      return
    }
    setAnalysis(null) // Clear previous results
    analyzeMutation.mutate()
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-3">
            <FileText className="h-8 w-8 text-blue-600" />
            Manual Resume-JD Comparison
          </h1>
          <p className="text-gray-600 mt-2">
            Compare your resume against any job description with AI-powered analysis
          </p>
        </div>

        {/* Split View */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Left: Resume */}
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900">Your Resume</h2>
              <span className="text-sm text-gray-500">{resumeText.length} characters</span>
            </div>
            
            <textarea
              value={resumeText}
              onChange={(e) => setResumeText(e.target.value)}
              placeholder="Upload PDF above OR paste your resume text here..."
              className="w-full h-96 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none font-mono text-sm"
            />
            <div className="mt-4 flex gap-2">
              <button 
                onClick={handleLoadFromProfile}
                className="px-4 py-2 text-sm text-blue-600 border border-blue-600 rounded-lg hover:bg-blue-50 transition-colors"
              >
                Load from Profile
              </button>
              <label className="px-4 py-2 text-sm text-purple-600 border border-purple-600 rounded-lg hover:bg-purple-50 transition-colors cursor-pointer inline-flex items-center gap-2">
                <Upload className="h-4 w-4" />
                {uploadPdfMutation.isPending ? 'Parsing...' : 'Upload PDF'}
                <input 
                  type="file" 
                  accept="application/pdf" 
                  onChange={handlePdfUpload}
                  className="hidden"
                  disabled={uploadPdfMutation.isPending}
                />
              </label>
              <button 
                onClick={handleClearResume}
                className="px-4 py-2 text-sm text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Clear
              </button>
              {pdfFile && !uploadPdfMutation.isPending && (
                <span className="px-3 py-2 text-xs text-green-700 bg-green-50 rounded-lg border border-green-200">
                  ✓ {pdfFile.name.substring(0, 20)}{pdfFile.name.length > 20 ? '...' : ''}
                </span>
              )}
            </div>
          </div>

          {/* Right: Job Description */}
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900">Job Description</h2>
              <span className="text-sm text-gray-500">{jdText.length} characters</span>
            </div>
            <textarea
              value={jdText}
              onChange={(e) => setJdText(e.target.value)}
              placeholder="Paste the job description here... Include requirements, qualifications, and responsibilities."
              className="w-full h-96 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none font-mono text-sm"
            />
            <div className="mt-4 flex gap-2">
              <button 
                onClick={handleClearJD}
                className="px-4 py-2 text-sm text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Clear
              </button>
            </div>
          </div>
        </div>

        {/* Analyze Button */}
        <div className="text-center mb-8">
          <button
            onClick={handleAnalyze}
            disabled={analyzeMutation.isPending || !resumeText.trim() || !jdText.trim()}
            className="px-8 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-lg font-semibold text-lg hover:from-blue-700 hover:to-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-xl flex items-center mx-auto gap-3"
          >
            {analyzeMutation.isPending ? (
              <>
                <div className="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full"></div>
                Analyzing with AI...
              </>
            ) : (
              <>
                <Sparkles className="h-5 w-5" />
                Analyze with AI
              </>
            )}
          </button>
          {(!resumeText.trim() || !jdText.trim()) && (
            <p className="mt-3 text-sm text-gray-500">Enter both resume and job description to analyze</p>
          )}
        </div>

        {/* Scoring Rules Info */}
        <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border border-blue-200 p-6 mb-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <TrendingUp className="h-5 w-5 mr-2 text-blue-600" />
            Multi-Layer AI ATS Scoring (DeepSeek + GPT-5-mini)
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-white rounded-lg p-4 border-2 border-blue-200">
              <h4 className="font-semibold text-blue-900 mb-3">Layer 1: DeepSeek-V3.2 (30%)</h4>
              <div className="space-y-2 text-sm text-gray-700">
                <div>• Fast baseline scoring</div>
                <div>• Skills & experience match</div>
                <div>• Quick assessment</div>
              </div>
            </div>
            <div className="bg-white rounded-lg p-4 border-2 border-green-200">
              <h4 className="font-semibold text-green-900 mb-3">Layer 2: GPT-5-mini (40%)</h4>
              <div className="space-y-2 text-sm text-gray-700">
                <div>• Validation & verification</div>
                <div>• Context understanding</div>
                <div>• Highest weight</div>
              </div>
            </div>
            <div className="bg-white rounded-lg p-4 border-2 border-purple-200">
              <h4 className="font-semibold text-purple-900 mb-3">Layer 3: DeepSeek-R1 (30%)</h4>
              <div className="space-y-2 text-sm text-gray-700">
                <div>• Deep reasoning</div>
                <div>• Quality assessment</div>
                <div>• Detailed feedback</div>
              </div>
            </div>
          </div>
          <div className="mt-4 text-center text-sm text-gray-600">
            Final Score = (Layer 1 × 30%) + (Layer 2 × 40%) + (Layer 3 × 30%)
          </div>
        </div>

        {/* Results */}
        {analysis && (
          <div className="space-y-6 animate-fadeIn">
            {/* 43-Point ATS Criteria Info */}
            <div className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg border border-green-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-3 flex items-center">
                <CheckCircle className="h-5 w-5 mr-2 text-green-600" />
                43-Point ATS Assessment Criteria
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-sm text-gray-700">
                <div className="bg-white rounded p-3">
                  <h4 className="font-semibold text-green-900 mb-2">Keywords (12 checks)</h4>
                  <div className="space-y-1">
                    <div>• Keyword density</div>
                    <div>• Skills match</div>
                    <div>• Technical terms</div>
                    <div>• Industry jargon</div>
                  </div>
                </div>
                <div className="bg-white rounded p-3">
                  <h4 className="font-semibold text-blue-900 mb-2">Fonts & Text (11 checks)</h4>
                  <div className="space-y-1">
                    <div>• Font readability</div>
                    <div>• Font size</div>
                    <div>• Special characters</div>
                    <div>• Text formatting</div>
                  </div>
                </div>
                <div className="bg-white rounded p-3">
                  <h4 className="font-semibold text-purple-900 mb-2">Layout (10 checks)</h4>
                  <div className="space-y-1">
                    <div>• Section headers</div>
                    <div>• Bullet points</div>
                    <div>• Tables & columns</div>
                    <div>• Graphics usage</div>
                  </div>
                </div>
                <div className="bg-white rounded p-3">
                  <h4 className="font-semibold text-indigo-900 mb-2">Structure (10 checks)</h4>
                  <div className="space-y-1">
                    <div>• Contact info</div>
                    <div>• Experience format</div>
                    <div>• Date formatting</div>
                    <div>• File metadata</div>
                  </div>
                </div>
              </div>
              <div className="mt-4 text-center text-sm text-gray-600">
                Complete industry-standard ATS compatibility check covering all major tracking systems
              </div>
            </div>

            {/* Match Score Card */}
            <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg border border-blue-200 p-8">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Overall Match */}
                <div className="text-center">
                  <div className="inline-flex items-center justify-center w-32 h-32 rounded-full bg-blue-600 text-white text-4xl font-bold mb-3">
                    {analysis.match_score || 0}%
                  </div>
                  <p className="text-lg font-semibold text-gray-900">Overall Match</p>
                  <p className="text-sm text-gray-600">Resume-JD Compatibility</p>
                </div>

                {/* ATS Score */}
                <div className="text-center">
                  <div className="inline-flex items-center justify-center w-32 h-32 rounded-full bg-green-600 text-white text-4xl font-bold mb-3">
                    {analysis.ats_score || 0}%
                  </div>
                  <p className="text-lg font-semibold text-gray-900">ATS Score</p>
                  <p className="text-sm text-gray-600">Applicant Tracking System</p>
                </div>

                {/* Keyword Match */}
                <div className="text-center">
                  <div className="inline-flex items-center justify-center w-32 h-32 rounded-full bg-purple-600 text-white text-4xl font-bold mb-3">
                    {analysis.keyword_density || 0}%
                  </div>
                  <p className="text-lg font-semibold text-gray-900">Keyword Match</p>
                  <p className="text-sm text-gray-600">JD Keywords Found</p>
                </div>
              </div>
            </div>

            {/* Detailed Analysis */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Matching Skills */}
              <div className="bg-white rounded-lg border border-gray-200 p-6">
                <h3 className="flex items-center text-lg font-semibold text-gray-900 mb-4">
                  <CheckCircle className="h-5 w-5 mr-2 text-green-600" />
                  Matching Skills ({analysis.matching_skills?.length || 0})
                </h3>
                <div className="flex flex-wrap gap-2">
                  {analysis.matching_skills?.map((skillItem: any, index: number) => {
                    const skillName = typeof skillItem === 'string' ? skillItem : skillItem.skill
                    const level = typeof skillItem === 'object' ? skillItem.level : null
                    return (
                      <span
                        key={index}
                        className="px-3 py-1 bg-green-50 text-green-700 rounded-full text-sm font-medium"
                        title={level ? `Your level: ${level}` : undefined}
                      >
                        ✓ {skillName}
                      </span>
                    )
                  })}
                </div>
              </div>

              {/* Missing Skills */}
              <div className="bg-white rounded-lg border border-gray-200 p-6">
                <h3 className="flex items-center text-lg font-semibold text-gray-900 mb-4">
                  <AlertCircle className="h-5 w-5 mr-2 text-yellow-600" />
                  Skills to Add ({analysis.missing_skills?.length || 0})
                </h3>
                <div className="flex flex-wrap gap-2">
                  {analysis.missing_skills?.map((skill: string, index: number) => (
                    <span
                      key={index}
                      className="px-3 py-1 bg-yellow-50 text-yellow-700 rounded-full text-sm font-medium"
                    >
                      ○ {skill}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            {/* ATS Detailed Analysis */}
            <div className="bg-white rounded-lg border border-gray-200 p-6">
              <h3 className="flex items-center text-lg font-semibold text-gray-900 mb-4">
                <TrendingUp className="h-5 w-5 mr-2 text-blue-600" />
                Detailed Analysis & Recommendations
              </h3>
              
              <div className="space-y-4">
                {/* ATS Recommendations */}
                {analysis.ats_details?.recommendations && analysis.ats_details.recommendations.length > 0 && (
                  <div>
                    <h4 className="font-semibold text-blue-900 mb-2">🎯 ATS Optimization Tips:</h4>
                    <ul className="space-y-2">
                      {analysis.ats_details.recommendations.map((rec: string, index: number) => (
                        <li key={index} className="flex items-start gap-2 text-gray-700">
                          <span className="text-blue-600 mt-1">•</span>
                          <span>{rec}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Keyword Analysis Details */}
                {analysis.ats_details?.keyword_analysis && (
                  <div className="bg-blue-50 rounded-lg p-4">
                    <h4 className="font-semibold text-gray-900 mb-2">🔑 Keyword Analysis:</h4>
                    <div className="grid grid-cols-2 gap-3 text-sm">
                      {analysis.ats_details.keyword_analysis.exact_matches > 0 && (
                        <div>
                          <span className="text-gray-600">Exact Matches:</span>
                          <span className="ml-2 font-semibold text-green-700">
                            {analysis.ats_details.keyword_analysis.exact_matches}
                          </span>
                        </div>
                      )}
                      {analysis.ats_details.keyword_analysis.action_verbs_count > 0 && (
                        <div>
                          <span className="text-gray-600">Action Verbs:</span>
                          <span className="ml-2 font-semibold text-blue-700">
                            {analysis.ats_details.keyword_analysis.action_verbs_count}
                          </span>
                        </div>
                      )}
                      {analysis.ats_details.keyword_analysis.quantified_achievements > 0 && (
                        <div>
                          <span className="text-gray-600">Quantified Achievements:</span>
                          <span className="ml-2 font-semibold text-purple-700">
                            {analysis.ats_details.keyword_analysis.quantified_achievements}
                          </span>
                        </div>
                      )}
                    </div>
                  </div>
                )}
                {/* Strengths */}
                {analysis.strengths && analysis.strengths.length > 0 && (
                  <div>
                    <h4 className="font-semibold text-green-900 mb-2">✨ Your Strengths:</h4>
                    <ul className="space-y-2">
                      {analysis.strengths.map((strength: string, index: number) => (
                        <li key={index} className="flex items-start gap-2 text-gray-700">
                          <span className="text-green-600 mt-1">✓</span>
                          <span>{strength}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Concerns */}
                {analysis.concerns && analysis.concerns.length > 0 && (
                  <div>
                    <h4 className="font-semibold text-yellow-900 mb-2">⚠️ Areas to Address:</h4>
                    <ul className="space-y-2">
                      {analysis.concerns.map((concern: string, index: number) => (
                        <li key={index} className="flex items-start gap-2 text-gray-700">
                          <span className="text-yellow-600 mt-1">•</span>
                          <span>{concern}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Overall Assessment */}
                {analysis.overall_assessment && (
                  <div className="bg-indigo-50 rounded-lg p-4">
                    <h4 className="font-semibold text-gray-900 mb-2">📊 Overall Assessment:</h4>
                    <p className="text-gray-700">{analysis.overall_assessment}</p>
                  </div>
                )}

                {/* Experience Match */}
                {analysis.experience_match && (
                  <div className="bg-blue-50 rounded-lg p-4">
                    <h4 className="font-semibold text-gray-900 mb-1">💼 Experience Match:</h4>
                    <p className="text-gray-700">{analysis.experience_match}</p>
                  </div>
                )}

                {/* Education Match */}
                {analysis.education_match && analysis.education_match !== 'Unknown' && (
                  <div className="bg-purple-50 rounded-lg p-4">
                    <h4 className="font-semibold text-gray-900 mb-1">🎓 Education Match:</h4>
                    <p className="text-gray-700">{analysis.education_match}</p>
                  </div>
                )}
              </div>
            </div>

            {/* COMPREHENSIVE ATS KEYWORD ANALYSIS */}
            {analysis.keyword_analysis && (
              <div className="space-y-6">
                {/* Score Improvement Potential */}
                <div className="bg-gradient-to-r from-emerald-50 to-green-50 rounded-lg border-2 border-emerald-300 p-6">
                  <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
                    <TrendingUp className="h-6 w-6 mr-2 text-emerald-600" />
                    ATS Score Improvement Potential
                  </h3>
                  <div className="grid grid-cols-3 gap-4 mb-4">
                    <div className="text-center bg-white rounded-lg p-4">
                      <div className="text-3xl font-bold text-gray-900">{analysis.keyword_analysis.current_ats_score || 0}%</div>
                      <div className="text-sm text-gray-600 font-semibold">Current Score</div>
                    </div>
                    <div className="text-center bg-white rounded-lg p-4">
                      <div className="text-3xl font-bold text-emerald-600">+{analysis.keyword_analysis.score_improvement_potential || 0}%</div>
                      <div className="text-sm text-gray-600 font-semibold">Potential Gain</div>
                    </div>
                    <div className="text-center bg-white rounded-lg p-4">
                      <div className="text-3xl font-bold text-green-600">{analysis.keyword_analysis.estimated_score_after_fixes || 0}%</div>
                      <div className="text-sm text-gray-600 font-semibold">After Fixes</div>
                    </div>
                  </div>
                </div>

                {/* Priority Actions */}
                {analysis.keyword_analysis.gap_analysis?.priority_actions && (
                  <div className="bg-gradient-to-r from-red-50 to-orange-50 rounded-lg border-2 border-red-300 p-6">
                    <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
                      <AlertCircle className="h-6 w-6 mr-2 text-red-600" />
                      🚨 Priority Actions (Do These First!)
                    </h3>
                    <div className="space-y-2">
                      {analysis.keyword_analysis.gap_analysis.priority_actions.map((action: string, index: number) => (
                        <div key={index} className="bg-white rounded-lg p-3 border border-red-200">
                          <p className="text-sm text-gray-800">{action}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Missing Critical Keywords */}
                {analysis.keyword_analysis.gap_analysis?.missing_critical && analysis.keyword_analysis.gap_analysis.missing_critical.length > 0 && (
                  <div className="bg-white rounded-lg border-2 border-yellow-300 p-6">
                    <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center">
                      <AlertCircle className="h-5 w-5 mr-2 text-yellow-600" />
                      ❌ Missing Critical Keywords
                    </h3>
                    <div className="space-y-4">
                      {analysis.keyword_analysis.gap_analysis.missing_critical.map((item: any, index: number) => (
                        <div key={index} className="border border-yellow-200 rounded-lg p-4 bg-yellow-50">
                          <div className="flex items-start justify-between mb-2">
                            <div className="font-semibold text-gray-900 flex items-center gap-2">
                              <span className="px-2 py-1 bg-yellow-200 text-yellow-900 rounded text-xs font-bold">
                                IMPORTANCE: {item.importance}/100
                              </span>
                              <span>{item.keyword}</span>
                            </div>
                            <span className="text-xs bg-red-500 text-white px-2 py-1 rounded">{item.impact}</span>
                          </div>
                          <p className="text-sm text-gray-600 mb-2"><strong>Why missing:</strong> {item.why_missing}</p>
                          <div className="bg-white rounded p-3 border border-yellow-300">
                            <p className="text-xs text-gray-500 mb-1 font-semibold">✅ RECOMMENDATION:</p>
                            <p className="text-sm text-gray-800">{item.recommendation}</p>
                            <p className="text-xs text-gray-500 mt-2"><strong>Where:</strong> {item.where_to_add}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Strategic Improvements */}
                {analysis.keyword_analysis.gap_analysis?.strategic_improvements && analysis.keyword_analysis.gap_analysis.strategic_improvements.length > 0 && (
                  <div className="bg-white rounded-lg border-2 border-blue-300 p-6">
                    <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center">
                      <Sparkles className="h-5 w-5 mr-2 text-blue-600" />
                      💡 Strategic Section-by-Section Improvements
                    </h3>
                    <div className="space-y-4">
                      {analysis.keyword_analysis.gap_analysis.strategic_improvements.map((item: any, index: number) => (
                        <div key={index} className="border border-blue-200 rounded-lg p-4 bg-blue-50">
                          <div className="flex items-start justify-between mb-2">
                            <div className="font-semibold text-blue-900">{item.section}</div>
                            <span className="text-xs bg-blue-600 text-white px-2 py-1 rounded">{item.impact}</span>
                          </div>
                          <div className="mb-2">
                            <span className="text-xs text-red-600 font-semibold">❌ Current Issue:</span>
                            <p className="text-sm text-gray-700 ml-4">{item.current_issue}</p>
                          </div>
                          <div className="mb-2">
                            <span className="text-xs text-green-600 font-semibold">✅ Fix:</span>
                            <p className="text-sm text-gray-700 ml-4">{item.fix}</p>
                          </div>
                          {item.example && (
                            <div className="bg-white rounded p-3 border border-blue-300 mt-2">
                              <p className="text-xs text-gray-500 mb-1 font-semibold">📝 EXAMPLE:</p>
                              <p className="text-sm text-gray-800 italic">{item.example}</p>
                              <button 
                                onClick={() => {
                                  navigator.clipboard.writeText(item.example)
                                  alert('✅ Example copied to clipboard!')
                                }}
                                className="text-xs text-blue-600 hover:text-blue-800 font-medium mt-2"
                              >
                                📋 Copy Example
                              </button>
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* JD-Resume Comparison Table */}
                {analysis.keyword_analysis.comparison_table && analysis.keyword_analysis.comparison_table.length > 0 && (
                  <div className="bg-white rounded-lg border border-gray-200 p-6">
                    <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center">
                      <CheckCircle className="h-5 w-5 mr-2 text-gray-600" />
                      📊 JD Requirements vs Your Resume - Side by Side
                    </h3>
                    <div className="overflow-x-auto">
                      <table className="w-full text-sm">
                        <thead className="bg-gray-100">
                          <tr>
                            <th className="px-4 py-3 text-left font-semibold text-gray-700">Importance</th>
                            <th className="px-4 py-3 text-left font-semibold text-gray-700">JD Requirement</th>
                            <th className="px-4 py-3 text-left font-semibold text-gray-700">Category</th>
                            <th className="px-4 py-3 text-left font-semibold text-gray-700">Resume Status</th>
                            <th className="px-4 py-3 text-left font-semibold text-gray-700">Action Needed</th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-200">
                          {analysis.keyword_analysis.comparison_table.slice(0, 15).map((row: any, index: number) => (
                            <tr key={index} className="hover:bg-gray-50">
                              <td className="px-4 py-3">
                                <span className={`px-2 py-1 rounded text-xs font-bold ${
                                  row.importance >= 90 ? 'bg-red-100 text-red-700' :
                                  row.importance >= 75 ? 'bg-orange-100 text-orange-700' :
                                  'bg-yellow-100 text-yellow-700'
                                }`}>
                                  {row.importance}
                                </span>
                              </td>
                              <td className="px-4 py-3 font-medium">{row.jd_requirement}</td>
                              <td className="px-4 py-3 text-gray-600 text-xs">{row.category.replace(/_/g, ' ')}</td>
                              <td className="px-4 py-3">{row.resume_status}</td>
                              <td className="px-4 py-3 text-xs text-gray-600">{row.action_needed}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}

                {/* Categorized Keywords from JD */}
                {analysis.keyword_analysis.categorized_keywords && (
                  <div className="bg-white rounded-lg border border-gray-200 p-6">
                    <h3 className="text-lg font-bold text-gray-900 mb-4">🎯 All ATS Keywords Extracted from Job Description</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {Object.entries(analysis.keyword_analysis.categorized_keywords).map(([category, keywords]: [string, any]) => {
                        if (category === 'ats_critical_phrases' || !Array.isArray(keywords) || keywords.length === 0) return null
                        return (
                          <div key={category} className="bg-gray-50 rounded-lg p-4">
                            <h4 className="font-semibold text-gray-900 mb-3 capitalize">{category.replace(/_/g, ' ')}</h4>
                            <div className="space-y-2">
                              {keywords.slice(0, 5).map((kw: any, idx: number) => (
                                <div key={idx} className="flex items-start gap-2">
                                  <span className={`px-2 py-0.5 rounded text-xs font-bold ${
                                    kw.importance >= 90 ? 'bg-red-100 text-red-700' :
                                    kw.importance >= 80 ? 'bg-orange-100 text-orange-700' :
                                    'bg-blue-100 text-blue-700'
                                  }`}>
                                    {kw.importance}
                                  </span>
                                  <div>
                                    <div className="text-sm font-medium text-gray-900">{kw.keyword}</div>
                                    <div className="text-xs text-gray-500">{kw.context}</div>
                                  </div>
                                </div>
                              ))}
                            </div>
                          </div>
                        )
                      })}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* AI-Generated Resume Suggestions - GAME CHANGER! */}
            {(analysis.missing_skills?.length > 0 || analysis.concerns?.length > 0) && (
              <div className="bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg border-2 border-purple-300 p-6">
                <h3 className="flex items-center text-xl font-bold text-gray-900 mb-4">
                  <Sparkles className="h-6 w-6 mr-2 text-purple-600" />
                  AI Resume Optimization Suggestions
                  <span className="ml-2 text-xs bg-purple-600 text-white px-2 py-1 rounded-full">GAME CHANGER</span>
                </h3>
                <p className="text-sm text-gray-600 mb-4">
                  Based on your resume and the job description, here are AI-generated suggestions to improve your match score:
                </p>

                {/* Missing Keywords Summary */}
                {analysis.missing_skills && analysis.missing_skills.length > 0 && (
                  <div className="bg-white rounded-lg p-4 mb-4">
                    <h4 className="font-semibold text-purple-900 mb-3">🎯 Keywords to Add ({analysis.missing_skills.length}):</h4>
                    <div className="bg-purple-50 rounded p-3 mb-3">
                      <p className="text-sm text-gray-700 font-medium mb-2">Add these keywords naturally to your resume:</p>
                      <div className="flex flex-wrap gap-2">
                        {analysis.missing_skills.slice(0, 10).map((skill: string, index: number) => (
                          <span key={index} className="px-2 py-1 bg-purple-100 text-purple-700 rounded text-xs font-medium">
                            {skill}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                )}

                {/* AI-Generated Experience Bullets */}
                <div className="bg-white rounded-lg p-4">
                  <h4 className="font-semibold text-purple-900 mb-3">✨ Suggested Experience Bullets:</h4>
                  <p className="text-xs text-gray-500 mb-3">
                    Add these AI-generated bullet points to your relevant work experience sections:
                  </p>
                  <div className="space-y-3">
                    {analysis.missing_skills && analysis.missing_skills.slice(0, 5).map((skill: string, index: number) => (
                      <div key={index} className="bg-gradient-to-r from-purple-50 to-white rounded-lg p-3 border border-purple-200">
                        <div className="flex items-start gap-2">
                          <span className="text-purple-600 font-bold mt-0.5">•</span>
                          <div className="flex-1">
                            <p className="text-sm text-gray-800 font-medium">
                              {`Utilized ${skill} to develop and implement solutions that improved system performance and efficiency, resulting in measurable business impact`}
                            </p>
                            <div className="mt-2 flex items-center gap-2">
                              <button 
                                onClick={() => {
                                  navigator.clipboard.writeText(`• Utilized ${skill} to develop and implement solutions that improved system performance and efficiency, resulting in measurable business impact`)
                                  alert('✅ Copied to clipboard!')
                                }}
                                className="text-xs text-purple-600 hover:text-purple-800 font-medium"
                              >
                                📋 Copy
                              </button>
                              <span className="text-xs text-gray-500">
                                Keywords: <span className="font-semibold text-purple-700">{skill}</span>
                              </span>
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                  <div className="mt-4 p-3 bg-yellow-50 rounded border border-yellow-200">
                    <p className="text-xs text-yellow-800">
                      <span className="font-semibold">💡 Pro Tip:</span> Customize these bullets with specific numbers, results, and details from your actual experience. 
                      Only add bullets that reflect real work you've done!
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* Score Explanation Box - Moved to Bottom */}
            <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border-2 border-blue-300 p-6">
              <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center">
                <TrendingUp className="h-5 w-5 mr-2 text-blue-600" />
                Understanding Your Scores
              </h3>
              <div className="grid grid-cols-2 gap-4 text-sm mb-4">
                <div className="text-center bg-white rounded-lg p-4">
                  <div className="text-3xl font-bold text-blue-600">{analysis.match_score || 0}%</div>
                  <div className="text-gray-600 font-semibold">Match Score</div>
                </div>
                <div className="text-center bg-white rounded-lg p-4">
                  <div className="text-3xl font-bold text-green-600">{analysis.ats_score || 0}%</div>
                  <div className="text-gray-600 font-semibold">ATS Score</div>
                </div>
              </div>
              <div className="mb-4 text-center p-3 bg-white rounded-lg border border-blue-200">
                <span className="text-xs text-gray-500">Difference: </span>
                <span className={`text-lg font-semibold ${
                  Math.abs((analysis.match_score || 0) - (analysis.ats_score || 0)) < 10 
                    ? 'text-green-600' 
                    : 'text-amber-600'
                }`}>
                  {Math.abs((analysis.match_score || 0) - (analysis.ats_score || 0)).toFixed(1)}%
                </span>
                <span className="text-sm text-gray-500 ml-1">
                  {Math.abs((analysis.match_score || 0) - (analysis.ats_score || 0)) < 10 
                    ? '✓ Well aligned' 
                    : '⚠ Gap detected'}
                </span>
              </div>
              <div className="bg-white rounded-lg p-4 text-sm text-gray-700 space-y-3">
                <div>
                  <div className="font-semibold text-blue-600 mb-1">🔵 Match Score ({analysis.match_score || 0}%)</div>
                  <div className="text-xs text-gray-600 ml-4">Your qualifications vs job requirements - measures skills, experience, education alignment</div>
                </div>
                <div>
                  <div className="font-semibold text-green-600 mb-1">🟢 ATS Score ({analysis.ats_score || 0}%)</div>
                  <div className="text-xs text-gray-600 ml-4">Resume optimization for tracking systems - evaluates keywords, formatting, structure (43 checks)</div>
                </div>
                <div>
                  <div className="font-semibold text-purple-600 mb-1">🟣 What the Difference Means</div>
                  <div className="text-xs text-gray-600 ml-4">
                    {Math.abs((analysis.match_score || 0) - (analysis.ats_score || 0)) < 10 
                      ? '👍 Small gap = You\'re qualified AND your resume shows it well'
                      : (analysis.match_score > analysis.ats_score 
                          ? '⚠️ You\'re qualified but resume needs optimization (improve keywords/formatting)'
                          : '⚠️ Resume looks good but may be missing key qualifications or experience')}
                  </div>
                </div>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex flex-wrap gap-4 justify-center">
              <button 
                onClick={() => window.print()}
                className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
              >
                Print Analysis Report
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
