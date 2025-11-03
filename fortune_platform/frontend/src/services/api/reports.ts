import { apiClient } from './client';
import { sanitizeHTML } from '@/utils/sanitize';
import type { Report, ReportContent, PaginatedResponse } from '@/types/api';

const REPORTS_ENDPOINT = '/api/analysis/reports/';

export const reportsApi = {
  // Get all reports (paginated)
  getAll: async (
    page = 1,
    pageSize = 20
  ): Promise<PaginatedResponse<Report>> => {
    const response = await apiClient.get<PaginatedResponse<Report>>(
      REPORTS_ENDPOINT,
      {
        params: { page, page_size: pageSize },
      }
    );
    return response.data;
  },

  // Get single report metadata by ID
  getById: async (id: string): Promise<Report> => {
    const response = await apiClient.get<Report>(`${REPORTS_ENDPOINT}${id}/`);
    return response.data;
  },

  // Get report HTML content (sanitized)
  getContent: async (id: string): Promise<ReportContent> => {
    const response = await apiClient.get<ReportContent>(
      `${REPORTS_ENDPOINT}${id}/html/`
    );

    // Sanitize HTML content before returning
    return {
      ...response.data,
      html_content: sanitizeHTML(response.data.html_content),
    };
  },

  // Get reports for a specific profile
  getByProfileId: async (profileId: string): Promise<Report[]> => {
    const response = await apiClient.get<Report[]>(REPORTS_ENDPOINT, {
      params: { profile_id: profileId },
    });
    return response.data;
  },

  // Get reports for a specific job
  getByJobId: async (jobId: string): Promise<Report[]> => {
    const response = await apiClient.get<Report[]>(REPORTS_ENDPOINT, {
      params: { job_id: jobId },
    });
    return response.data;
  },

  // Download report as PDF (if backend supports)
  downloadPdf: async (id: string): Promise<Blob> => {
    const response = await apiClient.get(`${REPORTS_ENDPOINT}${id}/pdf/`, {
      responseType: 'blob',
    });
    return response.data;
  },

  // Download report as HTML
  downloadHtml: async (id: string): Promise<Blob> => {
    const response = await apiClient.get(`${REPORTS_ENDPOINT}${id}/html/`, {
      responseType: 'blob',
    });
    return response.data;
  },
};
