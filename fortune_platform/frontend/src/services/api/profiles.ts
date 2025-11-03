import { apiClient } from './client';
import type {
  Profile,
  CreateProfileInput,
  UpdateProfileInput,
  PaginatedResponse,
} from '@/types/api';

const PROFILES_ENDPOINT = '/api/profiles/';

export const profilesApi = {
  // Get all profiles (paginated)
  getAll: async (page = 1, pageSize = 20): Promise<PaginatedResponse<Profile>> => {
    const response = await apiClient.get<PaginatedResponse<Profile>>(
      PROFILES_ENDPOINT,
      {
        params: { page, page_size: pageSize },
      }
    );
    return response.data;
  },

  // Get single profile by ID
  getById: async (id: string): Promise<Profile> => {
    const response = await apiClient.get<Profile>(`${PROFILES_ENDPOINT}${id}/`);
    return response.data;
  },

  // Create new profile
  create: async (data: CreateProfileInput): Promise<Profile> => {
    const response = await apiClient.post<Profile>(PROFILES_ENDPOINT, data);
    return response.data;
  },

  // Update existing profile
  update: async ({ id, ...data }: UpdateProfileInput): Promise<Profile> => {
    const response = await apiClient.put<Profile>(
      `${PROFILES_ENDPOINT}${id}/`,
      data
    );
    return response.data;
  },

  // Partial update profile
  patch: async ({ id, ...data }: UpdateProfileInput): Promise<Profile> => {
    const response = await apiClient.patch<Profile>(
      `${PROFILES_ENDPOINT}${id}/`,
      data
    );
    return response.data;
  },

  // Delete profile
  delete: async (id: string): Promise<void> => {
    await apiClient.delete(`${PROFILES_ENDPOINT}${id}/`);
  },
};
