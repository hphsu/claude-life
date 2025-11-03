import { useQuery, useMutation } from '@tanstack/react-query';
import { reportsApi } from '@/services/api';
import { getErrorMessage } from '@/services/api/client';
import type { Report, ReportContent } from '@/types/api';

// Query keys
export const reportKeys = {
  all: ['reports'] as const,
  lists: () => [...reportKeys.all, 'list'] as const,
  list: (page: number) => [...reportKeys.lists(), { page }] as const,
  details: () => [...reportKeys.all, 'detail'] as const,
  detail: (id: string) => [...reportKeys.details(), id] as const,
  content: (id: string) => [...reportKeys.detail(id), 'content'] as const,
  byProfile: (profileId: string) => [...reportKeys.all, 'by-profile', profileId] as const,
  byJob: (jobId: string) => [...reportKeys.all, 'by-job', jobId] as const,
};

// Get all reports
export const useReports = (page = 1, pageSize = 20) => {
  return useQuery({
    queryKey: reportKeys.list(page),
    queryFn: () => reportsApi.getAll(page, pageSize),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

// Get single report metadata
export const useReport = (id: string | undefined) => {
  return useQuery({
    queryKey: reportKeys.detail(id!),
    queryFn: () => reportsApi.getById(id!),
    enabled: !!id,
    staleTime: 5 * 60 * 1000,
  });
};

// Get report HTML content (sanitized)
export const useReportContent = (id: string | undefined) => {
  return useQuery({
    queryKey: reportKeys.content(id!),
    queryFn: () => reportsApi.getContent(id!),
    enabled: !!id,
    staleTime: 10 * 60 * 1000, // 10 minutes - content rarely changes
  });
};

// Get reports for a specific profile
export const useProfileReports = (profileId: string | undefined) => {
  return useQuery({
    queryKey: reportKeys.byProfile(profileId!),
    queryFn: () => reportsApi.getByProfileId(profileId!),
    enabled: !!profileId,
    staleTime: 5 * 60 * 1000,
  });
};

// Get reports for a specific job
export const useJobReports = (jobId: string | undefined) => {
  return useQuery({
    queryKey: reportKeys.byJob(jobId!),
    queryFn: () => reportsApi.getByJobId(jobId!),
    enabled: !!jobId,
    staleTime: 5 * 60 * 1000,
  });
};

// Download report as PDF
export const useDownloadPdf = () => {
  return useMutation({
    mutationFn: async (id: string) => {
      const blob = await reportsApi.downloadPdf(id);
      // Create download link
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `report-${id}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    },
    onError: (error) => {
      console.error('Failed to download PDF:', getErrorMessage(error));
    },
  });
};

// Download report as HTML
export const useDownloadHtml = () => {
  return useMutation({
    mutationFn: async (id: string) => {
      const blob = await reportsApi.downloadHtml(id);
      // Create download link
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `report-${id}.html`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    },
    onError: (error) => {
      console.error('Failed to download HTML:', getErrorMessage(error));
    },
  });
};
