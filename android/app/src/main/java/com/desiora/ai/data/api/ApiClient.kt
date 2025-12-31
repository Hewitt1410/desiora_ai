package com.desiora.ai.data.api

import com.desiora.ai.BuildConfig
import com.desiora.ai.data.storage.TokenStorage
import okhttp3.Interceptor
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.util.concurrent.TimeUnit

object ApiClient {
    private var apiService: ApiService? = null
    
    fun getApiService(tokenStorage: TokenStorage): ApiService {
        if (apiService == null) {
            val loggingInterceptor = HttpLoggingInterceptor().apply {
                level = if (BuildConfig.DEBUG) {
                    HttpLoggingInterceptor.Level.BODY
                } else {
                    HttpLoggingInterceptor.Level.NONE
                }
            }
            
            val authInterceptor = Interceptor { chain ->
                val originalRequest = chain.request()
                val token = tokenStorage.getAccessToken()
                
                val newRequest = if (token != null) {
                    originalRequest.newBuilder()
                        .header("Authorization", "Bearer $token")
                        .header("Content-Type", "application/json")
                        .build()
                } else {
                    originalRequest.newBuilder()
                        .header("Content-Type", "application/json")
                        .build()
                }
                
                val response = chain.proceed(newRequest)
                
                // Handle 401 - refresh token
                if (response.code == 401 && token != null) {
                    val refreshToken = tokenStorage.getRefreshToken()
                    if (refreshToken != null) {
                        try {
                            // Attempt to refresh token
                            // This would need to be done synchronously or with a lock
                            // For now, we'll just return the 401 response
                        } catch (e: Exception) {
                            // Token refresh failed
                            tokenStorage.clearTokens()
                        }
                    }
                }
                
                response
            }
            
            val okHttpClient = OkHttpClient.Builder()
                .addInterceptor(loggingInterceptor)
                .addInterceptor(authInterceptor)
                .connectTimeout(30, TimeUnit.SECONDS)
                .readTimeout(30, TimeUnit.SECONDS)
                .writeTimeout(30, TimeUnit.SECONDS)
                .build()
            
            val retrofit = Retrofit.Builder()
                .baseUrl("${BuildConfig.API_BASE_URL}/api/")
                .client(okHttpClient)
                .addConverterFactory(GsonConverterFactory.create())
                .build()
            
            apiService = retrofit.create(ApiService::class.java)
        }
        
        return apiService!!
    }
    
    fun reset() {
        apiService = null
    }
}

