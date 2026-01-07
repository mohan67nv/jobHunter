import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { 
  BookOpen, CheckCircle2, Building, Code, MessageSquare, 
  Sparkles, ChevronDown, ChevronUp, Briefcase, TrendingUp,
  Calendar, MapPin, Users, Globe, Award, Target, Plus,
  Trash2, RefreshCw, Star, Clock, Search, Filter
} from 'lucide-react'

interface ManualPrep {
  id: number
  company_name: string
  job_title: string
  job_url?: string
  job_description?: string
  created_at: string
  expires_at: string
  status: 'active' | 'archived' | 'completed'
  is_favorite: boolean
  interview_date?: string
  company_insights: any
  technical_qa: any[]
  behavioral_qa: any[]
  hr_qa: any[]
  key_talking_points: any[]
  preparation_tips: any[]
}

export default function ManualPrep() {
  const [selectedPrepId, setSelectedPrepId] = useState<number | null>(null)
  const [activeTab, setActiveTab] = useState<'insights' | 'technical' | 'behavioral' | 'hr' | 'tips'>('insights')
  const [expandedItems, setExpandedItems] = useState<Set<number>>(new Set())
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [statusFilter, setStatusFilter] = useState<'all' | 'active' | 'completed' | 'archived'>('active')
  
  // Form state
  const [formData, setFormData] = useState({
    company_name: '',
    job_title: '',
    job_url: '',
    job_description: ''
  })
  
  const queryClient = useQueryClient()

  // Fetch manual preps
  const { data: prepsResponse, isLoading } = useQuery({
    queryKey: ['manual-preps', statusFilter, searchQuery],
    queryFn: async () => {
      const params = new URLSearchParams()
      if (statusFilter !== 'all') params.append('status', statusFilter)
      if (searchQuery) params.append('search', searchQuery)
      
      const response = await fetch(`http://localhost:8000/api/manual-prep?${params}`)
      if (!response.ok) throw new Error('Failed to fetch manual preps')
      return response.json()
    },
  })

  const preps: ManualPrep[] = prepsResponse?.data || []

  // Fetch single prep details
  const { data: prepDetails, isLoading: isLoadingDetails } = useQuery({
    queryKey: ['manual-prep', selectedPrepId],
    queryFn: async () => {
      if (!selectedPrepId) return null
      const response = await fetch(`http://localhost:8000/api/manual-prep/${selectedPrepId}`)
      if (!response.ok) throw new Error('Failed to fetch prep details')
      return response.json()
    },
    enabled: !!selectedPrepId,
  })

  // Create manual prep mutation
  const createPrepMutation = useMutation({
    mutationFn: async (data: typeof formData) => {
      const params = new URLSearchParams()
      params.append('company_name', data.company_name)
      if (data.job_title) params.append('job_title', data.job_title)
      if (data.job_url) params.append('job_url', data.job_url)
      if (data.job_description) params.append('job_description', data.job_description)
      
      const response = await fetch(`http://localhost:8000/api/manual-prep?${params}`, {
        method: 'POST',
      })
      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Failed to create prep')
      }
      return response.json()
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['manual-preps'] })
      setSelectedPrepId(data.data.id)
      setShowCreateForm(false)
      setFormData({ company_name: '', job_title: '', job_url: '', job_description: '' })
      alert('✅ Manual prep created successfully! AI is generating content...')
    },
    onError: (error: any) => {
      alert(`❌ Failed to create prep: ${error.message}`)
    }
  })

  // Delete prep mutation
  const deletePrepMutation = useMutation({
    mutationFn: async (prepId: number) => {
      const response = await fetch(`http://localhost:8000/api/manual-prep/${prepId}`, {
        method: 'DELETE'
      })
      if (!response.ok) throw new Error('Failed to delete prep')
      return response.json()
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['manual-preps'] })
      if (selectedPrepId === preps[0]?.id) {
        setSelectedPrepId(preps[1]?.id || null)
      }
    }
  })

  // Toggle favorite mutation
  const toggleFavoriteMutation = useMutation({
    mutationFn: async ({ prepId, isFavorite }: { prepId: number, isFavorite: boolean }) => {
      const response = await fetch(`http://localhost:8000/api/manual-prep/${prepId}?is_favorite=${!isFavorite}`, {
        method: 'PUT',
      })
      if (!response.ok) throw new Error('Failed to update favorite')
      return response.json()
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['manual-preps'] })
      queryClient.invalidateQueries({ queryKey: ['manual-prep', selectedPrepId] })
    }
  })

  // Export to PDF mutation
  const exportPdfMutation = useMutation({
    mutationFn: async (prepId: number) => {
      const response = await fetch(`http://localhost:8000/api/manual-prep/${prepId}/export-pdf`, {
        method: 'GET',
      })
      if (!response.ok) throw new Error('Failed to export PDF')
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `interview_prep_${prepId}.pdf`
      a.click()
      window.URL.revokeObjectURL(url)
    },
    onSuccess: () => {
      alert('✅ PDF exported successfully!')
    },
    onError: () => {
      alert('❌ Failed to export PDF')
    }
  })

  // Set first prep as selected by default
  useEffect(() => {
    if (preps.length > 0 && !selectedPrepId) {
      setSelectedPrepId(preps[0].id)
    }
  }, [preps, selectedPrepId])

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

  const handleCreatePrep = (e: React.FormEvent) => {
    e.preventDefault()
    if (!formData.company_name.trim() || !formData.job_title.trim()) {
      alert('Company name and job title are required')
      return
    }
    createPrepMutation.mutate(formData)
  }

  const getDaysRemaining = (expiresAt: string) => {
    const days = Math.ceil((new Date(expiresAt).getTime() - Date.now()) / (1000 * 60 * 60 * 24))
    return days
  }

  const getDaysRemainingColor = (days: number) => {
    if (days <= 3) return 'text-red-600'
    if (days <= 7) return 'text-orange-600'
    if (days <= 14) return 'text-yellow-600'
    return 'text-green-600'
  }

  const selectedPrep = prepDetails || preps.find(p => p.id === selectedPrepId)

  return (
    <div className="min-h-screen">
      {/* Header */}
      <div className="mb-4 sm:mb-8">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 sm:gap-4">
          <div className="flex-1 min-w-0">
            <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent flex items-center gap-2 sm:gap-3">
              <Sparkles className="h-7 w-7 sm:h-8 sm:w-8 lg:h-10 lg:w-10 text-purple-600 flex-shrink-0" />
              <span>Manual Prep</span>
            </h1>
            <p className="text-gray-600 mt-2 text-sm sm:text-base lg:text-lg">
              Advanced AI-powered interview preparation using DeepSeek models
            </p>
          </div>
          <button
            onClick={() => setShowCreateForm(true)}
            className="px-4 sm:px-6 py-2.5 sm:py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-lg hover:from-purple-700 hover:to-pink-700 transition-all flex items-center justify-center gap-2 shadow-lg text-sm sm:text-base whitespace-nowrap flex-shrink-0"
          >
            <Plus className="h-4 w-4 sm:h-5 sm:w-5" />
            <span>New Prep</span>
          </button>
        </div>
      </div>

      {/* Create Form Modal */}
      {showCreateForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Create New Interview Prep</h2>
              <form onSubmit={handleCreatePrep} className="space-y-4">
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Company Name *
                  </label>
                  <input
                    type="text"
                    value={formData.company_name}
                    onChange={(e) => setFormData({ ...formData, company_name: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    placeholder="e.g., Google, Amazon, Microsoft"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Job Title *
                  </label>
                  <input
                    type="text"
                    value={formData.job_title}
                    onChange={(e) => setFormData({ ...formData, job_title: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    placeholder="e.g., Senior Software Engineer"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Job URL (Optional)
                  </label>
                  <input
                    type="url"
                    value={formData.job_url}
                    onChange={(e) => setFormData({ ...formData, job_url: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    placeholder="https://..."
                  />
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Job Description (Optional)
                  </label>
                  <textarea
                    value={formData.job_description}
                    onChange={(e) => setFormData({ ...formData, job_description: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    placeholder="Paste the full job description here for better AI-generated content..."
                    rows={6}
                  />
                </div>

                <div className="flex gap-3 pt-4">
                  <button
                    type="submit"
                    disabled={createPrepMutation.isPending}
                    className="flex-1 px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-lg hover:from-purple-700 hover:to-pink-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed font-semibold"
                  >
                    {createPrepMutation.isPending ? (
                      <span className="flex items-center justify-center gap-2">
                        <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                        Generating with AI...
                      </span>
                    ) : (
                      'Create Prep'
                    )}
                  </button>
                  <button
                    type="button"
                    onClick={() => setShowCreateForm(false)}
                    className="px-6 py-3 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-all font-semibold"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {isLoading ? (
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
          <p className="text-gray-600 mt-4">Loading preparations...</p>
        </div>
      ) : preps.length === 0 ? (
        <div className="bg-white rounded-xl shadow-lg p-12 text-center">
          <BookOpen className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 mb-2">No Manual Preps Yet</h2>
          <p className="text-gray-600 mb-6">
            Create your first manual interview preparation by clicking "New Prep" above.
            <br />
            Our advanced AI will generate comprehensive preparation materials using DeepSeek models.
          </p>
          <button
            onClick={() => setShowCreateForm(true)}
            className="px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-lg hover:from-purple-700 hover:to-pink-700 transition-all inline-flex items-center gap-2"
          >
            <Plus className="h-5 w-5" />
            Create First Prep
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Left: Prep List */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-xl shadow-lg p-4 sticky top-4">
              {/* Search and Filter */}
              <div className="mb-4 space-y-2">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                  <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="Search..."
                    className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent text-sm"
                  />
                </div>
                <select
                  value={statusFilter}
                  onChange={(e) => setStatusFilter(e.target.value as any)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent text-sm"
                >
                  <option value="all">All</option>
                  <option value="active">Active</option>
                  <option value="completed">Completed</option>
                  <option value="archived">Archived</option>
                </select>
              </div>

              <h2 className="text-lg font-bold text-gray-900 mb-4">Your Preparations</h2>
              <div className="space-y-2 max-h-[600px] overflow-y-auto">
                {preps.map((prep) => {
                  const daysRemaining = getDaysRemaining(prep.expires_at)
                  return (
                    <div
                      key={prep.id}
                      className={`group relative p-3 rounded-lg border-2 transition-all cursor-pointer ${
                        selectedPrepId === prep.id
                          ? 'border-purple-500 bg-purple-50'
                          : 'border-gray-200 hover:border-gray-300'
                      }`}
                    >
                      <div onClick={() => setSelectedPrepId(prep.id)}>
                        <div className="flex items-start justify-between mb-1">
                          <div className="font-semibold text-gray-900 text-sm truncate flex-1">
                            {prep.job_title}
                          </div>
                          {prep.is_favorite && (
                            <Star className="h-4 w-4 text-yellow-500 fill-current flex-shrink-0 ml-1" />
                          )}
                        </div>
                        <div className="text-xs text-gray-600 truncate mb-2">
                          {prep.company_name}
                        </div>
                        <div className={`text-xs font-medium ${getDaysRemainingColor(daysRemaining)} flex items-center gap-1`}>
                          <Clock className="h-3 w-3" />
                          {daysRemaining > 0 ? `${daysRemaining} days left` : 'Expired'}
                        </div>
                      </div>
                      
                      <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity">
                        <button
                          onClick={(e) => {
                            e.stopPropagation()
                            if (confirm(`Delete prep for ${prep.company_name}?`)) {
                              deletePrepMutation.mutate(prep.id)
                            }
                          }}
                          className="p-1 hover:bg-red-100 rounded transition-colors"
                        >
                          <Trash2 className="h-4 w-4 text-red-600" />
                        </button>
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>
          </div>

          {/* Right: Prep Content */}
          <div className="lg:col-span-3">
            {selectedPrep && (
              <>
                {/* Prep Header */}
                <div className="bg-gradient-to-r from-purple-600 to-pink-600 rounded-xl shadow-lg p-6 text-white mb-6">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <h2 className="text-2xl font-bold mb-2">{selectedPrep.job_title}</h2>
                      <div className="flex items-center gap-4 text-purple-100 flex-wrap">
                        <div className="flex items-center gap-2">
                          <Building className="h-4 w-4" />
                          {selectedPrep.company_name}
                        </div>
                        {selectedPrep.job_url && (
                          <a
                            href={selectedPrep.job_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="flex items-center gap-2 hover:text-white transition-colors"
                          >
                            <Globe className="h-4 w-4" />
                            View Job
                          </a>
                        )}
                        <div className="flex items-center gap-2">
                          <Calendar className="h-4 w-4" />
                          Created {new Date(selectedPrep.created_at).toLocaleDateString()}
                        </div>
                      </div>
                    </div>
                    <button
                      onClick={() => toggleFavoriteMutation.mutate({ 
                        prepId: selectedPrep.id, 
                        isFavorite: selectedPrep.is_favorite 
                      })}
                      className="p-2 hover:bg-white/20 rounded-lg transition-colors"
                    >
                      <Star className={`h-6 w-6 ${selectedPrep.is_favorite ? 'fill-current' : ''}`} />
                    </button>
                  </div>
                </div>

                {/* Tabs */}
                <div className="bg-white rounded-xl shadow-lg mb-6">
                  <div className="border-b border-gray-200">
                    <div className="flex overflow-x-auto">
                      <button
                        onClick={() => setActiveTab('insights')}
                        className={`flex items-center gap-2 px-6 py-4 border-b-2 font-semibold transition-colors whitespace-nowrap ${
                          activeTab === 'insights'
                            ? 'border-purple-600 text-purple-600'
                            : 'border-transparent text-gray-600 hover:text-gray-900'
                        }`}
                      >
                        <Building className="h-5 w-5" />
                        Company Insights
                      </button>
                      <button
                        onClick={() => setActiveTab('technical')}
                        className={`flex items-center gap-2 px-6 py-4 border-b-2 font-semibold transition-colors whitespace-nowrap ${
                          activeTab === 'technical'
                            ? 'border-purple-600 text-purple-600'
                            : 'border-transparent text-gray-600 hover:text-gray-900'
                        }`}
                      >
                        <Code className="h-5 w-5" />
                        Technical ({selectedPrep.technical_qa?.length || 0})
                      </button>
                      <button
                        onClick={() => setActiveTab('behavioral')}
                        className={`flex items-center gap-2 px-6 py-4 border-b-2 font-semibold transition-colors whitespace-nowrap ${
                          activeTab === 'behavioral'
                            ? 'border-purple-600 text-purple-600'
                            : 'border-transparent text-gray-600 hover:text-gray-900'
                        }`}
                      >
                        <MessageSquare className="h-5 w-5" />
                        Behavioral ({selectedPrep.behavioral_qa?.length || 0})
                      </button>
                      <button
                        onClick={() => setActiveTab('hr')}
                        className={`flex items-center gap-2 px-6 py-4 border-b-2 font-semibold transition-colors whitespace-nowrap ${
                          activeTab === 'hr'
                            ? 'border-purple-600 text-purple-600'
                            : 'border-transparent text-gray-600 hover:text-gray-900'
                        }`}
                      >
                        <Users className="h-5 w-5" />
                        HR Round ({selectedPrep.hr_qa?.length || 0})
                      </button>
                      <button
                        onClick={() => setActiveTab('tips')}
                        className={`flex items-center gap-2 px-6 py-4 border-b-2 font-semibold transition-colors whitespace-nowrap ${
                          activeTab === 'tips'
                            ? 'border-purple-600 text-purple-600'
                            : 'border-transparent text-gray-600 hover:text-gray-900'
                        }`}
                      >
                        <Target className="h-5 w-5" />
                        Strategy & Tips
                      </button>
                    </div>
                  </div>

                  {/* Tab Content */}
                  <div className="p-6">
                    {isLoadingDetails ? (
                      <div className="text-center py-12">
                        <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
                        <p className="text-gray-600 mt-4">Loading preparation details...</p>
                      </div>
                    ) : (
                      <>
                        {/* Company Insights Tab */}
                        {activeTab === 'insights' && selectedPrep.company_insights && (
                          <div className="space-y-6">
                            <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-lg p-6">
                              <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                                <Building className="h-6 w-6 text-purple-600" />
                                Company Overview
                              </h3>
                              <p className="text-gray-700 leading-relaxed">
                                {selectedPrep.company_insights.overview}
                              </p>
                              
                              {selectedPrep.company_insights.culture && (
                                <div className="mt-4 pt-4 border-t border-purple-200">
                                  <h4 className="font-semibold text-gray-900 mb-2">Culture</h4>
                                  <p className="text-gray-700">{selectedPrep.company_insights.culture}</p>
                                </div>
                              )}
                              
                              {selectedPrep.company_insights.tech_stack?.length > 0 && (
                                <div className="mt-4 pt-4 border-t border-purple-200">
                                  <h4 className="font-semibold text-gray-900 mb-2">Tech Stack</h4>
                                  <div className="flex flex-wrap gap-2">
                                    {selectedPrep.company_insights.tech_stack.map((tech: string, idx: number) => (
                                      <span key={idx} className="px-3 py-1 bg-white rounded-full text-sm text-gray-700 border border-purple-200">
                                        {tech}
                                      </span>
                                    ))}
                                  </div>
                                </div>
                              )}
                            </div>

                            {selectedPrep.company_insights.recent_news?.length > 0 && (
                              <div className="bg-white border border-gray-200 rounded-lg p-6">
                                <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
                                  <TrendingUp className="h-5 w-5 text-purple-600" />
                                  Recent News & Updates
                                </h3>
                                <div className="space-y-3">
                                  {selectedPrep.company_insights.recent_news.map((news: string, idx: number) => (
                                    <div key={idx} className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg">
                                      <div className="w-2 h-2 rounded-full bg-purple-600 mt-2 flex-shrink-0"></div>
                                      <p className="text-gray-700">{news}</p>
                                    </div>
                                  ))}
                                </div>
                              </div>
                            )}

                            {selectedPrep.company_insights.why_work_here?.length > 0 && (
                              <div className="bg-white border border-gray-200 rounded-lg p-6">
                                <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
                                  <Award className="h-5 w-5 text-purple-600" />
                                  Why Work Here?
                                </h3>
                                <div className="space-y-2">
                                  {selectedPrep.company_insights.why_work_here.map((reason: string, idx: number) => (
                                    <div key={idx} className="flex items-start gap-3">
                                      <CheckCircle2 className="h-5 w-5 text-green-600 mt-0.5 flex-shrink-0" />
                                      <p className="text-gray-700">{reason}</p>
                                    </div>
                                  ))}
                                </div>
                              </div>
                            )}
                          </div>
                        )}

                        {/* Technical Q&A Tab */}
                        {activeTab === 'technical' && (
                          <div className="space-y-4">
                            {selectedPrep.technical_qa?.length > 0 ? (
                              selectedPrep.technical_qa.map((qa: any, idx: number) => (
                                <div key={idx} className="bg-white border border-gray-200 rounded-lg overflow-hidden">
                                  <button
                                    onClick={() => toggleExpanded(idx)}
                                    className="w-full text-left p-4 hover:bg-gray-50 transition-colors flex items-start justify-between gap-4"
                                  >
                                    <div className="flex-1">
                                      <div className="flex items-center gap-3 mb-2">
                                        <span className="text-sm font-semibold text-gray-500">Q{idx + 1}</span>
                                        {qa.difficulty && (
                                          <span className={`px-2 py-1 rounded-full text-xs font-semibold ${
                                            qa.difficulty.toLowerCase() === 'easy' ? 'bg-green-100 text-green-800' :
                                            qa.difficulty.toLowerCase() === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                                            'bg-red-100 text-red-800'
                                          }`}>
                                            {qa.difficulty}
                                          </span>
                                        )}
                                        {qa.topics?.map((topic: string, tidx: number) => (
                                          <span key={tidx} className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs">
                                            {topic}
                                          </span>
                                        ))}
                                      </div>
                                      <h4 className="font-semibold text-gray-900">{qa.question}</h4>
                                    </div>
                                    {expandedItems.has(idx) ? (
                                      <ChevronUp className="h-5 w-5 text-gray-400 flex-shrink-0" />
                                    ) : (
                                      <ChevronDown className="h-5 w-5 text-gray-400 flex-shrink-0" />
                                    )}
                                  </button>
                                  
                                  {expandedItems.has(idx) && (
                                    <div className="p-4 pt-0 border-t border-gray-100">
                                      <div className="bg-purple-50 rounded-lg p-4 mb-4">
                                        <h5 className="font-semibold text-gray-900 mb-2">Answer:</h5>
                                        <p className="text-gray-700 whitespace-pre-wrap">{qa.answer}</p>
                                      </div>
                                      
                                      {qa.why_they_ask && (
                                        <div className="mb-4">
                                          <h5 className="font-semibold text-gray-900 mb-2 flex items-center gap-2">
                                            <Target className="h-4 w-4 text-purple-600" />
                                            Why They Ask This:
                                          </h5>
                                          <p className="text-gray-700">{qa.why_they_ask}</p>
                                        </div>
                                      )}
                                      
                                      {qa.follow_up && (
                                        <div className="bg-yellow-50 rounded-lg p-3">
                                          <h5 className="font-semibold text-gray-900 mb-1 text-sm">Follow-up:</h5>
                                          <p className="text-gray-700 text-sm">{qa.follow_up}</p>
                                        </div>
                                      )}
                                    </div>
                                  )}
                                </div>
                              ))
                            ) : (
                              <p className="text-gray-500 text-center py-8">No technical questions available</p>
                            )}
                          </div>
                        )}

                        {/* Behavioral Q&A Tab */}
                        {activeTab === 'behavioral' && (
                          <div className="space-y-4">
                            {selectedPrep.behavioral_qa?.length > 0 ? (
                              selectedPrep.behavioral_qa.map((qa: any, idx: number) => (
                                <div key={idx} className="bg-white border border-gray-200 rounded-lg overflow-hidden">
                                  <button
                                    onClick={() => toggleExpanded(1000 + idx)}
                                    className="w-full text-left p-4 hover:bg-gray-50 transition-colors flex items-start justify-between gap-4"
                                  >
                                    <div className="flex-1">
                                      <div className="flex items-center gap-3 mb-2">
                                        <span className="text-sm font-semibold text-gray-500">Q{idx + 1}</span>
                                        {qa.category && (
                                          <span className="px-2 py-1 bg-purple-100 text-purple-800 rounded-full text-xs font-semibold">
                                            {qa.category}
                                          </span>
                                        )}
                                      </div>
                                      <h4 className="font-semibold text-gray-900">{qa.question}</h4>
                                    </div>
                                    {expandedItems.has(1000 + idx) ? (
                                      <ChevronUp className="h-5 w-5 text-gray-400 flex-shrink-0" />
                                    ) : (
                                      <ChevronDown className="h-5 w-5 text-gray-400 flex-shrink-0" />
                                    )}
                                  </button>
                                  
                                  {expandedItems.has(1000 + idx) && (
                                    <div className="p-4 pt-0 border-t border-gray-100">
                                      {qa.star_example && (
                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                                          <div className="bg-blue-50 rounded-lg p-4">
                                            <h5 className="font-semibold text-blue-900 mb-2">Situation</h5>
                                            <p className="text-gray-700 text-sm">{qa.star_example.situation}</p>
                                          </div>
                                          <div className="bg-green-50 rounded-lg p-4">
                                            <h5 className="font-semibold text-green-900 mb-2">Task</h5>
                                            <p className="text-gray-700 text-sm">{qa.star_example.task}</p>
                                          </div>
                                          <div className="bg-purple-50 rounded-lg p-4">
                                            <h5 className="font-semibold text-purple-900 mb-2">Action</h5>
                                            <p className="text-gray-700 text-sm">{qa.star_example.action}</p>
                                          </div>
                                          <div className="bg-orange-50 rounded-lg p-4">
                                            <h5 className="font-semibold text-orange-900 mb-2">Result</h5>
                                            <p className="text-gray-700 text-sm">{qa.star_example.result}</p>
                                          </div>
                                        </div>
                                      )}
                                      
                                      {qa.company_relevance && (
                                        <div className="bg-purple-50 rounded-lg p-3">
                                          <h5 className="font-semibold text-gray-900 mb-1 text-sm">Company Relevance:</h5>
                                          <p className="text-gray-700 text-sm">{qa.company_relevance}</p>
                                        </div>
                                      )}
                                    </div>
                                  )}
                                </div>
                              ))
                            ) : (
                              <p className="text-gray-500 text-center py-8">No behavioral questions available</p>
                            )}
                          </div>
                        )}

                        {/* HR Q&A Tab */}
                        {activeTab === 'hr' && (
                          <div className="space-y-4">
                            {selectedPrep.hr_qa?.length > 0 ? (
                              selectedPrep.hr_qa.map((qa: any, idx: number) => (
                                <div key={idx} className="bg-white border border-gray-200 rounded-lg overflow-hidden">
                                  <button
                                    onClick={() => toggleExpanded(2000 + idx)}
                                    className="w-full text-left p-4 hover:bg-gray-50 transition-colors flex items-start justify-between gap-4"
                                  >
                                    <div className="flex-1">
                                      <div className="flex items-center gap-3 mb-2">
                                        <span className="text-sm font-semibold text-gray-500">Q{idx + 1}</span>
                                        {qa.category && (
                                          <span className="px-2 py-1 bg-pink-100 text-pink-800 rounded-full text-xs font-semibold">
                                            {qa.category}
                                          </span>
                                        )}
                                      </div>
                                      <h4 className="font-semibold text-gray-900">{qa.question}</h4>
                                    </div>
                                    {expandedItems.has(2000 + idx) ? (
                                      <ChevronUp className="h-5 w-5 text-gray-400 flex-shrink-0" />
                                    ) : (
                                      <ChevronDown className="h-5 w-5 text-gray-400 flex-shrink-0" />
                                    )}
                                  </button>
                                  
                                  {expandedItems.has(2000 + idx) && (
                                    <div className="p-4 pt-0 border-t border-gray-100">
                                      <div className="bg-purple-50 rounded-lg p-4 mb-4">
                                        <h5 className="font-semibold text-gray-900 mb-2">Answer Strategy:</h5>
                                        <p className="text-gray-700 whitespace-pre-wrap">{qa.answer}</p>
                                      </div>
                                      
                                      {qa.tips?.length > 0 && (
                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                          <div className="bg-green-50 rounded-lg p-3">
                                            <h5 className="font-semibold text-green-900 mb-2 text-sm">Do's:</h5>
                                            <ul className="space-y-1">
                                              {qa.tips.map((tip: string, tidx: number) => (
                                                <li key={tidx} className="text-gray-700 text-sm flex items-start gap-2">
                                                  <CheckCircle2 className="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
                                                  {tip}
                                                </li>
                                              ))}
                                            </ul>
                                          </div>
                                          {qa.red_flags?.length > 0 && (
                                            <div className="bg-red-50 rounded-lg p-3">
                                              <h5 className="font-semibold text-red-900 mb-2 text-sm">Avoid:</h5>
                                              <ul className="space-y-1">
                                                {qa.red_flags.map((flag: string, fidx: number) => (
                                                  <li key={fidx} className="text-gray-700 text-sm flex items-start gap-2">
                                                    <span className="text-red-600 mt-0.5 flex-shrink-0">✗</span>
                                                    {flag}
                                                  </li>
                                                ))}
                                              </ul>
                                            </div>
                                          )}
                                        </div>
                                      )}
                                    </div>
                                  )}
                                </div>
                              ))
                            ) : (
                              <p className="text-gray-500 text-center py-8">No HR questions available</p>
                            )}
                          </div>
                        )}

                        {/* Strategy & Tips Tab */}
                        {activeTab === 'tips' && (
                          <div className="space-y-6">
                            {selectedPrep.key_talking_points?.length > 0 && (
                              <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-lg p-6">
                                <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                                  <Target className="h-6 w-6 text-purple-600" />
                                  Key Talking Points
                                </h3>
                                <div className="space-y-4">
                                  {selectedPrep.key_talking_points.map((point: any, idx: number) => (
                                    <div key={idx} className="bg-white rounded-lg p-4 border border-purple-200">
                                      <h4 className="font-semibold text-gray-900 mb-2">{point.point}</h4>
                                      <p className="text-gray-700 text-sm mb-2">{point.why}</p>
                                      <div className="bg-purple-100 rounded p-2 text-sm text-purple-900">
                                        <span className="font-semibold">How to mention:</span> {point.how_to_mention}
                                      </div>
                                    </div>
                                  ))}
                                </div>
                              </div>
                            )}

                            {selectedPrep.preparation_tips?.length > 0 && (
                              <div className="bg-white border border-gray-200 rounded-lg p-6">
                                <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                                  <Sparkles className="h-6 w-6 text-purple-600" />
                                  Preparation Tips
                                </h3>
                                <div className="space-y-3">
                                  {selectedPrep.preparation_tips.map((tip: any, idx: number) => (
                                    <div key={idx} className="flex items-start gap-4 p-4 bg-gray-50 rounded-lg">
                                      <div className={`px-3 py-1 rounded-full text-xs font-semibold ${
                                        tip.priority === 'High' ? 'bg-red-100 text-red-800' :
                                        tip.priority === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                                        'bg-green-100 text-green-800'
                                      }`}>
                                        {tip.priority}
                                      </div>
                                      <div className="flex-1">
                                        <div className="text-xs text-gray-500 mb-1">{tip.category}</div>
                                        <p className="text-gray-700 font-medium">{tip.tip}</p>
                                      </div>
                                    </div>
                                  ))}
                                </div>
                              </div>
                            )}
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
