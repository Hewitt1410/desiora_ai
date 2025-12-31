import { apiClient } from './client';

export type SubscriptionPlan = 'free' | 'weekly' | 'monthly' | 'yearly';
export type SubscriptionStatus = 'active' | 'canceled' | 'expired' | 'trial' | 'past_due';

export interface SubscriptionResponse {
  id: number;
  user_id: number;
  plan: SubscriptionPlan;
  status: SubscriptionStatus;
  billing_provider?: 'stripe' | 'app_store' | 'google_play' | 'manual';
  provider_subscription_id?: string;
  current_period_start?: string;
  current_period_end?: string;
  canceled_at?: string;
  trial_end?: string;
  ai_job_quota: number;
  ai_jobs_used: number;
  ai_jobs_remaining: number;
  metadata?: string;
  created_at: string;
  updated_at?: string;
}

export interface SubscriptionStatusResponse {
  subscription: SubscriptionResponse;
  can_use_ai_job: boolean;
  quota_info: {
    quota: number;
    used: number;
    remaining: number;
    percentage_used: number;
  };
}

export interface CancelSubscriptionRequest {
  reason?: string;
}

export interface CancelSubscriptionResponse {
  message: string;
  subscription: SubscriptionResponse;
}

export const subscriptionsApi = {
  getStatus: async (): Promise<SubscriptionStatusResponse> => {
    return apiClient.get<SubscriptionStatusResponse>('/subscriptions/status');
  },

  cancel: async (data?: CancelSubscriptionRequest): Promise<CancelSubscriptionResponse> => {
    return apiClient.post<CancelSubscriptionResponse>('/subscriptions/cancel', data || {});
  },
};

