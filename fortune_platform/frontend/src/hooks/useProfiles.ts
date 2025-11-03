import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { profilesApi } from '@/services/api';
import { getErrorMessage } from '@/services/api/client';
import type {
  Profile,
  CreateProfileInput,
  UpdateProfileInput,
} from '@/types/api';

// Query keys
export const profileKeys = {
  all: ['profiles'] as const,
  lists: () => [...profileKeys.all, 'list'] as const,
  list: (page: number) => [...profileKeys.lists(), { page }] as const,
  details: () => [...profileKeys.all, 'detail'] as const,
  detail: (id: string) => [...profileKeys.details(), id] as const,
};

// Get all profiles
export const useProfiles = (page = 1, pageSize = 20) => {
  return useQuery({
    queryKey: profileKeys.list(page),
    queryFn: () => profilesApi.getAll(page, pageSize),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

// Get single profile
export const useProfile = (id: string | undefined) => {
  return useQuery({
    queryKey: profileKeys.detail(id!),
    queryFn: () => profilesApi.getById(id!),
    enabled: !!id, // Only fetch if ID is provided
    staleTime: 5 * 60 * 1000,
  });
};

// Create profile mutation
export const useCreateProfile = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateProfileInput) => profilesApi.create(data),
    onSuccess: () => {
      // Invalidate profiles list to refetch
      queryClient.invalidateQueries({ queryKey: profileKeys.lists() });
    },
    onError: (error) => {
      console.error('Failed to create profile:', getErrorMessage(error));
    },
  });
};

// Update profile mutation
export const useUpdateProfile = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: UpdateProfileInput) => profilesApi.update(data),
    onSuccess: (data) => {
      // Invalidate and update cache
      queryClient.invalidateQueries({ queryKey: profileKeys.lists() });
      queryClient.setQueryData(profileKeys.detail(data.id), data);
    },
    onError: (error) => {
      console.error('Failed to update profile:', getErrorMessage(error));
    },
  });
};

// Delete profile mutation
export const useDeleteProfile = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: string) => profilesApi.delete(id),
    onSuccess: (_, id) => {
      // Invalidate lists and remove from cache
      queryClient.invalidateQueries({ queryKey: profileKeys.lists() });
      queryClient.removeQueries({ queryKey: profileKeys.detail(id) });
    },
    onError: (error) => {
      console.error('Failed to delete profile:', getErrorMessage(error));
    },
  });
};
