package com.desiora.ai.data.repository

import com.desiora.ai.data.api.ApiClient
import com.desiora.ai.data.api.ApiService
import com.desiora.ai.data.model.*
import com.desiora.ai.data.storage.TokenStorage
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.asRequestBody
import java.io.File

class ImageRepository(private val tokenStorage: TokenStorage) {
    
    private val apiService: ApiService = ApiClient.getApiService(tokenStorage)
    private val okHttpClient = OkHttpClient()
    
    suspend fun uploadImage(imageFile: File): Result<String> {
        return try {
            // Step 1: Get presigned URL
            val presignRequest = PresignUploadRequest(
                filename = imageFile.name,
                contentType = "image/jpeg",
                fileSize = imageFile.length()
            )
            val presignResponse = apiService.presignUpload(presignRequest)
            
            if (!presignResponse.isSuccessful || presignResponse.body() == null) {
                return Result.failure(Exception("Failed to get upload URL"))
            }
            
            val presignData = presignResponse.body()!!
            
            // Step 2: Upload to S3
            val requestBody = imageFile.asRequestBody("image/jpeg".toMediaType())
            val uploadRequest = Request.Builder()
                .url(presignData.uploadUrl)
                .put(requestBody)
                .build()
            
            val uploadResponse = okHttpClient.newCall(uploadRequest).execute()
            
            if (!uploadResponse.isSuccessful) {
                return Result.failure(Exception("Failed to upload image"))
            }
            
            // Step 3: Confirm upload
            val confirmResponse = apiService.confirmUpload(ConfirmUploadRequest(presignData.s3Key))
            
            if (!confirmResponse.isSuccessful) {
                return Result.failure(Exception("Failed to confirm upload"))
            }
            
            Result.success(presignData.s3Key)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}


