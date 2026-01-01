import Foundation

// MARK: - Authentication Models
struct LoginRequest: Codable {
    let email: String
    let password: String
}

struct RegisterRequest: Codable {
    let email: String
    let password: String
    let username: String?
    let full_name: String?
    
    enum CodingKeys: String, CodingKey {
        case email, password, username
        case full_name
    }
}

struct TokenResponse: Codable {
    let access_token: String
    let refresh_token: String
    let token_type: String
}

struct RefreshTokenRequest: Codable {
    let refresh_token: String
}

struct UserResponse: Codable {
    let id: Int
    let email: String
    let username: String?
    let full_name: String?
    let is_active: Bool
    let is_verified: Bool
    let role: String
    let oauth_provider: String
    let created_at: String
    let updated_at: String?
}

struct OAuthRequest: Codable {
    let code: String
    let provider: String
    let redirect_uri: String?
}

// MARK: - Image Models
struct PresignUploadRequest: Codable {
    let filename: String
    let content_type: String
    let file_size: Int
}

struct PresignUploadResponse: Codable {
    let upload_url: String
    let s3_key: String
    let image_id: Int
    let expires_in: Int
}

struct ConfirmUploadRequest: Codable {
    let s3_key: String
}

// MARK: - Design Job Models
struct DesignJobCreateRequest: Codable {
    let job_type: String
    let prompt: String
    let parameters: [String: String]?
}

struct DesignJobResponse: Codable, Identifiable {
    let id: Int
    let user_id: Int
    let job_type: String
    let prompt: String
    let status: String
    let parameters: [String: String]?
    let result_urls: [String]?
    let result_metadata: [String: String]?
    let error_message: String?
    let retry_count: Int
    let max_retries: Int
    let started_at: String?
    let completed_at: String?
    let processing_time_seconds: Int?
    let queue_id: String?
    let created_at: String
    let updated_at: String?
}

struct DesignJobListResponse: Codable {
    let jobs: [DesignJobResponse]
    let total: Int
    let page: Int
    let page_size: Int
}

// MARK: - Subscription Models
struct SubscriptionStatusResponse: Codable {
    let subscription: SubscriptionResponse
    let can_use_ai_job: Bool
    let quota_info: QuotaInfo
}

struct SubscriptionResponse: Codable {
    let id: Int
    let user_id: Int
    let plan: String
    let status: String
    let billing_provider: String?
    let provider_subscription_id: String?
    let current_period_start: String?
    let current_period_end: String?
    let canceled_at: String?
    let trial_end: String?
    let ai_job_quota: Int
    let ai_jobs_used: Int
    let ai_jobs_remaining: Int
    let metadata: String?
    let created_at: String
    let updated_at: String?
}

struct QuotaInfo: Codable {
    let quota: Int
    let used: Int
    let remaining: Int
    let percentage_used: Double
}

struct CancelSubscriptionRequest: Codable {
    let reason: String?
}

struct CancelSubscriptionResponse: Codable {
    let message: String
    let subscription: SubscriptionResponse
}

// MARK: - API Error
struct APIError: Codable, Error {
    let detail: String
}



