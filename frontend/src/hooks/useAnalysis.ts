/**
 * React Query hooks for AI analysis
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { analysisApi } from '../lib/api'

export function useAnalysis(jobId: number | null) {
  return useQuery({
    queryKey: ['analysis', jobId],
    queryFn: async () => {
      if (!jobId) return null
      const response = await analysisApi.get(jobId)
      return response.data
    },
    enabled: !!jobId,
    retry: false, // Don't retry if analysis doesn't exist
  })
}

export function useAnalyzeJob() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ jobId, generateMaterials = true }: { jobId: number; generateMaterials?: boolean }) =>
      analysisApi.analyzeJob(jobId, generateMaterials),
    onSuccess: (_, variables) => {
      // Invalidate analysis query after a delay to allow background processing
      setTimeout(() => {
        queryClient.invalidateQueries({ queryKey: ['analysis', variables.jobId] })
      }, 3000)
    },
  })
}

export function useInterviewPrep(jobId: number | null) {
  return useQuery({
    queryKey: ['interview-prep', jobId],
    queryFn: async () => {
      if (!jobId) return null
      const response = await analysisApi.getInterviewPrep(jobId)
      return response.data
    },
    enabled: !!jobId,
  })
}
