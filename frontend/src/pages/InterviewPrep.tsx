import { useState, useEffect } from 'react'
import { useQuery } from '@tanstack/react-query'
import { applicationsApi, analysisApi } from '../lib/api'
import { BookOpen, CheckCircle2, Circle, MessageSquare, Code, Building, Sparkles, ChevronRight } from 'lucide-react'

interface InterviewQuestion {
  category: string
  question: string
  answer?: string
  prepared: boolean
  notes: string
}

export default function InterviewPrep() {
  const [selectedJobId, setSelectedJobId] = useState<number | null>(null)
  const [questions, setQuestions] = useState<InterviewQuestion[]>([])
  const [expandedQuestion, setExpandedQuestion] = useState<number | null>(null)

  // Fetch applications with "interview" status
  const { data: applications, isLoading } = useQuery({
    queryKey: ['applications', 'interview'],
    queryFn: async () => {
      const response = await applicationsApi.list('interview')
      return response.data
    },
  })

  // Fetch interview prep for selected job
  const { data: interviewData } = useQuery({
    queryKey: ['interview-prep', selectedJobId],
    queryFn: async () => {
      if (!selectedJobId) return null
      const response = await analysisApi.getInterviewPrep(selectedJobId)
      return response.data
    },
    enabled: !!selectedJobId,
  })

  // Set first job as selected by default
  useEffect(() => {
    if (applications && applications.length > 0 && !selectedJobId) {
      setSelectedJobId(applications[0].job_id)
    }
  }, [applications, selectedJobId])

  // Parse interview questions from analysis
  useEffect(() => {
    if (interviewData?.interview_questions) {
      const parsedQuestions: InterviewQuestion[] = interviewData.interview_questions.map((q: string) => {
        // Try to categorize questions
        let category = 'General'
        if (q.toLowerCase().includes('technical') || q.toLowerCase().includes('code') || q.toLowerCase().includes('algorithm')) {
          category = 'Technical'
        } else if (q.toLowerCase().includes('team') || q.toLowerCase().includes('conflict') || q.toLowerCase().includes('experience')) {
          category = 'Behavioral'
        } else if (q.toLowerCase().includes('company') || q.toLowerCase().includes('why') || q.toLowerCase().includes('culture')) {
          category = 'Company-Specific'
        }
        
        return {
          category,
          question: q,
          prepared: false,
          notes: '',
        }
      })
      setQuestions(parsedQuestions)
    }
  }, [interviewData])

  const togglePrepared = (index: number) => {
    setQuestions(prev => prev.map((q, i) => 
      i === index ? { ...q, prepared: !q.prepared } : q
    ))
  }

  const updateNotes = (index: number, notes: string) => {
    setQuestions(prev => prev.map((q, i) => 
      i === index ? { ...q, notes } : q
    ))
  }

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'Technical':
        return <Code className="h-5 w-5 text-blue-600" />
      case 'Behavioral':
        return <MessageSquare className="h-5 w-5 text-purple-600" />
      case 'Company-Specific':
        return <Building className="h-5 w-5 text-green-600" />
      default:
        return <BookOpen className="h-5 w-5 text-gray-600" />
    }
  }

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'Technical':
        return 'bg-blue-50 border-blue-200 text-blue-800'
      case 'Behavioral':
        return 'bg-purple-50 border-purple-200 text-purple-800'
      case 'Company-Specific':
        return 'bg-green-50 border-green-200 text-green-800'
      default:
        return 'bg-gray-50 border-gray-200 text-gray-800'
    }
  }

  const selectedApplication = applications?.find((app: any) => app.job_id === selectedJobId)
  const technicalQuestions = questions.filter(q => q.category === 'Technical')
  const behavioralQuestions = questions.filter(q => q.category === 'Behavioral')
  const companyQuestions = questions.filter(q => q.category === 'Company-Specific')
  const generalQuestions = questions.filter(q => q.category === 'General')

  const preparedCount = questions.filter(q => q.prepared).length
  const totalCount = questions.length

  return (
    <div className="min-h-screen">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent flex items-center gap-3">
          <Sparkles className="h-10 w-10 text-purple-600" />
          Interview Preparation
        </h1>
        <p className="text-gray-600 mt-2 text-lg">
          AI-powered interview prep based on job descriptions
        </p>
      </div>

      {isLoading ? (
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          <p className="text-gray-600 mt-4">Loading interviews...</p>
        </div>
      ) : !applications || applications.length === 0 ? (
        <div className="bg-white rounded-xl shadow-lg p-12 text-center">
          <BookOpen className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 mb-2">No Interview Scheduled</h2>
          <p className="text-gray-600">
            When you set an application status to "Interview", it will appear here with AI-generated interview prep materials.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Left: Job List */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-xl shadow-lg p-4 sticky top-4">
              <h2 className="text-lg font-bold text-gray-900 mb-4">Upcoming Interviews</h2>
              <div className="space-y-2">
                {applications.map((app: any) => (
                  <button
                    key={app.id}
                    onClick={() => setSelectedJobId(app.job_id)}
                    className={`w-full text-left p-4 rounded-lg border-2 transition-all ${
                      selectedJobId === app.job_id
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                    }`}
                  >
                    <div className="font-semibold text-gray-900 text-sm mb-1 line-clamp-2">
                      {app.job?.title || 'Job Title'}
                    </div>
                    <div className="text-xs text-gray-600 mb-2">
                      {app.job?.company || 'Company'}
                    </div>
                    {app.interview_date && (
                      <div className="text-xs text-blue-600 font-medium">
                        📅 {new Date(app.interview_date).toLocaleDateString()}
                      </div>
                    )}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Right: Interview Prep Kit */}
          <div className="lg:col-span-3">
            <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
              <div className="flex items-start justify-between mb-6">
                <div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-1">
                    {selectedApplication?.job?.title || 'Job Title'}
                  </h2>
                  <p className="text-gray-600">
                    {selectedApplication?.job?.company || 'Company'} • {selectedApplication?.job?.location || 'Location'}
                  </p>
                </div>
                <div className="text-right">
                  <div className="text-3xl font-bold text-blue-600">{preparedCount}/{totalCount}</div>
                  <div className="text-sm text-gray-600">Questions Prepared</div>
                </div>
              </div>

              {/* Progress Bar */}
              <div className="w-full bg-gray-200 rounded-full h-3 mb-6">
                <div
                  className="bg-gradient-to-r from-blue-600 to-purple-600 h-3 rounded-full transition-all"
                  style={{ width: `${totalCount > 0 ? (preparedCount / totalCount) * 100 : 0}%` }}
                ></div>
              </div>
            </div>

            {/* Question Categories */}
            <div className="space-y-6">
              {/* Technical Questions */}
              {technicalQuestions.length > 0 && (
                <div className="bg-white rounded-xl shadow-lg p-6">
                  <div className="flex items-center mb-4">
                    <Code className="h-6 w-6 text-blue-600 mr-3" />
                    <h3 className="text-xl font-bold text-gray-900">
                      Technical Questions ({technicalQuestions.length})
                    </h3>
                  </div>
                  <div className="space-y-3">
                    {technicalQuestions.map((q, idx) => {
                      const globalIdx = questions.indexOf(q)
                      return (
                        <div key={globalIdx} className="border border-gray-200 rounded-lg">
                          <div className="p-4">
                            <div className="flex items-start justify-between">
                              <div className="flex-1">
                                <button
                                  onClick={() => setExpandedQuestion(expandedQuestion === globalIdx ? null : globalIdx)}
                                  className="text-left w-full"
                                >
                                  <p className="font-medium text-gray-900 hover:text-blue-600">
                                    {idx + 1}. {q.question}
                                  </p>
                                </button>
                              </div>
                              <button
                                onClick={() => togglePrepared(globalIdx)}
                                className="ml-4 flex-shrink-0"
                              >
                                {q.prepared ? (
                                  <CheckCircle2 className="h-6 w-6 text-green-600" />
                                ) : (
                                  <Circle className="h-6 w-6 text-gray-400" />
                                )}
                              </button>
                            </div>
                            {expandedQuestion === globalIdx && (
                              <div className="mt-4 pt-4 border-t border-gray-200">
                                <label className="block text-sm font-medium text-gray-700 mb-2">
                                  Your Notes:
                                </label>
                                <textarea
                                  value={q.notes}
                                  onChange={(e) => updateNotes(globalIdx, e.target.value)}
                                  placeholder="Add your preparation notes, key points, or answer outline..."
                                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                                  rows={4}
                                />
                              </div>
                            )}
                          </div>
                        </div>
                      )
                    })}
                  </div>
                </div>
              )}

              {/* Behavioral Questions */}
              {behavioralQuestions.length > 0 && (
                <div className="bg-white rounded-xl shadow-lg p-6">
                  <div className="flex items-center mb-4">
                    <MessageSquare className="h-6 w-6 text-purple-600 mr-3" />
                    <h3 className="text-xl font-bold text-gray-900">
                      Behavioral Questions ({behavioralQuestions.length})
                    </h3>
                  </div>
                  <div className="space-y-3">
                    {behavioralQuestions.map((q, idx) => {
                      const globalIdx = questions.indexOf(q)
                      return (
                        <div key={globalIdx} className="border border-gray-200 rounded-lg">
                          <div className="p-4">
                            <div className="flex items-start justify-between">
                              <div className="flex-1">
                                <button
                                  onClick={() => setExpandedQuestion(expandedQuestion === globalIdx ? null : globalIdx)}
                                  className="text-left w-full"
                                >
                                  <p className="font-medium text-gray-900 hover:text-purple-600">
                                    {idx + 1}. {q.question}
                                  </p>
                                </button>
                              </div>
                              <button
                                onClick={() => togglePrepared(globalIdx)}
                                className="ml-4 flex-shrink-0"
                              >
                                {q.prepared ? (
                                  <CheckCircle2 className="h-6 w-6 text-green-600" />
                                ) : (
                                  <Circle className="h-6 w-6 text-gray-400" />
                                )}
                              </button>
                            </div>
                            {expandedQuestion === globalIdx && (
                              <div className="mt-4 pt-4 border-t border-gray-200">
                                <label className="block text-sm font-medium text-gray-700 mb-2">
                                  Your Notes (Use STAR method):
                                </label>
                                <textarea
                                  value={q.notes}
                                  onChange={(e) => updateNotes(globalIdx, e.target.value)}
                                  placeholder="Situation: ...\nTask: ...\nAction: ...\nResult: ..."
                                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                                  rows={6}
                                />
                              </div>
                            )}
                          </div>
                        </div>
                      )
                    })}
                  </div>
                </div>
              )}

              {/* Company-Specific Questions */}
              {companyQuestions.length > 0 && (
                <div className="bg-white rounded-xl shadow-lg p-6">
                  <div className="flex items-center mb-4">
                    <Building className="h-6 w-6 text-green-600 mr-3" />
                    <h3 className="text-xl font-bold text-gray-900">
                      Company-Specific Questions ({companyQuestions.length})
                    </h3>
                  </div>
                  <div className="space-y-3">
                    {companyQuestions.map((q, idx) => {
                      const globalIdx = questions.indexOf(q)
                      return (
                        <div key={globalIdx} className="border border-gray-200 rounded-lg">
                          <div className="p-4">
                            <div className="flex items-start justify-between">
                              <div className="flex-1">
                                <button
                                  onClick={() => setExpandedQuestion(expandedQuestion === globalIdx ? null : globalIdx)}
                                  className="text-left w-full"
                                >
                                  <p className="font-medium text-gray-900 hover:text-green-600">
                                    {idx + 1}. {q.question}
                                  </p>
                                </button>
                              </div>
                              <button
                                onClick={() => togglePrepared(globalIdx)}
                                className="ml-4 flex-shrink-0"
                              >
                                {q.prepared ? (
                                  <CheckCircle2 className="h-6 w-6 text-green-600" />
                                ) : (
                                  <Circle className="h-6 w-6 text-gray-400" />
                                )}
                              </button>
                            </div>
                            {expandedQuestion === globalIdx && (
                              <div className="mt-4 pt-4 border-t border-gray-200">
                                <label className="block text-sm font-medium text-gray-700 mb-2">
                                  Your Research & Notes:
                                </label>
                                <textarea
                                  value={q.notes}
                                  onChange={(e) => updateNotes(globalIdx, e.target.value)}
                                  placeholder="Add research about the company, their products, culture, recent news..."
                                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                                  rows={4}
                                />
                              </div>
                            )}
                          </div>
                        </div>
                      )
                    })}
                  </div>
                </div>
              )}

              {/* General Questions */}
              {generalQuestions.length > 0 && (
                <div className="bg-white rounded-xl shadow-lg p-6">
                  <div className="flex items-center mb-4">
                    <BookOpen className="h-6 w-6 text-gray-600 mr-3" />
                    <h3 className="text-xl font-bold text-gray-900">
                      General Questions ({generalQuestions.length})
                    </h3>
                  </div>
                  <div className="space-y-3">
                    {generalQuestions.map((q, idx) => {
                      const globalIdx = questions.indexOf(q)
                      return (
                        <div key={globalIdx} className="border border-gray-200 rounded-lg">
                          <div className="p-4">
                            <div className="flex items-start justify-between">
                              <div className="flex-1">
                                <button
                                  onClick={() => setExpandedQuestion(expandedQuestion === globalIdx ? null : globalIdx)}
                                  className="text-left w-full"
                                >
                                  <p className="font-medium text-gray-900">
                                    {idx + 1}. {q.question}
                                  </p>
                                </button>
                              </div>
                              <button
                                onClick={() => togglePrepared(globalIdx)}
                                className="ml-4 flex-shrink-0"
                              >
                                {q.prepared ? (
                                  <CheckCircle2 className="h-6 w-6 text-green-600" />
                                ) : (
                                  <Circle className="h-6 w-6 text-gray-400" />
                                )}
                              </button>
                            </div>
                            {expandedQuestion === globalIdx && (
                              <div className="mt-4 pt-4 border-t border-gray-200">
                                <label className="block text-sm font-medium text-gray-700 mb-2">
                                  Your Notes:
                                </label>
                                <textarea
                                  value={q.notes}
                                  onChange={(e) => updateNotes(globalIdx, e.target.value)}
                                  placeholder="Add your preparation notes..."
                                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                                  rows={4}
                                />
                              </div>
                            )}
                          </div>
                        </div>
                      )
                    })}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
