package com.desiora.ai.ui.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import com.desiora.ai.data.storage.TokenStorage

class DesignJobViewModelFactory(private val tokenStorage: TokenStorage) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(DesignJobViewModel::class.java)) {
            @Suppress("UNCHECKED_CAST")
            return DesignJobViewModel(tokenStorage) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}

