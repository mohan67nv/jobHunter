import { useState, useEffect } from 'react'
import { useQuery } from '@tanstack/react-query'
import { applicationsApi, analysisApi } from '../lib/api'
import { 
  BookOpen, CheckCircle2, Building, Code, MessageSquare, 
  Sparkles, ChevronDown, ChevronUp, Briefcase, TrendingUp,
  Calendar, MapPin, Users, Globe, Award, Target
} from 'lucide-react'

interface CompanyInfo {
  overview: {
    industry: string
    size: string
    headquarters: string
    founded: string
    description: string
    mission: string
    products_services: string[]
  }
  recent_news: Array<{
    title: string
    date: string
    summary: string
    relevance: string
  }>
  culture: {
    values: string[]
    work_environment: string
    work_life_balance: string
    diversity_inclusion: string
    employee_reviews_summary: string
  }
  company_qa: Array<{
    question: string
    answer: string
    talking_points: string[]
    reference: string
  }>
  questions_to_ask: Array<{
    question: string
    why_ask: string
  }>
}

interface TechnicalQA {
  question: string
  answer: string
  difficulty: string
  category: string
  source?: string
  project_name?: string
  how_to_explain?: string
  what_to_emphasize?: string[]
  expected_questions?: string[]
  impressive_metrics?: string[]
  key_points: string[]
  interview_tip?: string
  follow_ups?: string[]
}

interface BehavioralQA {
  question: string
  answer: string
  situation: string
  task: string
  action: string
  result: string
  competency: string
  tips: string[]
}

interface HRQA {
  question: string
  answer: string
  category: string
  dos: string[]
  donts: string[]
  example_answer: string
}

export default function InterviewPrep() {
  const [selectedJobId, setSelectedJobId] = useState<number | null>(null)
  const [activeTab, setActiveTab] = useState<'company' | 'technical' | 'behavioral' | 'hr'>('company')
  const [expandedItems, setExpandedItems] = useState<Set<number>>(new Set())

  // Fetch applications with interview-related statuses
  const { data: applications, isLoading } = useQuery({
    queryKey: ['applications', 'interview'],
    queryFn: async () => {
      const response = await applicationsApi.list('interview')
      return response.data
    },
  })

  // Fetch comprehensive interview prep
  const { data: interviewData, isLoading: isLoadingPrep } = useQuery({
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

  const toggleExpanded = (index: number) => {
    setExpandedItems(prev => {
      const newSet = new Set(prev)
      if (newSet.has(index)) {
        newSet.delete(index)
      } else {
        newSet.add(index)
      }
      return newSet
    })
  }

  const selectedApplication = applications?.find((app: any) => app.job_id === selectedJobId)
  const companyInfo: CompanyInfo | undefined = interviewData?.company_info
  const technicalQA: TechnicalQA[] = interviewData?.technical_qa || []
  const behavioralQA: BehavioralQA[] = interviewData?.behavioral_qa || []
  const hrQA: HRQA[] = interviewData?.hr_qa || []

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty.toLowerCase()) {
      case 'easy': return 'bg-green-100 text-green-800'
      case 'medium': return 'bg-yellow-100 text-yellow-800'
      case 'hard': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getSourceBadge = (source?: string) => {
    switch (source) {
      case 'employee_experience':
        return { text: 'Employee Experience', color: 'bg-emerald-100 text-emerald-800', icon: '💼' }
      case 'job_requirements':
        return { text: 'Job Requirements', color: 'bg-blue-100 text-blue-800', icon: '📋' }
      case 'resume_project':
        return { text: 'Your Project', color: 'bg-purple-100 text-purple-800', icon: '🎯' }
      default:
        return null
    }
  }

  return (
    <div className="min-h-screen">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent flex items-center gap-3">
          <Sparkles className="h-10 w-10 text-purple-600" />
          Interview Preparation
        </h1>
        <p className="text-gray-600 mt-2 text-lg">
          Comprehensive interview prep with company research and Q&A powered by AI
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
          <h2 className="text-2xl font-bold text-gray-900 mb-2">No Interviews Scheduled</h2>
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
                    className={`w-full text-left p-3 rounded-lg border-2 transition-all ${
                      selectedJobId === app.job_id
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                  >
                    <div className="font-semibold text-gray-900 truncate">
                      {app.job?.title || 'Job Title'}
                    </div>
                    <div className="text-sm text-gray-600 truncate">
                      {app.job?.company || 'Company'}
                    </div>
                    {app.interview_date && (
                      <div className="text-xs text-blue-600 mt-1 flex items-center gap-1">
                        <Calendar className="h-3 w-3" />
                        {new Date(app.interview_date).toLocaleDateString()}
                      </div>
                    )}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Right: Interview Prep Content */}
          <div className="lg:col-span-3">
            {selectedApplication && (
              <>
                {/* Job Header */}
                <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl shadow-lg p-6 text-white mb-6">
                  <h2 className="text-2xl font-bold mb-2">{selectedApplication.job?.title}</h2>
                  <div className="flex items-center gap-4 text-blue-100">
                    <div className="flex items-center gap-2">
                      <Building className="h-4 w-4" />
                      {selectedApplication.job?.company}
                    </div>
                    {selectedApplication.job?.location && (
                      <div className="flex items-center gap-2">
                        <MapPin className="h-4 w-4" />
                        {selectedApplication.job.location}
                      </div>
                    )}
                  </div>
                </div>

                {/* Tabs */}
                <div className="bg-white rounded-xl shadow-lg mb-6">
                  <div className="border-b border-gray-200">
                    <div className="flex overflow-x-auto">
                      <button
                        onClick={() => setActiveTab('company')}
                        className={`flex items-center gap-2 px-6 py-4 border-b-2 font-semibold transition-colors ${
                          activeTab === 'company'
                            ? 'border-blue-600 text-blue-600'
                            : 'border-transparent text-gray-600 hover:text-gray-900'
                        }`}
                      >
                        <Building className="h-5 w-5" />
                        Company
                      </button>
                      <button
                        onClick={() => setActiveTab('technical')}
                        className={`flex items-center gap-2 px-6 py-4 border-b-2 font-semibold transition-colors ${
                          activeTab === 'technical'
                            ? 'border-blue-600 text-blue-600'
                            : 'border-transparent text-gray-600 hover:text-gray-900'
                        }`}
                      >
                        <Code className="h-5 w-5" />
                        Technical ({technicalQA.length})
                      </button>
                      <button
                        onClick={() => setActiveTab('behavioral')}
                        className={`flex items-center gap-2 px-6 py-4 border-b-2 font-semibold transition-colors ${
                          activeTab === 'behavioral'
                            ? 'border-blue-600 text-blue-600'
                            : 'border-transparent text-gray-600 hover:text-gray-900'
                        }`}
                      >
                        <MessageSquare className="h-5 w-5" />
                        Behavioral ({behavioralQA.length})
                      </button>
                      <button
                        onClick={() => setActiveTab('hr')}
                        className={`flex items-center gap-2 px-6 py-4 border-b-2 font-semibold transition-colors ${
                          activeTab === 'hr'
                            ? 'border-blue-600 text-blue-600'
                            : 'border-transparent text-gray-600 hover:text-gray-900'
                        }`}
                      >
                        <Users className="h-5 w-5" />
                        HR Round ({hrQA.length})
                      </button>
                    </div>
                  </div>

                  {/* Tab Content */}
                  <div className="p-6">
                    {isLoadingPrep ? (
                      <div className="text-center py-12">
                        <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
                        <p className="text-gray-600 mt-4">Generating comprehensive interview prep with AI...</p>
                      </div>
                    ) : (
                      <>
                        {/* Company Tab */}
                        {activeTab === 'company' && companyInfo && (
                          <div className="space-y-6">
                            {/* Company Overview */}
                            <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg p-6">
                              <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                                <Building className="h-6 w-6 text-blue-600" />
                                Company Overview
                              </h3>
                              <div className="grid grid-cols-2 gap-4 mb-4">
                                <div>
                                  <div className="text-sm text-gray-600">Industry</div>
                                  <div className="font-semibold text-gray-900">{companyInfo.overview.industry}</div>
                                </div>
                                <div>
                                  <div className="text-sm text-gray-600">Size</div>
                                  <div className="font-semibold text-gray-900">{companyInfo.overview.size}</div>
                                </div>
                                <div>
                                  <div className="text-sm text-gray-600">Headquarters</div>
                                  <div className="font-semibold text-gray-900">{companyInfo.overview.headquarters}</div>
                                </div>
                                <div>
                                  <div className="text-sm text-gray-600">Founded</div>
                                  <div className="font-semibold text-gray-900">{companyInfo.overview.founded}</div>
                                </div>
                              </div>
                              <p className="text-gray-700 leading-relaxed mb-4">{companyInfo.overview.description}</p>
                              <div className="bg-white rounded-lg p-4">
                                <div className="text-sm font-semibold text-gray-600 mb-2">Mission</div>
                                <p className="text-gray-700 italic">{companyInfo.overview.mission}</p>
                              </div>
                            </div>

                            {/* Recent News */}
                            {companyInfo.recent_news && companyInfo.recent_news.length > 0 && (
                              <div>
                                <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                                  <TrendingUp className="h-6 w-6 text-green-600" />
                                  Recent News & Developments
                                </h3>
                                <div className="space-y-3">
                                  {companyInfo.recent_news.map((news, idx) => (
                                    <div key={idx} className="bg-white border-2 border-gray-200 rounded-lg p-4 hover:border-green-400 transition-colors">
                                      <div className="flex justify-between items-start mb-2">
                                        <h4 className="font-semibold text-gray-900">{news.title}</h4>
                                        <span className="text-xs text-gray-500">{news.date}</span>
                                      </div>
                                      <p className="text-gray-700 text-sm mb-2">{news.summary}</p>
                                      <div className="bg-green-50 border-l-4 border-green-400 p-2 text-sm">
                                        <span className="font-semibold text-green-800">Why it matters: </span>
                                        <span className="text-green-700">{news.relevance}</span>
                                      </div>
                                    </div>
                                  ))}
                                </div>
                              </div>
                            )}

                            {/* Culture */}
                            <div>
                              <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                                <Globe className="h-6 w-6 text-purple-600" />
                                Company Culture
                              </h3>
                              <div className="bg-white border-2 border-gray-200 rounded-lg p-4 space-y-4">
                                <div>
                                  <div className="text-sm font-semibold text-gray-600 mb-2">Core Values</div>
                                  <div className="flex flex-wrap gap-2">
                                    {companyInfo.culture.values.map((value, idx) => (
                                      <span key={idx} className="bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-sm font-semibold">
                                        {value}
                                      </span>
                                    ))}
                                  </div>
                                </div>
                                <div>
                                  <div className="text-sm font-semibold text-gray-600 mb-1">Work Environment</div>
                                  <p className="text-gray-700">{companyInfo.culture.work_environment}</p>
                                </div>
                                <div>
                                  <div className="text-sm font-semibold text-gray-600 mb-1">Work-Life Balance</div>
                                  <p className="text-gray-700">{companyInfo.culture.work_life_balance}</p>
                                </div>
                                <div>
                                  <div className="text-sm font-semibold text-gray-600 mb-1">Diversity & Inclusion</div>
                                  <p className="text-gray-700">{companyInfo.culture.diversity_inclusion}</p>
                                </div>
                              </div>
                            </div>

                            {/* Company-Specific Q&A */}
                            <div>
                              <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                                <MessageSquare className="h-6 w-6 text-blue-600" />
                                Company-Specific Questions & Answers
                              </h3>
                              <div className="space-y-4">
                                {companyInfo.company_qa.map((qa, idx) => (
                                  <div key={idx} className="bg-white border-2 border-gray-200 rounded-lg overflow-hidden">
                                    <button
                                      onClick={() => toggleExpanded(idx)}
                                      className="w-full p-4 flex items-start justify-between hover:bg-gray-50 transition-colors"
                                    >
                                      <div className="flex-1 text-left">
                                        <div className="font-semibold text-gray-900 mb-1">{qa.question}</div>
                                        {!expandedItems.has(idx) && (
                                          <div className="text-sm text-gray-600 line-clamp-2">{qa.answer}</div>
                                        )}
                                      </div>
                                      {expandedItems.has(idx) ? (
                                        <ChevronUp className="h-5 w-5 text-gray-400 flex-shrink-0 ml-2" />
                                      ) : (
                                        <ChevronDown className="h-5 w-5 text-gray-400 flex-shrink-0 ml-2" />
                                      )}
                                    </button>
                                    {expandedItems.has(idx) && (
                                      <div className="px-4 pb-4 border-t border-gray-200 space-y-3">
                                        <div className="bg-blue-50 p-3 rounded-lg">
                                          <div className="text-sm font-semibold text-blue-900 mb-1">Answer:</div>
                                          <p className="text-gray-700 leading-relaxed">{qa.answer}</p>
                                        </div>
                                        <div>
                                          <div className="text-sm font-semibold text-gray-700 mb-2">Key Talking Points:</div>
                                          <ul className="space-y-1">
                                            {qa.talking_points.map((point, pidx) => (
                                              <li key={pidx} className="flex items-start gap-2">
                                                <CheckCircle2 className="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
                                                <span className="text-gray-700 text-sm">{point}</span>
                                              </li>
                                            ))}
                                          </ul>
                                        </div>
                                        <div className="bg-yellow-50 border-l-4 border-yellow-400 p-3">
                                          <span className="text-sm text-yellow-800">
                                            <span className="font-semibold">Reference: </span>
                                            {qa.reference}
                                          </span>
                                        </div>
                                      </div>
                                    )}
                                  </div>
                                ))}
                              </div>
                            </div>

                            {/* Questions to Ask */}
                            {companyInfo.questions_to_ask && companyInfo.questions_to_ask.length > 0 && (
                              <div>
                                <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                                  <Target className="h-6 w-6 text-orange-600" />
                                  Smart Questions to Ask
                                </h3>
                                <div className="bg-orange-50 border-2 border-orange-200 rounded-lg p-4">
                                  <p className="text-sm text-orange-800 mb-4">
                                    Asking thoughtful questions shows engagement and helps you evaluate if the role is right for you.
                                  </p>
                                  <div className="space-y-3">
                                    {companyInfo.questions_to_ask.map((q, idx) => (
                                      <div key={idx} className="bg-white rounded-lg p-3">
                                        <div className="font-semibold text-gray-900 mb-1">{q.question}</div>
                                        <div className="text-sm text-orange-600">
                                          <span className="font-semibold">Why: </span>
                                          {q.why_ask}
                                        </div>
                                      </div>
                                    ))}
                                  </div>
                                </div>
                              </div>
                            )}
                          </div>
                        )}

                        {/* Technical Tab */}
                        {activeTab === 'technical' && (
                          <div className="space-y-4">
                            <div className="bg-blue-50 border-l-4 border-blue-600 p-4 mb-6">
                              <p className="text-blue-900 mb-2">
                                <span className="font-semibold">Pro tip:</span> For each question, think through your approach out loud, 
                                mention trade-offs, and discuss scalability considerations.
                              </p>
                              <p className="text-blue-800 text-sm">
                                💡 Questions include: Employee interview experiences, job requirement analysis, and guidance on explaining YOUR projects impressively.
                              </p>
                            </div>
                            {technicalQA.map((qa, idx) => {
                              const sourceBadge = getSourceBadge(qa.source)
                              return (
                                <div key={idx} className="bg-white border-2 border-gray-200 rounded-lg overflow-hidden">
                                  <button
                                    onClick={() => toggleExpanded(1000 + idx)}
                                    className="w-full p-4 flex items-start justify-between hover:bg-gray-50 transition-colors"
                                  >
                                    <div className="flex-1 text-left">
                                      <div className="flex items-center gap-2 mb-2 flex-wrap">
                                        <span className={`text-xs px-2 py-1 rounded-full font-semibold ${getDifficultyColor(qa.difficulty)}`}>
                                          {qa.difficulty}
                                        </span>
                                        <span className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded-full font-semibold">
                                          {qa.category}
                                        </span>
                                        {sourceBadge && (
                                          <span className={`text-xs px-2 py-1 rounded-full font-semibold ${sourceBadge.color}`}>
                                            {sourceBadge.icon} {sourceBadge.text}
                                          </span>
                                        )}
                                        {qa.project_name && (
                                          <span className="text-xs bg-indigo-100 text-indigo-800 px-2 py-1 rounded-full font-semibold">
                                            📁 {qa.project_name}
                                          </span>
                                        )}
                                      </div>
                                      <div className="font-semibold text-gray-900">{qa.question}</div>
                                    </div>
                                    {expandedItems.has(1000 + idx) ? (
                                      <ChevronUp className="h-5 w-5 text-gray-400 flex-shrink-0 ml-2" />
                                    ) : (
                                      <ChevronDown className="h-5 w-5 text-gray-400 flex-shrink-0 ml-2" />
                                    )}
                                  </button>
                                  {expandedItems.has(1000 + idx) && (
                                    <div className="px-4 pb-4 border-t border-gray-200 space-y-3">
                                      {qa.how_to_explain && (
                                        <div className="bg-gradient-to-r from-purple-50 to-pink-50 border-l-4 border-purple-500 p-4 rounded-r-lg">
                                          <div className="text-sm font-bold text-purple-900 mb-2 flex items-center gap-2">
                                            <span className="text-lg">🎯</span> How to Explain This Impressively:
                                          </div>
                                          <p className="text-purple-900 leading-relaxed">{qa.how_to_explain}</p>
                                        </div>
                                      )}
                                      
                                      {qa.what_to_emphasize && qa.what_to_emphasize.length > 0 && (
                                        <div className="bg-amber-50 border-l-4 border-amber-500 p-3 rounded-r-lg">
                                          <div className="text-sm font-semibold text-amber-900 mb-2">⭐ What to Emphasize:</div>
                                          <ul className="space-y-1">
                                            {qa.what_to_emphasize.map((point, eidx) => (
                                              <li key={eidx} className="flex items-start gap-2">
                                                <span className="text-amber-600 font-bold">→</span>
                                                <span className="text-amber-900 text-sm font-medium">{point}</span>
                                              </li>
                                            ))}
                                          </ul>
                                        </div>
                                      )}
                                      
                                      {qa.impressive_metrics && qa.impressive_metrics.length > 0 && (
                                        <div className="bg-green-50 border-l-4 border-green-500 p-3 rounded-r-lg">
                                          <div className="text-sm font-semibold text-green-900 mb-2">📊 Impressive Metrics to Highlight:</div>
                                          <ul className="space-y-1">
                                            {qa.impressive_metrics.map((metric, midx) => (
                                              <li key={midx} className="flex items-start gap-2">
                                                <span className="text-green-600 font-bold">✓</span>
                                                <span className="text-green-900 text-sm font-medium">{metric}</span>
                                              </li>
                                            ))}
                                          </ul>
                                        </div>
                                      )}
                                      
                                      <div className="bg-blue-50 p-4 rounded-lg">
                                        <div className="text-sm font-semibold text-blue-900 mb-2">Answer:</div>
                                        <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">{qa.answer}</p>
                                      </div>
                                      
                                      <div>
                                        <div className="text-sm font-semibold text-gray-700 mb-2">Key Points:</div>
                                        <ul className="space-y-1">
                                          {qa.key_points.map((point, pidx) => (
                                            <li key={pidx} className="flex items-start gap-2">
                                              <CheckCircle2 className="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
                                              <span className="text-gray-700 text-sm">{point}</span>
                                            </li>
                                          ))}
                                        </ul>
                                      </div>
                                      
                                      {qa.expected_questions && qa.expected_questions.length > 0 && (
                                        <div className="bg-orange-50 border-l-4 border-orange-400 p-3 rounded-r-lg">
                                          <div className="text-sm font-semibold text-orange-900 mb-2">❓ Expected Follow-up Questions:</div>
                                          <ul className="space-y-1">
                                            {qa.expected_questions.map((question, qidx) => (
                                              <li key={qidx} className="text-sm text-orange-800">• {question}</li>
                                            ))}
                                          </ul>
                                        </div>
                                      )}
                                      
                                      {qa.interview_tip && (
                                        <div className="bg-indigo-50 border-l-4 border-indigo-400 p-3 rounded-r-lg">
                                          <div className="text-sm font-semibold text-indigo-900 mb-1">💡 Interview Tip:</div>
                                          <p className="text-indigo-800 text-sm">{qa.interview_tip}</p>
                                        </div>
                                      )}
                                      
                                      {qa.follow_ups && qa.follow_ups.length > 0 && (
                                        <div className="bg-yellow-50 border-l-4 border-yellow-400 p-3 rounded-r-lg">
                                          <div className="text-sm font-semibold text-yellow-900 mb-2">Possible Follow-ups:</div>
                                          <ul className="space-y-1">
                                            {qa.follow_ups.map((followup, fidx) => (
                                              <li key={fidx} className="text-sm text-yellow-800">• {followup}</li>
                                            ))}
                                          </ul>
                                        </div>
                                      )}
                                    </div>
                                  )}
                                </div>
                              )
                            })}
                          </div>
                        )}

                        {/* Behavioral Tab */}
                        {activeTab === 'behavioral' && (
                          <div className="space-y-4">
                            <div className="bg-purple-50 border-l-4 border-purple-600 p-4 mb-6">
                              <p className="text-purple-900">
                                <span className="font-semibold">STAR Method:</span> Structure your answers with Situation, Task, Action, Result. 
                                Be specific, use metrics, and show growth.
                              </p>
                            </div>
                            {behavioralQA.map((qa, idx) => (
                              <div key={idx} className="bg-white border-2 border-gray-200 rounded-lg overflow-hidden">
                                <button
                                  onClick={() => toggleExpanded(2000 + idx)}
                                  className="w-full p-4 flex items-start justify-between hover:bg-gray-50 transition-colors"
                                >
                                  <div className="flex-1 text-left">
                                    <div className="flex items-center gap-2 mb-2">
                                      <span className="text-xs bg-purple-100 text-purple-800 px-2 py-1 rounded-full font-semibold">
                                        {qa.competency}
                                      </span>
                                    </div>
                                    <div className="font-semibold text-gray-900">{qa.question}</div>
                                  </div>
                                  {expandedItems.has(2000 + idx) ? (
                                    <ChevronUp className="h-5 w-5 text-gray-400 flex-shrink-0 ml-2" />
                                  ) : (
                                    <ChevronDown className="h-5 w-5 text-gray-400 flex-shrink-0 ml-2" />
                                  )}
                                </button>
                                {expandedItems.has(2000 + idx) && (
                                  <div className="px-4 pb-4 border-t border-gray-200 space-y-3">
                                    <div className="bg-purple-50 p-4 rounded-lg space-y-3">
                                      <div>
                                        <div className="text-sm font-semibold text-purple-900 mb-1">📍 Situation:</div>
                                        <p className="text-gray-700 text-sm">{qa.situation}</p>
                                      </div>
                                      <div>
                                        <div className="text-sm font-semibold text-purple-900 mb-1">🎯 Task:</div>
                                        <p className="text-gray-700 text-sm">{qa.task}</p>
                                      </div>
                                      <div>
                                        <div className="text-sm font-semibold text-purple-900 mb-1">⚡ Action:</div>
                                        <p className="text-gray-700 text-sm">{qa.action}</p>
                                      </div>
                                      <div>
                                        <div className="text-sm font-semibold text-purple-900 mb-1">🏆 Result:</div>
                                        <p className="text-gray-700 text-sm">{qa.result}</p>
                                      </div>
                                    </div>
                                    <div className="bg-blue-50 p-3 rounded-lg">
                                      <div className="text-sm font-semibold text-blue-900 mb-2">Complete Answer:</div>
                                      <p className="text-gray-700 leading-relaxed text-sm">{qa.answer}</p>
                                    </div>
                                    {qa.tips && qa.tips.length > 0 && (
                                      <div className="bg-green-50 border-l-4 border-green-400 p-3">
                                        <div className="text-sm font-semibold text-green-900 mb-2">💡 Tips:</div>
                                        <ul className="space-y-1">
                                          {qa.tips.map((tip, tidx) => (
                                            <li key={tidx} className="text-sm text-green-800">• {tip}</li>
                                          ))}
                                        </ul>
                                      </div>
                                    )}
                                  </div>
                                )}
                              </div>
                            ))}
                          </div>
                        )}

                        {/* HR Tab */}
                        {activeTab === 'hr' && (
                          <div className="space-y-4">
                            <div className="bg-green-50 border-l-4 border-green-600 p-4 mb-6">
                              <p className="text-green-900">
                                <span className="font-semibold">Strategy:</span> Be honest but strategic. Show self-awareness, 
                                growth mindset, and alignment with company values.
                              </p>
                            </div>
                            {hrQA.map((qa, idx) => (
                              <div key={idx} className="bg-white border-2 border-gray-200 rounded-lg overflow-hidden">
                                <button
                                  onClick={() => toggleExpanded(3000 + idx)}
                                  className="w-full p-4 flex items-start justify-between hover:bg-gray-50 transition-colors"
                                >
                                  <div className="flex-1 text-left">
                                    <div className="flex items-center gap-2 mb-2">
                                      <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full font-semibold">
                                        {qa.category}
                                      </span>
                                    </div>
                                    <div className="font-semibold text-gray-900">{qa.question}</div>
                                  </div>
                                  {expandedItems.has(3000 + idx) ? (
                                    <ChevronUp className="h-5 w-5 text-gray-400 flex-shrink-0 ml-2" />
                                  ) : (
                                    <ChevronDown className="h-5 w-5 text-gray-400 flex-shrink-0 ml-2" />
                                  )}
                                </button>
                                {expandedItems.has(3000 + idx) && (
                                  <div className="px-4 pb-4 border-t border-gray-200 space-y-3">
                                    <div className="bg-green-50 p-4 rounded-lg">
                                      <div className="text-sm font-semibold text-green-900 mb-2">Strategic Answer:</div>
                                      <p className="text-gray-700 leading-relaxed">{qa.answer}</p>
                                    </div>
                                    <div className="bg-blue-50 p-3 rounded-lg">
                                      <div className="text-sm font-semibold text-blue-900 mb-2">Example Answer:</div>
                                      <p className="text-gray-700 text-sm italic">{qa.example_answer}</p>
                                    </div>
                                    <div className="grid grid-cols-2 gap-3">
                                      <div className="bg-green-50 border-l-4 border-green-500 p-3">
                                        <div className="text-sm font-semibold text-green-900 mb-2">✅ Do:</div>
                                        <ul className="space-y-1">
                                          {qa.dos.map((item, didx) => (
                                            <li key={didx} className="text-sm text-green-800">• {item}</li>
                                          ))}
                                        </ul>
                                      </div>
                                      <div className="bg-red-50 border-l-4 border-red-500 p-3">
                                        <div className="text-sm font-semibold text-red-900 mb-2">❌ Don't:</div>
                                        <ul className="space-y-1">
                                          {qa.donts.map((item, didx) => (
                                            <li key={didx} className="text-sm text-red-800">• {item}</li>
                                          ))}
                                        </ul>
                                      </div>
                                    </div>
                                  </div>
                                )}
                              </div>
                            ))}
                          </div>
                        )}
                      </>
                    )}
                  </div>
                </div>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
