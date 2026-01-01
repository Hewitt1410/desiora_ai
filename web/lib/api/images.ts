import { apiClient } from './client';

export interface PresignUploadRequest {
  filename: string;
  content_type: string;
  file_size: number;
}

export interface PresignUploadResponse {
  upload_url: string;
  s3_key: string;
  image_id: number;
  expires_in: number;
}

export interface ImageCreateRequest {
  s3_key: string;
  filename: string;
  original_filename: string;
  content_type: string;
  file_size: number;
  metadata?: Record<string, any>;
}

export interface ImageResponse {
  id: number;
  user_id: number;
  filename: string;
  original_filename: string;
  content_type: string;
  file_type: 'jpg' | 'jpeg' | 'png' | 'heic';
  file_size: number;
  s3_key: string;
  s3_bucket: string;
  s3_url?: string;
  status: 'pending' | 'uploaded' | 'failed';
  metadata?: string;
  created_at: string;
  updated_at?: string;
}

export const imagesApi = {
  presignUpload: async (data: PresignUploadRequest): Promise<PresignUploadResponse> => {
    return apiClient.post<PresignUploadResponse>('/images/presign-upload', data);
  },

  createImage: async (data: ImageCreateRequest): Promise<ImageResponse> => {
    return apiClient.post<ImageResponse>('/images', data);
  },

  confirmUpload: async (s3Key: string): Promise<{ message: string }> => {
    return apiClient.post('/images/confirm-upload', { s3_key: s3Key });
  },
};




