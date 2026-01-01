import { apiClient } from './client';
import { UserResponse } from './auth';
import { SubscriptionResponse } from './subscriptions';
import { DesignJobResponse } from './designs';

export interface UserListResponse {
  users: UserResponse[];
  total: number;
  page: number;
  page_size: number;
}

export interface SubscriptionListResponse {
  subscriptions: SubscriptionResponse[];
  total: number;
  page: number;
  page_size: number;
}

export interface DesignJobListResponse {
  jobs: DesignJobResponse[];
  total: number;
  page: number;
  page_size: number;
}

export interface UsageStatsResponse {
  total_users: number;
  active_users: number;
  total_subscriptions: number;
  subscriptions_by_plan: Record<string, number>;
  subscriptions_by_status: Record<string, number>;
  total_jobs: number;
  jobs_by_status: Record<string, number>;
  total_ai_jobs_used: number;
  total_ai_jobs_quota: number;
  average_jobs_per_user: number;
  top_users_by_jobs: Array<{
    user_id: number;
    email: string;
    username?: string;
    job_count: number;
  }>;
}

export interface AdminStatsResponse {
  users: {
    total: number;
    active: number;
    inactive: number;
  };
  subscriptions: {
    total: number;
    by_plan: Record<string, number>;
    by_status: Record<string, number>;
  };
  jobs: {
    total: number;
    by_status: Record<string, number>;
    average_per_user: number;
  };
  usage: {
    ai_jobs_used: number;
    ai_jobs_quota: number;
    usage_percentage: number;
    top_users: Array<{
      user_id: number;
      email: string;
      username?: string;
      job_count: number;
    }>;
  };
  generated_at: string;
}

export const adminApi = {
  getUsers: async (params?: {
    page?: number;
    page_size?: number;
    role?: 'user' | 'admin' | 'super_admin';
    is_active?: boolean;
  }): Promise<UserListResponse> => {
    return apiClient.get<UserListResponse>('/admin/users', { params });
  },

  getSubscriptions: async (params?: {
    page?: number;
    page_size?: number;
    plan?: string;
    status?: string;
  }): Promise<SubscriptionListResponse> => {
    return apiClient.get<SubscriptionListResponse>('/admin/subscriptions', { params });
  },

  getJobs: async (params?: {
    page?: number;
    page_size?: number;
    status?: string;
    user_id?: number;
  }): Promise<DesignJobListResponse> => {
    return apiClient.get<DesignJobListResponse>('/admin/jobs', { params });
  },

  getStats: async (): Promise<AdminStatsResponse> => {
    return apiClient.get<AdminStatsResponse>('/admin/stats');
  },

  getUsageStats: async (): Promise<UsageStatsResponse> => {
    return apiClient.get<UsageStatsResponse>('/admin/stats/usage');
  },
};


