package com.desiora.ai.ui.profile

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import com.desiora.ai.databinding.FragmentProfileBinding
import com.desiora.ai.ui.viewmodel.AuthViewModel
import com.desiora.ai.ui.auth.AuthViewModelFactory
import com.desiora.ai.utils.ThemeManager
import androidx.appcompat.app.AlertDialog
import android.content.Intent
import androidx.lifecycle.Observer

class ProfileFragment : Fragment() {
    
    private var _binding: FragmentProfileBinding? = null
    private val binding get() = _binding!!
    
    private lateinit var authViewModel: AuthViewModel
    
    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentProfileBinding.inflate(inflater, container, false)
        return binding.root
    }
    
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        
        val tokenStorage = com.desiora.ai.data.storage.TokenStorage(requireContext())
        authViewModel = ViewModelProvider(this, AuthViewModelFactory(tokenStorage))[AuthViewModel::class.java]
        
        setupObservers()
        setupClickListeners()
        updateThemeToggle()
    }
    
    private fun setupObservers() {
        authViewModel.user.observe(viewLifecycleOwner, Observer { user ->
            user?.let {
                binding.tvEmail.text = it.email
                binding.tvUsername.text = it.username ?: "N/A"
                binding.tvRole.text = "Role: ${it.role}"
            }
        })
    }
    
    private fun setupClickListeners() {
        binding.switchTheme.setOnCheckedChangeListener { _: android.widget.CompoundButton, isChecked: Boolean ->
            val mode = if (isChecked) ThemeManager.ThemeMode.DARK else ThemeManager.ThemeMode.LIGHT
            ThemeManager.setThemeMode(requireContext(), mode)
            requireActivity().recreate() // Recreate activity to apply theme
        }
        
        binding.btnSystemTheme.setOnClickListener {
            ThemeManager.setThemeMode(requireContext(), ThemeManager.ThemeMode.SYSTEM)
            requireActivity().recreate()
            updateThemeToggle()
        }
        
        binding.btnLogout.setOnClickListener {
            showLogoutDialog()
        }
    }
    
    private fun updateThemeToggle() {
        val currentMode = ThemeManager.getThemeMode(requireContext())
        val isDarkMode = (currentMode == ThemeManager.ThemeMode.DARK)
        binding.switchTheme.isChecked = isDarkMode
        val themeText = when (currentMode) {
            ThemeManager.ThemeMode.LIGHT -> "Light Mode"
            ThemeManager.ThemeMode.DARK -> "Dark Mode"
            ThemeManager.ThemeMode.SYSTEM -> "System Default"
        }
        binding.tvThemeMode.text = themeText
    }
    
    private fun showLogoutDialog() {
        AlertDialog.Builder(requireContext())
            .setTitle("Logout")
            .setMessage("Are you sure you want to logout?")
            .setPositiveButton("Logout") { _, _ ->
                authViewModel.logout()
                // Navigate to login activity
                val intent = Intent(requireContext(), com.desiora.ai.ui.auth.LoginActivity::class.java)
                intent.flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
                startActivity(intent)
                requireActivity().finish()
            }
            .setNegativeButton("Cancel", null)
            .show()
    }
    
    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}



