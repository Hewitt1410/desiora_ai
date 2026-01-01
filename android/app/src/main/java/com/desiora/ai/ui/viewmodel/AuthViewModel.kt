package com.desiora.ai.ui.viewmodel

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.desiora.ai.data.model.UserResponse
import com.desiora.ai.data.repository.AuthRepository
import com.desiora.ai.data.storage.TokenStorage
import kotlinx.coroutines.launch

class AuthViewModel(private val tokenStorage: TokenStorage) : ViewModel() {
    
    private val authRepository = AuthRepository(tokenStorage)
    
    private val _user = MutableLiveData<UserResponse?>()
    val user: LiveData<UserResponse?> = _user
    
    private val _isLoading = MutableLiveData<Boolean>()
    val isLoading: LiveData<Boolean> = _isLoading
    
    private val _error = MutableLiveData<String?>()
    val error: LiveData<String?> = _error
    
    fun login(email: String, password: String) {
        viewModelScope.launch {
            _isLoading.value = true
            _error.value = null
            
            authRepository.login(email, password)
                .onSuccess { user ->
                    _user.value = user
                    _isLoading.value = false
                }
                .onFailure { exception ->
                    _error.value = exception.message
                    _isLoading.value = false
                }
        }
    }
    
    fun register(email: String, password: String, username: String?) {
        viewModelScope.launch {
            _isLoading.value = true
            _error.value = null
            
            authRepository.register(email, password, username)
                .onSuccess { user ->
                    _user.value = user
                    _isLoading.value = false
                }
                .onFailure { exception ->
                    _error.value = exception.message
                    _isLoading.value = false
                }
        }
    }
    
    fun googleOAuth(code: String, redirectUri: String?) {
        viewModelScope.launch {
            _isLoading.value = true
            _error.value = null
            
            authRepository.googleOAuth(code, redirectUri)
                .onSuccess { user ->
                    _user.value = user
                    _isLoading.value = false
                }
                .onFailure { exception ->
                    _error.value = exception.message
                    _isLoading.value = false
                }
        }
    }
    
    fun getCurrentUser() {
        viewModelScope.launch {
            _isLoading.value = true
            authRepository.getCurrentUser()
                .onSuccess { user ->
                    _user.value = user
                    _isLoading.value = false
                }
                .onFailure {
                    _user.value = null
                    _isLoading.value = false
                }
        }
    }
    
    fun logout() {
        authRepository.logout()
        _user.value = null
    }
    
    fun isLoggedIn(): Boolean {
        return authRepository.isLoggedIn()
    }
    
    fun clearError() {
        _error.value = null
    }
}


