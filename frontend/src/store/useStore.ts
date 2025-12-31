/**
 * Global state management using Zustand
 */
import { create } from 'zustand'
import { Job, FilterOptions } from '../types'

interface AppState {
  // Selected job
  selectedJob: Job | null
  setSelectedJob: (job: Job | null) => void

  // Filters
  filters: FilterOptions
  setFilters: (filters: FilterOptions) => void
  removeFilter: (key: keyof FilterOptions) => void
  resetFilters: () => void

  // UI state
  sidebarOpen: boolean
  setSidebarOpen: (open: boolean) => void

  // Job detail modal
  jobDetailModalOpen: boolean
  setJobDetailModalOpen: (open: boolean) => void
}

export const useStore = create<AppState>((set) => ({
  // Selected job
  selectedJob: null,
  setSelectedJob: (job) => set({ selectedJob: job }),

  // Filters
  filters: {},
  setFilters: (filters) => set((state) => ({ filters: { ...state.filters, ...filters } })),
  removeFilter: (key) => set((state) => {
    const newFilters = { ...state.filters }
    delete newFilters[key]
    return { filters: newFilters }
  }),
  resetFilters: () => set({ filters: {} }),

  // UI state
  sidebarOpen: true,
  setSidebarOpen: (open) => set({ sidebarOpen: open }),

  // Job detail modal
  jobDetailModalOpen: false,
  setJobDetailModalOpen: (open) => set({ jobDetailModalOpen: open }),
}))
