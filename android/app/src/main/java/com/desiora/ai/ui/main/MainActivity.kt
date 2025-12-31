package com.desiora.ai.ui.main

import android.content.Intent
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.fragment.app.Fragment
import com.desiora.ai.R
import com.desiora.ai.databinding.ActivityMainBinding
import com.desiora.ai.ui.design.CreateDesignFragment
import com.desiora.ai.ui.design.DesignJobDetailFragment
import com.desiora.ai.ui.dashboard.DashboardFragment
import com.desiora.ai.ui.subscription.SubscriptionFragment

class MainActivity : AppCompatActivity() {
    
    private lateinit var binding: ActivityMainBinding
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        
        setupBottomNavigation()
        
        if (savedInstanceState == null) {
            supportFragmentManager.beginTransaction()
                .replace(R.id.fragment_container, DashboardFragment())
                .commit()
        }
    }
    
    private fun setupBottomNavigation() {
        binding.bottomNavigation.setOnItemSelectedListener { item ->
            when (item.itemId) {
                R.id.nav_dashboard -> {
                    replaceFragment(DashboardFragment())
                    true
                }
                R.id.nav_create -> {
                    replaceFragment(CreateDesignFragment())
                    true
                }
                R.id.nav_subscription -> {
                    replaceFragment(SubscriptionFragment())
                    true
                }
                else -> false
            }
        }
    }
    
    private fun replaceFragment(fragment: Fragment) {
        supportFragmentManager.beginTransaction()
            .replace(R.id.fragment_container, fragment)
            .commit()
    }
    
    fun navigateToJobDetail(jobId: Int) {
        val fragment = DesignJobDetailFragment.newInstance(jobId)
        supportFragmentManager.beginTransaction()
            .replace(R.id.fragment_container, fragment)
            .addToBackStack(null)
            .commit()
    }
}

