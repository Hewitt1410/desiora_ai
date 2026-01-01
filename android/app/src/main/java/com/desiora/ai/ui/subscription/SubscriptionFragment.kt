package com.desiora.ai.ui.subscription

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import com.desiora.ai.databinding.FragmentSubscriptionBinding
import com.desiora.ai.data.storage.TokenStorage
import com.desiora.ai.ui.viewmodel.SubscriptionViewModel

class SubscriptionFragment : Fragment() {
    
    private var _binding: FragmentSubscriptionBinding? = null
    private val binding get() = _binding!!
    
    private lateinit var viewModel: SubscriptionViewModel
    
    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentSubscriptionBinding.inflate(inflater, container, false)
        return binding.root
    }
    
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        
        val tokenStorage = TokenStorage(requireContext())
        viewModel = ViewModelProvider(this, SubscriptionViewModelFactory(tokenStorage))[SubscriptionViewModel::class.java]
        
        setupObservers()
        viewModel.loadSubscription()
    }
    
    private fun setupObservers() {
        viewModel.subscription.observe(viewLifecycleOwner) { subscriptionStatus ->
            subscriptionStatus?.let {
                binding.tvCurrentPlan.text = it.subscription.plan.replace("_", " ").capitalize()
                binding.tvPlanStatus.text = "Status: ${it.subscription.status.capitalize()}"
                
                // Update quota info from subscriptionStatus
                val quotaInfo = it.quotaInfo
                val percentage = if (quotaInfo.quota > 0) {
                    (quotaInfo.used.toFloat() / quotaInfo.quota.toFloat() * 100).toInt()
                } else {
                    0
                }
                binding.progressQuota.progress = percentage
                binding.tvQuotaInfo.text = "${quotaInfo.used} / ${quotaInfo.quota} jobs used"
            }
        }
        
        viewModel.isLoading.observe(viewLifecycleOwner) { isLoading ->
            binding.progressBar.visibility = if (isLoading) View.VISIBLE else View.GONE
        }
        
        viewModel.error.observe(viewLifecycleOwner) { error ->
            error?.let {
                Toast.makeText(requireContext(), it, Toast.LENGTH_SHORT).show()
                viewModel.clearError()
            }
        }
    }
    
    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}

class SubscriptionViewModelFactory(private val tokenStorage: TokenStorage) : androidx.lifecycle.ViewModelProvider.Factory {
    override fun <T : androidx.lifecycle.ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(SubscriptionViewModel::class.java)) {
            @Suppress("UNCHECKED_CAST")
            return SubscriptionViewModel(tokenStorage) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}

