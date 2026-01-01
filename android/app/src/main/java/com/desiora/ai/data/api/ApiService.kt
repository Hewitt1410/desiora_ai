package com.desiora.ai.data.api

import com.desiora.ai.data.model.*
import retrofit2.Response
import retrofit2.http.*

interface ApiService {
    
    // Authentication
    @POST("auth/login")
    suspend fun login(@Body request: LoginRequest): Response<TokenResponse>
    
    @POST("auth/register")
    suspend fun register(@Body request: RegisterRequest): Response<TokenResponse>
    
    @POST("auth/oauth/google")
    suspend fun googleOAuth(@Body request: OAuthRequest): Response<TokenResponse>
    
    @POST("auth/refresh")
    suspend fun refreshToken(@Body request: RefreshTokenRequest): Response<TokenResponse>
    
    @GET("auth/me")
    suspend fun getMe(): Response<UserResponse>
    
    // Images
    @POST("images/presign-upload")
    suspend fun presignUpload(@Body request: PresignUploadRequest): Response<PresignUploadResponse>
    
    @POST("images/confirm-upload")
    suspend fun confirmUpload(@Body request: ConfirmUploadRequest): Response<Map<String, String>>
    
    // Design Jobs
    @POST("designs")
    suspend fun createDesignJob(@Body request: DesignJobCreateRequest): Response<DesignJobResponse>
    
    @GET("designs/{id}")
    suspend fun getDesignJob(@Path("id") id: Int): Response<DesignJobResponse>
    
    @GET("designs")
    suspend fun listDesignJobs(
        @Query("page") page: Int = 1,
        @Query("page_size") pageSize: Int = 20,
        @Query("status") status: String? = null
    ): Response<DesignJobListResponse>
    
    // Subscriptions
    @GET("subscriptions/status")
    suspend fun getSubscriptionStatus(): Response<SubscriptionStatusResponse>
    
    @POST("subscriptions/cancel")
    suspend fun cancelSubscription(@Body request: CancelSubscriptionRequest): Response<CancelSubscriptionResponse>
    
    // Admin (if user is admin)
    @GET("admin/users")
    suspend fun getUsers(
        @Query("page") page: Int = 1,
        @Query("page_size") pageSize: Int = 20
    ): Response<UserListResponse>
    
    @GET("admin/stats")
    suspend fun getAdminStats(): Response<AdminStatsResponse>
}



