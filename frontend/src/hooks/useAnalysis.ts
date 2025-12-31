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
    refetchOnWindowFocus: true, // Refetch when window regains focus
    staleTime: 0, // Always consider data stale so it refetches
  })
}

export function useAnalyzeJob() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ jobId, generateMaterials = true }: { jobId: number; generateMaterials?: boolean }) =>
      analysisApi.analyzeJob(jobId, generateMaterials),
    onSuccess: (_, variables) => {
      console.log('✅ AI Analysis API call successful for job', variables.jobId)
      
      // Aggressively poll for results every 2 seconds for up to 60 seconds
      let attempts = 0
      const maxAttempts = 30
      
      const pollInterval = setInterval(async () => {
        attempts++
        console.log(`🔄 Polling attempt ${attempts}/${maxAttempts}...`)
        
        try {
          const response = await analysisApi.get(variables.jobId)
          if (response.data && (response.data.tailored_resume || response.data.ats_score > 0)) {
            clearInterval(pollInterval)
            console.log('✅ Full analysis complete!', response.data)
            
            // Force refetch by invalidating and refetching
            await queryClient.invalidateQueries({ queryKey: ['analysis', variables.jobId] })
            await queryClient.refetchQueries({ queryKey: ['analysis', variables.jobId] })
            await queryClient.invalidateQueries({ queryKey: ['jobs'] })
            
            console.log('✅ UI refreshed with analysis results')
          } else {
            console.log('⏳ Analysis in progress, waiting...')
          }
        } catch (error) {
          // Analysis not ready yet, continue polling
          console.log('⏳ Analysis not ready, continuing to poll...')
          if (attempts >= maxAttempts) {
            clearInterval(pollInterval)
            console.log('⏱️ Analysis taking longer than expected (60s). Please close and reopen the job.')
          }
        }
      }, 2000) // Poll every 2 seconds
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
