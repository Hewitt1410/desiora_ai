import { apiClient } from './client';

export type JobStatus = 'pending' | 'processing' | 'completed' | 'failed' | 'retrying';

export interface DesignJobCreateRequest {
  job_type: string;
  prompt: string;
  parameters?: {
    image_url: string;
    style: string;
    room_type?: string;
    [key: string]: any;
  };
}

export interface DesignJobResponse {
  id: number;
  user_id: number;
  job_type: string;
  prompt: string;
  status: JobStatus;
  parameters?: Record<string, any>;
  result_urls?: string[];
  result_metadata?: Record<string, any>;
  error_message?: string;
  retry_count: number;
  max_retries: number;
  started_at?: string;
  completed_at?: string;
  processing_time_seconds?: number;
  queue_id?: string;
  created_at: string;
  updated_at?: string;
}

export interface DesignJobListResponse {
  jobs: DesignJobResponse[];
  total: number;
  page: number;
  page_size: number;
}

export const designsApi = {
  createJob: async (data: DesignJobCreateRequest): Promise<DesignJobResponse> => {
    return apiClient.post<DesignJobResponse>('/designs', data);
  },

  getJob: async (jobId: number): Promise<DesignJobResponse> => {
    return apiClient.get<DesignJobResponse>(`/designs/${jobId}`);
  },

  listJobs: async (params?: {
    page?: number;
    page_size?: number;
    status?: JobStatus;
  }): Promise<DesignJobListResponse> => {
    return apiClient.get<DesignJobListResponse>('/designs', { params });
  },
};




