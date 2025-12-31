package com.desiora.ai.data.repository

import com.desiora.ai.data.api.ApiClient
import com.desiora.ai.data.api.ApiService
import com.desiora.ai.data.model.*
import com.desiora.ai.data.storage.TokenStorage

class SubscriptionRepository(private val tokenStorage: TokenStorage) {
    
    private val apiService: ApiService = ApiClient.getApiService(tokenStorage)
    
    suspend fun getStatus(): Result<SubscriptionStatusResponse> {
        return try {
            val response = apiService.getSubscriptionStatus()
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception(response.message() ?: "Failed to get subscription"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun cancel(reason: String? = null): Result<CancelSubscriptionResponse> {
        return try {
            val response = apiService.cancelSubscription(CancelSubscriptionRequest(reason))
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception(response.message() ?: "Failed to cancel subscription"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}

