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
      console.log('✅ AI Analysis started for job', variables.jobId)
      
      // Poll for results every 3 seconds for up to 60 seconds
      let attempts = 0
      const maxAttempts = 20
      
      const pollInterval = setInterval(async () => {
        attempts++
        
        try {
          const response = await analysisApi.get(variables.jobId)
          if (response.data) {
            clearInterval(pollInterval)
            console.log('✅ Analysis complete!', response.data)
            
            // Invalidate queries to refresh UI
            queryClient.invalidateQueries({ queryKey: ['analysis', variables.jobId] })
            queryClient.invalidateQueries({ queryKey: ['jobs'] })
          }
        } catch (error) {
          // Analysis not ready yet, continue polling
          if (attempts >= maxAttempts) {
            clearInterval(pollInterval)
            console.log('⏱️ Analysis taking longer than expected, please refresh')
          }
        }
      }, 3000)
    },
    onError: (error) => {
      console.error('❌ Failed to start analysis:', error)
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
