/**
 * TypeScript type definitions for SmartJobHunter Pro
 */

export interface Job {
  id: number
  title: string
  company: string
  location: string
  salary?: string
  job_type?: string
  contract_type?: string
  remote_type?: string
  experience_level?: string
  posted_date: string
  scraped_date: string
  deadline_date?: string
  description: string
  requirements?: string
  benefits?: string
  url: string
  source: string
  is_active: boolean
  is_duplicate: boolean
  duplicate_of?: number
  view_count: number
  created_at: string
  updated_at: string
  languages?: string[]
}

export interface JobAnalysis {
  id: number
  job_id: number
  match_score?: number
  ats_score?: number
  matching_skills: string[]
  missing_skills: string[]
  experience_match?: string
  salary_match?: string
  keyword_density?: number
  recommendations: {
    resume?: string[]
    cover_letter?: string[]
    interview?: string[]
  }
  tailored_resume?: string
  tailored_cover_letter?: string
  interview_questions: string[]
  analyzed_at: string
}

export interface Application {
  id: number
  job_id: number
  status: string
  applied_date?: string
  interview_date?: string
  interview_type?: string
  follow_up_date?: string
  notes?: string
  resume_version?: string
  cover_letter_used?: string
  salary_expectation?: string
  rejection_reason?: string
  created_at: string
  updated_at: string
}

export interface UserProfile {
  id: number
  name?: string
  email?: string
  phone?: string
  linkedin_url?: string
  github_url?: string
  portfolio_url?: string
  current_title?: string
  years_experience?: number
  resume_text: string
  resume_pdf_path?: string
  preferences: {
    keywords?: string[]
    locations?: string[]
    salary_min?: number
    job_types?: string[]
  }
  target_companies: string[]
  blacklisted_companies: string[]
}

export interface DashboardStats {
  total_jobs: number
  new_today: number
  high_match_jobs: number
  total_applications: number
  active_applications: number
  last_scrape?: any
}

export interface FilterOptions {
  source?: string
  job_type?: string
  remote_type?: string
  experience_level?: string
  min_match_score?: number
  posted_after?: string
  search?: string
}
