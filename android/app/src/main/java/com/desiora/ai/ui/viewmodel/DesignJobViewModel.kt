package com.desiora.ai.ui.viewmodel

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.desiora.ai.data.model.DesignJobResponse
import com.desiora.ai.data.model.DesignJobListResponse
import com.desiora.ai.data.repository.DesignJobRepository
import com.desiora.ai.data.storage.TokenStorage
import kotlinx.coroutines.launch

class DesignJobViewModel(private val tokenStorage: TokenStorage) : ViewModel() {
    
    private val designJobRepository = DesignJobRepository(tokenStorage)
    
    private val _jobs = MutableLiveData<List<DesignJobResponse>>()
    val jobs: LiveData<List<DesignJobResponse>> = _jobs
    
    private val _currentJob = MutableLiveData<DesignJobResponse?>()
    val currentJob: LiveData<DesignJobResponse?> = _currentJob
    
    private val _isLoading = MutableLiveData<Boolean>()
    val isLoading: LiveData<Boolean> = _isLoading
    
    private val _error = MutableLiveData<String?>()
    val error: LiveData<String?> = _error
    
    fun createJob(
        jobType: String,
        prompt: String,
        imageUrl: String,
        style: String,
        roomType: String?
    ) {
        viewModelScope.launch {
            _isLoading.value = true
            _error.value = null
            
            designJobRepository.createJob(jobType, prompt, imageUrl, style, roomType)
                .onSuccess { job ->
                    _currentJob.value = job
                    _isLoading.value = false
                }
                .onFailure { exception ->
                    _error.value = exception.message
                    _isLoading.value = false
                }
        }
    }
    
    fun getJob(jobId: Int) {
        viewModelScope.launch {
            _isLoading.value = true
            _error.value = null
            
            designJobRepository.getJob(jobId)
                .onSuccess { job ->
                    _currentJob.value = job
                    _isLoading.value = false
                }
                .onFailure { exception ->
                    _error.value = exception.message
                    _isLoading.value = false
                }
        }
    }
    
    fun pollJob(jobId: Int) {
        viewModelScope.launch {
            designJobRepository.getJob(jobId)
                .onSuccess { job ->
                    _currentJob.value = job
                }
        }
    }
    
    fun loadJobs(page: Int = 1, pageSize: Int = 20, status: String? = null) {
        viewModelScope.launch {
            _isLoading.value = true
            _error.value = null
            
            designJobRepository.listJobs(page, pageSize, status)
                .onSuccess { response ->
                    _jobs.value = response.jobs
                    _isLoading.value = false
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




