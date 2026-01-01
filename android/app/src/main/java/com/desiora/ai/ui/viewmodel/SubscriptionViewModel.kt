package com.desiora.ai.ui.viewmodel

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.desiora.ai.data.model.SubscriptionStatusResponse
import com.desiora.ai.data.repository.SubscriptionRepository
import com.desiora.ai.data.storage.TokenStorage
import kotlinx.coroutines.launch

class SubscriptionViewModel(private val tokenStorage: TokenStorage) : ViewModel() {
    
    private val subscriptionRepository = SubscriptionRepository(tokenStorage)
    
    private val _subscription = MutableLiveData<SubscriptionStatusResponse?>()
    val subscription: LiveData<SubscriptionStatusResponse?> = _subscription
    
    private val _isLoading = MutableLiveData<Boolean>()
    val isLoading: LiveData<Boolean> = _isLoading
    
    private val _error = MutableLiveData<String?>()
    val error: LiveData<String?> = _error
    
    fun loadSubscription() {
        viewModelScope.launch {
            _isLoading.value = true
            _error.value = null
            
            subscriptionRepository.getStatus()
                .onSuccess { subscription ->
                    _subscription.value = subscription
                    _isLoading.value = false
                }
                .onFailure { exception ->
                    _error.value = exception.message
                    _isLoading.value = false
                }
        }
    }
    
    fun cancelSubscription(reason: String? = null) {
        viewModelScope.launch {
            _isLoading.value = true
            _error.value = null
            
            subscriptionRepository.cancel(reason)
                .onSuccess {
                    loadSubscription() // Reload subscription status
                }
                .onFailure { exception ->
                    _error.value = exception.message
                    _isLoading.value = false
                }
        }
    }
    
    fun clearError() {
        _error.value = null
    }
}




