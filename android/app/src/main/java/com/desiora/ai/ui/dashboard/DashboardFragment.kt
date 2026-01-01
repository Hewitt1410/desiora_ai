package com.desiora.ai.ui.dashboard

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import androidx.recyclerview.widget.LinearLayoutManager
import com.desiora.ai.databinding.FragmentDashboardBinding
import com.desiora.ai.data.storage.TokenStorage
import com.desiora.ai.ui.main.MainActivity
import com.desiora.ai.ui.viewmodel.DesignJobViewModel

class DashboardFragment : Fragment() {
    
    private var _binding: FragmentDashboardBinding? = null
    private val binding get() = _binding!!
    
    private lateinit var viewModel: DesignJobViewModel
    private lateinit var adapter: DesignJobAdapter
    
    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentDashboardBinding.inflate(inflater, container, false)
        return binding.root
    }
    
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        
        val tokenStorage = TokenStorage(requireContext())
        viewModel = ViewModelProvider(this, DesignJobViewModelFactory(tokenStorage))[DesignJobViewModel::class.java]
        
        setupRecyclerView()
        setupObservers()
        
        viewModel.loadJobs()
    }
    
    private fun setupRecyclerView() {
        adapter = DesignJobAdapter { job ->
            (activity as? MainActivity)?.navigateToJobDetail(job.id)
        }
        
        binding.recyclerViewJobs.layoutManager = LinearLayoutManager(requireContext())
        binding.recyclerViewJobs.adapter = adapter
    }
    
    private fun setupObservers() {
        viewModel.jobs.observe(viewLifecycleOwner) { jobs ->
            adapter.submitList(jobs)
            binding.emptyState.visibility = if (jobs.isEmpty()) View.VISIBLE else View.GONE
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

class DesignJobViewModelFactory(private val tokenStorage: TokenStorage) : ViewModelProvider.Factory {
    override fun <T : androidx.lifecycle.ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(DesignJobViewModel::class.java)) {
            @Suppress("UNCHECKED_CAST")
            return DesignJobViewModel(tokenStorage) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}


