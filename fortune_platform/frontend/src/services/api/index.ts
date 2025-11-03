// Export API client and helpers
export { apiClient, getErrorMessage, setAuthToken, getAuthToken, clearAuthToken, isAuthenticated } from './client';

// Export API services
export { profilesApi } from './profiles';
export { ordersApi } from './orders';
export { jobsApi } from './jobs';
export { reportsApi } from './reports';

// Export types
export type { ApiError } from './client';
