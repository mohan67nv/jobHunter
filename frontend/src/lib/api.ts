/**
 * API client for SmartJobHunter Pro
 */
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('[API Error]', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

// API endpoints
export const jobsApi = {
  list: (params: any) => api.get('/api/jobs', { params }),
  get: (id: number) => api.get(`/api/jobs/${id}`),
  update: (id: number, data: any) => api.put(`/api/jobs/${id}`, data),
  delete: (id: number) => api.delete(`/api/jobs/${id}`),
  getSimilar: (id: number) => api.get(`/api/jobs/${id}/similar`),
}

export const applicationsApi = {
  list: (status?: string) => api.get('/api/applications', { params: { status } }),
  get: (id: number) => api.get(`/api/applications/${id}`),
  create: (data: any) => api.post('/api/applications', data),
  update: (id: number, data: any) => api.put(`/api/applications/${id}`, data),
  delete: (id: number) => api.delete(`/api/applications/${id}`),
  getStats: () => api.get('/api/applications/stats'),
}

export const analysisApi = {
  analyzeJob: (jobId: number, generateMaterials: boolean = true) =>
    api.post(`/api/analysis/analyze-job/${jobId}`, null, { params: { generate_materials: generateMaterials } }),
  batchAnalyze: (jobIds: number[]) => api.post('/api/analysis/batch-analyze', { job_ids: jobIds }),
  get: (jobId: number) => api.get(`/api/analysis/${jobId}`),
  generateResume: (jobId: number) => api.post(`/api/analysis/generate-resume/${jobId}`),
  generateCoverLetter: (jobId: number) => api.post(`/api/analysis/generate-cover-letter/${jobId}`),
  getInterviewPrep: (jobId: number) => api.get(`/api/analysis/interview-prep/${jobId}`),
}

export const scrapersApi = {
  scrape: (keyword: string, location: string, sources?: string[]) =>
    api.post('/api/scrapers/scrape', null, { params: { keyword, location, sources } }),
  scrapeCompanies: () => api.post('/api/scrapers/scrape-companies'),
  getHistory: (limit: number = 50) => api.get('/api/scrapers/history', { params: { limit } }),
  getSources: () => api.get('/api/scrapers/sources'),
}

export const userApi = {
  getProfile: () => api.get('/api/user/profile'),
  updateProfile: (data: any) => api.put('/api/user/profile', data),
  uploadResume: (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/api/user/resume', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  listResumes: () => api.get('/api/user/resumes'),
  createResumeVersion: (data: any) => api.post('/api/user/resumes', data),
  listCoverLetters: () => api.get('/api/user/cover-letters'),
  createCoverLetter: (data: any) => api.post('/api/user/cover-letters', data),
  updatePreferences: (data: any) => api.put('/api/user/preferences', data),
}

export const analyticsApi = {
  getOverview: () => api.get('/api/analytics/overview'),
  getApplicationsTimeline: (days: number = 30) => api.get('/api/analytics/applications-timeline', { params: { days } }),
  getJobsBySource: () => api.get('/api/analytics/sources'),
  getMatchScoreDistribution: () => api.get('/api/analytics/match-score-distribution'),
  getTopCompanies: (limit: number = 10) => api.get('/api/analytics/top-companies', { params: { limit } }),
  getSkillsDemand: (limit: number = 20) => api.get('/api/analytics/skills-demand', { params: { limit } }),
  getApplicationFunnel: () => api.get('/api/analytics/application-funnel'),
  getSuccessRate: () => api.get('/api/analytics/success-rate'),
}

export default api
