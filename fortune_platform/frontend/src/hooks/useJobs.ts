import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { jobsApi } from '@/services/api';
import { getErrorMessage } from '@/services/api/client';
import type { Job, JobStatus } from '@/types/api';

// Query keys
export const jobKeys = {
  all: ['jobs'] as const,
  lists: () => [...jobKeys.all, 'list'] as const,
  list: (page: number) => [...jobKeys.lists(), { page }] as const,
  details: () => [...jobKeys.all, 'detail'] as const,
  detail: (id: string) => [...jobKeys.details(), id] as const,
  status: (id: string) => [...jobKeys.detail(id), 'status'] as const,
  byOrder: (orderId: string) => [...jobKeys.all, 'by-order', orderId] as const,
};

// Get all jobs
export const useJobs = (page = 1, pageSize = 20) => {
  return useQuery({
    queryKey: jobKeys.list(page),
    queryFn: () => jobsApi.getAll(page, pageSize),
    staleTime: 30 * 1000, // 30 seconds - jobs change frequently
  });
};

// Get single job by ID
export const useJob = (id: string | undefined) => {
  return useQuery({
    queryKey: jobKeys.detail(id!),
    queryFn: () => jobsApi.getById(id!),
    enabled: !!id,
    staleTime: 30 * 1000,
  });
};

// Get job status and progress (with polling)
export const useJobStatus = (
  id: string | undefined,
  options?: {
    refetchInterval?: number | false;
    enabled?: boolean;
  }
) => {
  return useQuery({
    queryKey: jobKeys.status(id!),
    queryFn: () => jobsApi.getStatus(id!),
    enabled: !!id && (options?.enabled !== false),
    staleTime: 0, // Always refetch
    refetchInterval: options?.refetchInterval ?? 5000, // Poll every 5 seconds by default
  });
};

// Get jobs for a specific order (with polling)
export const useOrderJobs = (
  orderId: string | undefined,
  options?: {
    refetchInterval?: number | false;
    enabled?: boolean;
  }
) => {
  return useQuery({
    queryKey: jobKeys.byOrder(orderId!),
    queryFn: () => jobsApi.getByOrderId(orderId!),
    enabled: !!orderId && (options?.enabled !== false),
    staleTime: 0,
    refetchInterval: options?.refetchInterval ?? 5000,
  });
};

// Cancel a running job
export const useCancelJob = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: string) => jobsApi.cancel(id),
    onSuccess: (_, id) => {
      // Invalidate job queries to refetch
      queryClient.invalidateQueries({ queryKey: jobKeys.detail(id) });
      queryClient.invalidateQueries({ queryKey: jobKeys.status(id) });
      queryClient.invalidateQueries({ queryKey: jobKeys.lists() });
    },
    onError: (error) => {
      console.error('Failed to cancel job:', getErrorMessage(error));
    },
  });
};
