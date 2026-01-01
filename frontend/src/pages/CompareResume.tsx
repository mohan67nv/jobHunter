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
      alert('✅ PDF parsed successfully!')
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
            
            {/* PDF Upload */}
            <div className="mb-4 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border-2 border-dashed border-blue-300">
              <label className="flex items-center justify-center gap-2 cursor-pointer">
                <Upload className="h-5 w-5 text-blue-600" />
                <span className="text-blue-600 font-semibold">Upload PDF Resume</span>
                <input 
                  type="file" 
                  accept="application/pdf" 
                  onChange={handlePdfUpload}
                  className="hidden"
                />
              </label>
              {uploadPdfMutation.isPending && (
                <div className="mt-2 text-center text-sm text-blue-600">
                  <div className="inline-block animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-2"></div>
                  Parsing PDF with GPT-5-mini...
                </div>
              )}
              {pdfFile && !uploadPdfMutation.isPending && (
                <div className="mt-2 text-center text-sm text-green-600">
                  ✅ {pdfFile.name}
                </div>
              )}
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
              <button 
                onClick={handleClearResume}
                className="px-4 py-2 text-sm text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Clear
              </button>
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
                <div className="flex justify-between items-center">
                  <span className="text-gray-700">Overall fit</span>
                  <span className="font-semibold text-indigo-600">10%</span>
                </div>
              </div>
            </div>
            <div className="bg-white rounded-lg p-4">
              <h4 className="font-semibold text-gray-900 mb-3">ATS Score (42 checks):</h4>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between items-center">
                  <span className="text-gray-700">Keywords analysis</span>
                  <span className="font-semibold text-blue-600">40%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-700">Structure & content</span>
                  <span className="font-semibold text-green-600">20%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-700">Fonts & formatting</span>
                  <span className="font-semibold text-purple-600">15%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-700">Layout & page setup</span>
                  <span className="font-semibold text-indigo-600">25%</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Analyze Button */}
        <div className="text-center mb-8">
          <button
            onClick={handleAnalyze}
            disabled={analyzeMutation.isPending || !resumeText || !jdText}
            className="inline-flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed text-lg font-semibold shadow-lg"
          >
            <Sparkles className="h-6 w-6" />
            {analyzeMutation.isPending ? 'Analyzing with AI...' : 'Analyze with AI'}
          </button>
          <p className="text-sm text-gray-500 mt-2">
            Powered by GPT-5 Mini, Gemini 2.0 Flash & Perplexity AI
          </p>
        </div>

        {/* Results */}
        {analysis && (
          <div className="space-y-6 animate-fadeIn">
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
