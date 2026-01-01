package com.desiora.ai.data.model

import com.google.gson.annotations.SerializedName

// Authentication Models
data class LoginRequest(
    val email: String,
    val password: String
)

data class RegisterRequest(
    val email: String,
    val password: String,
    val username: String? = null,
    val full_name: String? = null
)

data class TokenResponse(
    @SerializedName("access_token") val accessToken: String,
    @SerializedName("refresh_token") val refreshToken: String,
    @SerializedName("token_type") val tokenType: String = "bearer"
)

data class RefreshTokenRequest(
    @SerializedName("refresh_token") val refreshToken: String
)

data class UserResponse(
    val id: Int,
    val email: String,
    val username: String?,
    @SerializedName("full_name") val fullName: String?,
    @SerializedName("is_active") val isActive: Boolean,
    @SerializedName("is_verified") val isVerified: Boolean,
    val role: String,
    @SerializedName("oauth_provider") val oauthProvider: String,
    @SerializedName("created_at") val createdAt: String,
    @SerializedName("updated_at") val updatedAt: String?
)

data class OAuthRequest(
    val code: String,
    val provider: String,
    @SerializedName("redirect_uri") val redirectUri: String? = null
)

// Image Models
data class PresignUploadRequest(
    val filename: String,
    @SerializedName("content_type") val contentType: String,
    @SerializedName("file_size") val fileSize: Long
)

data class PresignUploadResponse(
    @SerializedName("upload_url") val uploadUrl: String,
    @SerializedName("s3_key") val s3Key: String,
    @SerializedName("image_id") val imageId: Int,
    @SerializedName("expires_in") val expiresIn: Int
)

data class ConfirmUploadRequest(
    @SerializedName("s3_key") val s3Key: String
)

// Design Job Models
data class DesignJobCreateRequest(
    @SerializedName("job_type") val jobType: String,
    val prompt: String,
    val parameters: Map<String, Any>? = null
)

data class DesignJobResponse(
    val id: Int,
    @SerializedName("user_id") val userId: Int,
    @SerializedName("job_type") val jobType: String,
    val prompt: String,
    val status: String,
    val parameters: Map<String, Any>?,
    @SerializedName("result_urls") val resultUrls: List<String>?,
    @SerializedName("result_metadata") val resultMetadata: Map<String, Any>?,
    @SerializedName("error_message") val errorMessage: String?,
    @SerializedName("retry_count") val retryCount: Int,
    @SerializedName("max_retries") val maxRetries: Int,
    @SerializedName("started_at") val startedAt: String?,
    @SerializedName("completed_at") val completedAt: String?,
    @SerializedName("processing_time_seconds") val processingTimeSeconds: Int?,
    @SerializedName("queue_id") val queueId: String?,
    @SerializedName("created_at") val createdAt: String,
    @SerializedName("updated_at") val updatedAt: String?
)

data class DesignJobListResponse(
    val jobs: List<DesignJobResponse>,
    val total: Int,
    val page: Int,
    @SerializedName("page_size") val pageSize: Int
)

// Subscription Models
data class SubscriptionStatusResponse(
    val subscription: SubscriptionResponse,
    @SerializedName("can_use_ai_job") val canUseAiJob: Boolean,
    @SerializedName("quota_info") val quotaInfo: QuotaInfo
)

data class SubscriptionResponse(
    val id: Int,
    @SerializedName("user_id") val userId: Int,
    val plan: String,
    val status: String,
    @SerializedName("billing_provider") val billingProvider: String?,
    @SerializedName("provider_subscription_id") val providerSubscriptionId: String?,
    @SerializedName("current_period_start") val currentPeriodStart: String?,
    @SerializedName("current_period_end") val currentPeriodEnd: String?,
    @SerializedName("canceled_at") val canceledAt: String?,
    @SerializedName("trial_end") val trialEnd: String?,
    @SerializedName("ai_job_quota") val aiJobQuota: Int,
    @SerializedName("ai_jobs_used") val aiJobsUsed: Int,
    @SerializedName("ai_jobs_remaining") val aiJobsRemaining: Int,
    val metadata: String?,
    @SerializedName("created_at") val createdAt: String,
    @SerializedName("updated_at") val updatedAt: String?
)

data class QuotaInfo(
    val quota: Int,
    val used: Int,
    val remaining: Int,
    @SerializedName("percentage_used") val percentageUsed: Double
)

data class CancelSubscriptionRequest(
    val reason: String? = null
)

data class CancelSubscriptionResponse(
    val message: String,
    val subscription: SubscriptionResponse
)

// Admin Models
data class UserListResponse(
    val users: List<UserResponse>,
    val total: Int,
    val page: Int,
    @SerializedName("page_size") val pageSize: Int
)

data class AdminStatsResponse(
    val users: UserStats,
    val subscriptions: SubscriptionStats,
    val jobs: JobStats,
    val usage: UsageStats,
    @SerializedName("generated_at") val generatedAt: String
)

data class UserStats(
    val total: Int,
    val active: Int,
    val inactive: Int
)

data class SubscriptionStats(
    val total: Int,
    @SerializedName("by_plan") val byPlan: Map<String, Int>,
    @SerializedName("by_status") val byStatus: Map<String, Int>
)

data class JobStats(
    val total: Int,
    @SerializedName("by_status") val byStatus: Map<String, Int>,
    @SerializedName("average_per_user") val averagePerUser: Double
)

data class UsageStats(
    @SerializedName("ai_jobs_used") val aiJobsUsed: Int,
    @SerializedName("ai_jobs_quota") val aiJobsQuota: Int,
    @SerializedName("usage_percentage") val usagePercentage: Double,
    @SerializedName("top_users") val topUsers: List<TopUser>
)

data class TopUser(
    @SerializedName("user_id") val userId: Int,
    val email: String,
    val username: String?,
    @SerializedName("job_count") val jobCount: Int
)




