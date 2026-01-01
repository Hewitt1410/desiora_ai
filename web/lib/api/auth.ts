import { apiClient } from './client';

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  username?: string;
  full_name?: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface UserResponse {
  id: number;
  email: string;
  username?: string;
  full_name?: string;
  is_active: boolean;
  is_verified: boolean;
  role: 'user' | 'admin' | 'super_admin';
  oauth_provider: 'google' | 'apple' | 'email';
  created_at: string;
  updated_at?: string;
}

export interface OAuthRequest {
  code: string;
  provider: 'google' | 'apple';
  redirect_uri?: string;
}

export const authApi = {
  login: async (data: LoginRequest): Promise<TokenResponse> => {
    const response = await apiClient.post<TokenResponse>('/auth/login', data);
    apiClient.setToken(response.access_token, response.refresh_token);
    return response;
  },

  register: async (data: RegisterRequest): Promise<TokenResponse> => {
    const response = await apiClient.post<TokenResponse>('/auth/register', data);
    apiClient.setToken(response.access_token, response.refresh_token);
    return response;
  },

  googleOAuth: async (data: OAuthRequest): Promise<TokenResponse> => {
    const response = await apiClient.post<TokenResponse>('/auth/oauth/google', {
      code: data.code,
      provider: 'google',
      redirect_uri: data.redirect_uri,
    });
    apiClient.setToken(response.access_token, response.refresh_token);
    return response;
  },

  appleOAuth: async (data: OAuthRequest): Promise<TokenResponse> => {
    const response = await apiClient.post<TokenResponse>('/auth/oauth/apple', {
      code: data.code,
      provider: 'apple',
      redirect_uri: data.redirect_uri,
    });
    apiClient.setToken(response.access_token, response.refresh_token);
    return response;
  },

  getMe: async (): Promise<UserResponse> => {
    return apiClient.get<UserResponse>('/auth/me');
  },

  refreshToken: async (refreshToken: string): Promise<TokenResponse> => {
    const response = await apiClient.post<TokenResponse>('/auth/refresh', {
      refresh_token: refreshToken,
    });
    apiClient.setToken(response.access_token, response.refresh_token);
    return response;
  },
};



