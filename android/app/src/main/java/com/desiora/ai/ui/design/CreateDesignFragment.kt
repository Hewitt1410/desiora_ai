package com.desiora.ai.ui.design

import android.app.Activity
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.provider.MediaStore
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import com.desiora.ai.databinding.FragmentCreateDesignBinding
import com.desiora.ai.data.storage.TokenStorage
import com.desiora.ai.ui.main.MainActivity
import com.desiora.ai.ui.viewmodel.DesignJobViewModel
import com.github.dhaval2404.imagepicker.ImagePicker
import java.io.File

class CreateDesignFragment : Fragment() {
    
    private var _binding: FragmentCreateDesignBinding? = null
    private val binding get() = _binding!!
    
    private lateinit var viewModel: DesignJobViewModel
    private lateinit var imageRepository: com.desiora.ai.data.repository.ImageRepository
    private var selectedImageUri: Uri? = null
    private var uploadedImageUrl: String? = null
    
    private val imagePickerLauncher = registerForActivityResult(
        ActivityResultContracts.StartActivityForResult()
    ) { result ->
        if (result.resultCode == Activity.RESULT_OK) {
            val uri = result.data?.data
            uri?.let {
                selectedImageUri = it
                binding.ivSelectedImage.setImageURI(it)
                binding.ivSelectedImage.visibility = View.VISIBLE
                binding.btnUploadImage.text = "Change Image"
            }
        }
    }
    
    private val cameraLauncher = registerForActivityResult(
        ActivityResultContracts.StartActivityForResult()
    ) { result ->
        if (result.resultCode == Activity.RESULT_OK) {
            val uri = result.data?.data
            uri?.let {
                selectedImageUri = it
                binding.ivSelectedImage.setImageURI(it)
                binding.ivSelectedImage.visibility = View.VISIBLE
                binding.btnUploadImage.text = "Change Image"
            }
        }
    }
    
    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentCreateDesignBinding.inflate(inflater, container, false)
        return binding.root
    }
    
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        
        val tokenStorage = TokenStorage(requireContext())
        viewModel = ViewModelProvider(this, DesignJobViewModelFactory(tokenStorage))[DesignJobViewModel::class.java]
        imageRepository = com.desiora.ai.data.repository.ImageRepository(tokenStorage)
        
        setupClickListeners()
        setupObservers()
    }
    
    private fun setupClickListeners() {
        binding.btnUploadImage.setOnClickListener {
            showImagePickerOptions()
        }
        
        binding.btnCaptureImage.setOnClickListener {
            ImagePicker.with(this)
                .cameraOnly()
                .start(cameraLauncher)
        }
        
        binding.btnSubmit.setOnClickListener {
            if (selectedImageUri == null) {
                Toast.makeText(requireContext(), "Please select an image", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }
            
            val style = binding.spStyle.selectedItem.toString().lowercase()
            val roomType = binding.spRoomType.selectedItem.toString().lowercase()
            val prompt = binding.etPrompt.text.toString().takeIf { it.isNotBlank() }
                ?: "Redesign this ${roomType.replace("_", " ")} in $style style"
            
            uploadImageAndCreateJob(style, roomType, prompt)
        }
    }
    
    private fun showImagePickerOptions() {
        ImagePicker.with(this)
            .galleryOnly()
            .start(imagePickerLauncher)
    }
    
    private fun uploadImageAndCreateJob(style: String, roomType: String, prompt: String) {
        selectedImageUri?.let { uri ->
            binding.progressBar.visibility = View.VISIBLE
            binding.btnSubmit.isEnabled = false
            
            // Convert URI to File
            val imageFile = File(uri.path ?: "")
            
            // Upload image
            viewModel.createJob(
                jobType = "room_design",
                prompt = prompt,
                imageUrl = uploadedImageUrl ?: "",
                style = style,
                roomType = roomType
            )
        }
    }
    
    private fun setupObservers() {
        viewModel.currentJob.observe(viewLifecycleOwner) { job ->
            job?.let {
                binding.progressBar.visibility = View.GONE
                binding.btnSubmit.isEnabled = true
                (activity as? MainActivity)?.navigateToJobDetail(it.id)
            }
        }
        
        viewModel.isLoading.observe(viewLifecycleOwner) { isLoading ->
            binding.progressBar.visibility = if (isLoading) View.VISIBLE else View.GONE
            binding.btnSubmit.isEnabled = !isLoading
        }
        
        viewModel.error.observe(viewLifecycleOwner) { error ->
            error?.let {
                Toast.makeText(requireContext(), it, Toast.LENGTH_SHORT).show()
                binding.progressBar.visibility = View.GONE
                binding.btnSubmit.isEnabled = true
                viewModel.clearError()
            }
        }
    }
    
    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}

