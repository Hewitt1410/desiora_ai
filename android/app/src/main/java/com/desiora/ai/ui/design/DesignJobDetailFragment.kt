package com.desiora.ai.ui.design

import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import com.desiora.ai.databinding.FragmentDesignJobDetailBinding
import com.desiora.ai.data.storage.TokenStorage
import com.desiora.ai.ui.viewmodel.DesignJobViewModel
import com.bumptech.glide.Glide

class DesignJobDetailFragment : Fragment() {
    
    private var _binding: FragmentDesignJobDetailBinding? = null
    private val binding get() = _binding!!
    
    private lateinit var viewModel: DesignJobViewModel
    private var jobId: Int = -1
    private var isPolling = false
    private val handler = Handler(Looper.getMainLooper())
    
    companion object {
        private const val ARG_JOB_ID = "job_id"
        
        fun newInstance(jobId: Int): DesignJobDetailFragment {
            return DesignJobDetailFragment().apply {
                arguments = Bundle().apply {
                    putInt(ARG_JOB_ID, jobId)
                }
            }
        }
    }
    
    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentDesignJobDetailBinding.inflate(inflater, container, false)
        return binding.root
    }
    
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        
        jobId = arguments?.getInt(ARG_JOB_ID) ?: -1
        
        val tokenStorage = TokenStorage(requireContext())
        viewModel = ViewModelProvider(this, DesignJobViewModelFactory(tokenStorage))[DesignJobViewModel::class.java]
        
        setupObservers()
        viewModel.getJob(jobId)
    }
    
    private fun setupObservers() {
        viewModel.currentJob.observe(viewLifecycleOwner) { job ->
            job?.let {
                updateUI(it)
                
                // Start polling if job is still processing
                if ((it.status == "pending" || it.status == "processing") && !isPolling) {
                    startPolling()
                } else if (it.status == "completed" || it.status == "failed") {
                    stopPolling()
                }
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
    
    private fun updateUI(job: com.desiora.ai.data.model.DesignJobResponse) {
        binding.tvJobType.text = job.jobType.replace("_", " ").capitalize()
        binding.tvPrompt.text = job.prompt
        binding.tvStatus.text = job.status.capitalize()
        
        // Update status color
        val statusColor = when (job.status) {
            "completed" -> android.graphics.Color.GREEN
            "processing" -> android.graphics.Color.BLUE
            "failed" -> android.graphics.Color.RED
            else -> android.graphics.Color.GRAY
        }
        binding.tvStatus.setTextColor(statusColor)
        
        // Show results if available
        if (job.resultUrls != null && job.resultUrls.isNotEmpty()) {
            binding.recyclerViewResults.visibility = View.VISIBLE
            binding.tvNoResults.visibility = View.GONE
            
            // Load images using Glide
            // For simplicity, showing first result
            Glide.with(this)
                .load(job.resultUrls[0])
                .into(binding.ivResult)
        } else {
            binding.recyclerViewResults.visibility = View.GONE
            binding.tvNoResults.visibility = View.VISIBLE
        }
        
        // Show error if failed
        if (job.status == "failed" && job.errorMessage != null) {
            binding.tvError.visibility = View.VISIBLE
            binding.tvError.text = job.errorMessage
        } else {
            binding.tvError.visibility = View.GONE
        }
    }
    
    private fun startPolling() {
        isPolling = true
        val runnable = object : Runnable {
            override fun run() {
                if (isPolling) {
                    viewModel.pollJob(jobId)
                    handler.postDelayed(this, 3000) // Poll every 3 seconds
                }
            }
        }
        handler.post(runnable)
    }
    
    private fun stopPolling() {
        isPolling = false
    }
    
    override fun onDestroyView() {
        super.onDestroyView()
        stopPolling()
        _binding = null
    }
}




