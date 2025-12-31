package com.desiora.ai.data.repository

import com.desiora.ai.data.api.ApiClient
import com.desiora.ai.data.api.ApiService
import com.desiora.ai.data.model.*
import com.desiora.ai.data.storage.TokenStorage

class AuthRepository(private val tokenStorage: TokenStorage) {
    
    private val apiService: ApiService = ApiClient.getApiService(tokenStorage)
    
    suspend fun login(email: String, password: String): Result<UserResponse> {
        return try {
            val response = apiService.login(LoginRequest(email, password))
            if (response.isSuccessful && response.body() != null) {
                val tokenResponse = response.body()!!
                tokenStorage.saveTokens(tokenResponse.accessToken, tokenResponse.refreshToken)
                val userResponse = apiService.getMe()
                if (userResponse.isSuccessful && userResponse.body() != null) {
                    Result.success(userResponse.body()!!)
                } else {
                    Result.failure(Exception("Failed to get user info"))
                }
            } else {
                Result.failure(Exception(response.message() ?: "Login failed"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun register(email: String, password: String, username: String?): Result<UserResponse> {
        return try {
            val response = apiService.register(RegisterRequest(email, password, username))
            if (response.isSuccessful && response.body() != null) {
                val tokenResponse = response.body()!!
                tokenStorage.saveTokens(tokenResponse.accessToken, tokenResponse.refreshToken)
                val userResponse = apiService.getMe()
                if (userResponse.isSuccessful && userResponse.body() != null) {
                    Result.success(userResponse.body()!!)
                } else {
                    Result.failure(Exception("Failed to get user info"))
                }
            } else {
                Result.failure(Exception(response.message() ?: "Registration failed"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun googleOAuth(code: String, redirectUri: String?): Result<UserResponse> {
        return try {
            val response = apiService.googleOAuth(OAuthRequest(code, "google", redirectUri))
            if (response.isSuccessful && response.body() != null) {
                val tokenResponse = response.body()!!
                tokenStorage.saveTokens(tokenResponse.accessToken, tokenResponse.refreshToken)
                val userResponse = apiService.getMe()
                if (userResponse.isSuccessful && userResponse.body() != null) {
                    Result.success(userResponse.body()!!)
                } else {
                    Result.failure(Exception("Failed to get user info"))
                }
            } else {
                Result.failure(Exception(response.message() ?: "OAuth failed"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun getCurrentUser(): Result<UserResponse> {
        return try {
            val response = apiService.getMe()
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception(response.message() ?: "Failed to get user"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    fun logout() {
        tokenStorage.clearTokens()
        ApiClient.reset()
    }
    
    fun isLoggedIn(): Boolean {
        return tokenStorage.hasTokens()
    }
}

