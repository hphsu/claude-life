import { useQuery } from '@tanstack/react-query';
import { useState, useEffect } from 'react';

export interface JobStatus {
  id: string;
  status: 'queued' | 'processing' | 'completed' | 'failed';
  progress: number;
  message?: string;
  result?: any;
  error?: string;
  createdAt: string;
  updatedAt: string;
}

/**
 * Hook to fetch and monitor job status
 * @param jobId - The ID of the job to monitor
 * @param options - Query options
 * @returns Job status data and query state
 */
export function useJobStatus(
  jobId: string | null,
  options?: {
    refetchInterval?: number;
    enabled?: boolean;
  }
) {
  const [pollingEnabled, setPollingEnabled] = useState(true);

  const query = useQuery({
    queryKey: ['jobStatus', jobId],
    queryFn: async (): Promise<JobStatus> => {
      if (!jobId) {
        throw new Error('Job ID is required');
      }

      const response = await fetch(`/api/jobs/${jobId}/status`);

      if (!response.ok) {
        throw new Error('Failed to fetch job status');
      }

      return response.json();
    },
    enabled: !!jobId && (options?.enabled ?? true) && pollingEnabled,
    refetchInterval: (data) => {
      // Stop polling if job is completed or failed
      if (data?.status === 'completed' || data?.status === 'failed') {
        setPollingEnabled(false);
        return false;
      }
      // Poll every 2 seconds for active jobs
      return options?.refetchInterval ?? 2000;
    },
    retry: 3,
    retryDelay: 1000,
  });

  // Reset polling when jobId changes
  useEffect(() => {
    if (jobId) {
      setPollingEnabled(true);
    }
  }, [jobId]);

  return {
    ...query,
    status: query.data?.status,
    progress: query.data?.progress ?? 0,
    message: query.data?.message,
    result: query.data?.result,
    error: query.data?.error,
    isQueued: query.data?.status === 'queued',
    isProcessing: query.data?.status === 'processing',
    isCompleted: query.data?.status === 'completed',
    isFailed: query.data?.status === 'failed',
  };
}

/**
 * Hook to monitor multiple jobs
 * @param jobIds - Array of job IDs to monitor
 * @returns Map of job statuses
 */
export function useMultipleJobStatus(jobIds: string[]) {
  const queries = useQuery({
    queryKey: ['multipleJobStatus', jobIds],
    queryFn: async (): Promise<Record<string, JobStatus>> => {
      const promises = jobIds.map(async (jobId) => {
        const response = await fetch(`/api/jobs/${jobId}/status`);
        if (!response.ok) {
          throw new Error(`Failed to fetch job ${jobId}`);
        }
        const data = await response.json();
        return [jobId, data] as [string, JobStatus];
      });

      const results = await Promise.all(promises);
      return Object.fromEntries(results);
    },
    enabled: jobIds.length > 0,
    refetchInterval: 2000,
  });

  return queries;
}
