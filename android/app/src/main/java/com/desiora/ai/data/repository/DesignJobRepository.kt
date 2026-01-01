package com.desiora.ai.data.repository

import com.desiora.ai.data.api.ApiClient
import com.desiora.ai.data.api.ApiService
import com.desiora.ai.data.model.*
import com.desiora.ai.data.storage.TokenStorage

class DesignJobRepository(private val tokenStorage: TokenStorage) {
    
    private val apiService: ApiService = ApiClient.getApiService(tokenStorage)
    
    suspend fun createJob(
        jobType: String,
        prompt: String,
        imageUrl: String,
        style: String,
        roomType: String?
    ): Result<DesignJobResponse> {
        return try {
            val parameters = mapOf(
                "image_url" to imageUrl,
                "style" to style,
                "room_type" to (roomType ?: "living_room")
            )
            val request = DesignJobCreateRequest(jobType, prompt, parameters)
            val response = apiService.createDesignJob(request)
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception(response.message() ?: "Failed to create job"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun getJob(jobId: Int): Result<DesignJobResponse> {
        return try {
            val response = apiService.getDesignJob(jobId)
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception(response.message() ?: "Failed to get job"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun listJobs(page: Int = 1, pageSize: Int = 20, status: String? = null): Result<DesignJobListResponse> {
        return try {
            val response = apiService.listDesignJobs(page, pageSize, status)
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception(response.message() ?: "Failed to list jobs"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}


