package com.desiora.ai.utils

import android.content.Context
import android.content.SharedPreferences
import androidx.appcompat.app.AppCompatDelegate

object ThemeManager {
    private const val PREFS_NAME = "theme_prefs"
    private const val KEY_THEME_MODE = "theme_mode"
    
    enum class ThemeMode(val value: Int) {
        LIGHT(AppCompatDelegate.MODE_NIGHT_NO),
        DARK(AppCompatDelegate.MODE_NIGHT_YES),
        SYSTEM(AppCompatDelegate.MODE_NIGHT_FOLLOW_SYSTEM);
        
        companion object {
            fun fromInt(value: Int): ThemeMode {
                return when (value) {
                    AppCompatDelegate.MODE_NIGHT_NO -> LIGHT
                    AppCompatDelegate.MODE_NIGHT_YES -> DARK
                    AppCompatDelegate.MODE_NIGHT_FOLLOW_SYSTEM -> SYSTEM
                    else -> SYSTEM
                }
            }
        }
    }
    
    fun getThemeMode(context: Context): ThemeMode {
        val prefs: SharedPreferences = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
        val modeValue = prefs.getInt(KEY_THEME_MODE, AppCompatDelegate.MODE_NIGHT_FOLLOW_SYSTEM)
        return ThemeMode.fromInt(modeValue)
    }
    
    fun setThemeMode(context: Context, mode: ThemeMode) {
        val prefs: SharedPreferences = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
        prefs.edit().putInt(KEY_THEME_MODE, mode.value).apply()
        AppCompatDelegate.setDefaultNightMode(mode.value)
    }
    
    fun applyTheme(context: Context) {
        val mode = getThemeMode(context)
        AppCompatDelegate.setDefaultNightMode(mode.value)
    }
}


