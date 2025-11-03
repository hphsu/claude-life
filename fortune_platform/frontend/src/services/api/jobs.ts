import { apiClient } from './client';
import type { Job, JobStatus, PaginatedResponse } from '@/types/api';

const JOBS_ENDPOINT = '/api/analysis/jobs/';

export const jobsApi = {
  // Get all jobs (paginated)
  getAll: async (page = 1, pageSize = 20): Promise<PaginatedResponse<Job>> => {
    const response = await apiClient.get<PaginatedResponse<Job>>(
      JOBS_ENDPOINT,
      {
        params: { page, page_size: pageSize },
      }
    );
    return response.data;
  },

  // Get single job by ID
  getById: async (id: string): Promise<Job> => {
    const response = await apiClient.get<Job>(`${JOBS_ENDPOINT}${id}/`);
    return response.data;
  },

  // Get job status and progress
  getStatus: async (id: string): Promise<JobStatus> => {
    const response = await apiClient.get<JobStatus>(
      `${JOBS_ENDPOINT}${id}/status/`
    );
    return response.data;
  },

  // Get jobs for a specific order
  getByOrderId: async (orderId: string): Promise<Job[]> => {
    const response = await apiClient.get<Job[]>(JOBS_ENDPOINT, {
      params: { order_id: orderId },
    });
    return response.data;
  },

  // Cancel a running job
  cancel: async (id: string): Promise<void> => {
    await apiClient.post(`${JOBS_ENDPOINT}${id}/cancel/`);
  },
};
