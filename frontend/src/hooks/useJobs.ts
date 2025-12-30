/**
 * React Query hooks for jobs
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { jobsApi } from '../lib/api'
import { FilterOptions } from '../types'

export function useJobs(page: number = 1, filters: FilterOptions = {}) {
  return useQuery({
    queryKey: ['jobs', page, filters],
    queryFn: async () => {
      const response = await jobsApi.list({ page, page_size: 50, ...filters })
      return response.data
    },
  })
}

export function useJob(id: number | null) {
  return useQuery({
    queryKey: ['job', id],
    queryFn: async () => {
      if (!id) return null
      const response = await jobsApi.get(id)
      return response.data
    },
    enabled: !!id,
  })
}

export function useUpdateJob() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: any }) => jobsApi.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['jobs'] })
    },
  })
}

export function useDeleteJob() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (id: number) => jobsApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['jobs'] })
    },
  })
}
