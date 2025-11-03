/**
 * Authentication service for JWT-based authentication with Django backend.
 * Handles login, registration, token management, and user profile operations.
 */
import { apiClient } from '../api/client';

export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  date_joined: string;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface LoginResponse {
  access: string;
  refresh: string;
}

export interface RegisterResponse {
  user: User;
  tokens: AuthTokens;
  message: string;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
  password2: string;
  first_name?: string;
  last_name?: string;
}

const TOKEN_KEY = 'auth_tokens';
const USER_KEY = 'auth_user';

/**
 * Token Storage Utilities
 */
export const tokenStorage = {
  getTokens(): AuthTokens | null {
    const tokens = localStorage.getItem(TOKEN_KEY);
    return tokens ? JSON.parse(tokens) : null;
  },

  setTokens(tokens: AuthTokens): void {
    localStorage.setItem(TOKEN_KEY, JSON.stringify(tokens));
  },

  clearTokens(): void {
    localStorage.removeItem(TOKEN_KEY);
  },

  getAccessToken(): string | null {
    const tokens = this.getTokens();
    return tokens?.access || null;
  },

  getRefreshToken(): string | null {
    const tokens = this.getTokens();
    return tokens?.refresh || null;
  },
};

/**
 * User Storage Utilities
 */
export const userStorage = {
  getUser(): User | null {
    const user = localStorage.getItem(USER_KEY);
    return user ? JSON.parse(user) : null;
  },

  setUser(user: User): void {
    localStorage.setItem(USER_KEY, JSON.stringify(user));
  },

  clearUser(): void {
    localStorage.removeItem(USER_KEY);
  },
};

/**
 * Authentication Service
 */
export const authService = {
  /**
   * Login user with username and password
   */
  async login(username: string, password: string): Promise<{ user: User; tokens: AuthTokens }> {
    const response = await apiClient.post<LoginResponse>('/auth/login/', {
      username,
      password,
    });

    const tokens: AuthTokens = {
      access: response.data.access,
      refresh: response.data.refresh,
    };

    // Store tokens
    tokenStorage.setTokens(tokens);

    // Fetch and store user profile
    const user = await this.getCurrentUser();
    userStorage.setUser(user);

    return { user, tokens };
  },

  /**
   * Register new user
   */
  async register(data: RegisterData): Promise<{ user: User; tokens: AuthTokens }> {
    const response = await apiClient.post<RegisterResponse>('/auth/register/', data);

    const tokens = response.data.tokens;
    const user = response.data.user;

    // Store tokens and user
    tokenStorage.setTokens(tokens);
    userStorage.setUser(user);

    return { user, tokens };
  },

  /**
   * Logout user and blacklist refresh token
   */
  async logout(): Promise<void> {
    const refreshToken = tokenStorage.getRefreshToken();

    if (refreshToken) {
      try {
        await apiClient.post('/auth/logout/', {
          refresh: refreshToken,
        });
      } catch (error) {
        // Continue with logout even if blacklist fails
        console.error('Failed to blacklist token:', error);
      }
    }

    // Clear local storage
    tokenStorage.clearTokens();
    userStorage.clearUser();
  },

  /**
   * Refresh access token using refresh token
   */
  async refreshAccessToken(): Promise<string> {
    const refreshToken = tokenStorage.getRefreshToken();

    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    const response = await apiClient.post<{ access: string; refresh?: string }>('/auth/refresh/', {
      refresh: refreshToken,
    });

    const tokens = tokenStorage.getTokens();
    if (tokens) {
      tokens.access = response.data.access;
      // Update refresh token if rotation is enabled
      if (response.data.refresh) {
        tokens.refresh = response.data.refresh;
      }
      tokenStorage.setTokens(tokens);
    }

    return response.data.access;
  },

  /**
   * Verify if token is valid
   */
  async verifyToken(token: string): Promise<boolean> {
    try {
      await apiClient.post('/auth/verify/', { token });
      return true;
    } catch (error) {
      return false;
    }
  },

  /**
   * Get current user profile
   */
  async getCurrentUser(): Promise<User> {
    const response = await apiClient.get<User>('/auth/me/');
    return response.data;
  },

  /**
   * Update current user profile
   */
  async updateUser(data: Partial<User>): Promise<User> {
    const response = await apiClient.patch<User>('/auth/me/', data);
    const user = response.data;
    userStorage.setUser(user);
    return user;
  },

  /**
   * Change password
   */
  async changePassword(oldPassword: string, newPassword: string): Promise<void> {
    await apiClient.post('/auth/change-password/', {
      old_password: oldPassword,
      new_password: newPassword,
    });
  },

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    const tokens = tokenStorage.getTokens();
    return !!tokens?.access;
  },

  /**
   * Initialize auth state from storage
   */
  initializeAuth(): { user: User | null; tokens: AuthTokens | null } {
    return {
      user: userStorage.getUser(),
      tokens: tokenStorage.getTokens(),
    };
  },
};
