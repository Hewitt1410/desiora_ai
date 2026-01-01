package com.desiora.ai.ui.dashboard

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.desiora.ai.R
import com.desiora.ai.data.model.DesignJobResponse
import java.text.SimpleDateFormat
import java.util.*

class DesignJobAdapter(
    private val onItemClick: (DesignJobResponse) -> Unit
) : ListAdapter<DesignJobResponse, DesignJobAdapter.ViewHolder>(DesignJobDiffCallback()) {
    
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_design_job, parent, false)
        return ViewHolder(view, onItemClick)
    }
    
    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        holder.bind(getItem(position))
    }
    
    class ViewHolder(
        itemView: View,
        private val onItemClick: (DesignJobResponse) -> Unit
    ) : RecyclerView.ViewHolder(itemView) {
        
        private val jobType: TextView = itemView.findViewById(R.id.tvJobType)
        private val prompt: TextView = itemView.findViewById(R.id.tvPrompt)
        private val status: TextView = itemView.findViewById(R.id.tvStatus)
        private val createdAt: TextView = itemView.findViewById(R.id.tvCreatedAt)
        
        fun bind(job: DesignJobResponse) {
            jobType.text = job.jobType.replace("_", " ").capitalize()
            prompt.text = job.prompt
            status.text = job.status.capitalize()
            
            val dateFormat = SimpleDateFormat("MMM d, yyyy", Locale.getDefault())
            createdAt.text = dateFormat.format(Date(job.createdAt))
            
            itemView.setOnClickListener {
                onItemClick(job)
            }
        }
    }
    
    class DesignJobDiffCallback : DiffUtil.ItemCallback<DesignJobResponse>() {
        override fun areItemsTheSame(oldItem: DesignJobResponse, newItem: DesignJobResponse): Boolean {
            return oldItem.id == newItem.id
        }
        
        override fun areContentsTheSame(oldItem: DesignJobResponse, newItem: DesignJobResponse): Boolean {
            return oldItem == newItem
        }
    }
}


