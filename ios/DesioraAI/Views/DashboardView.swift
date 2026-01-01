import SwiftUI

struct DashboardView: View {
    @EnvironmentObject var designJobViewModel: DesignJobViewModel
    
    var body: some View {
        NavigationView {
            List {
                ForEach(designJobViewModel.jobs) { job in
                    NavigationLink(destination: DesignJobDetailView(jobId: job.id)
                        .environmentObject(designJobViewModel)) {
                        DesignJobRow(job: job)
                    }
                }
            }
            .navigationTitle("My Design Jobs")
            .refreshable {
                await designJobViewModel.loadJobs()
            }
            .overlay {
                if designJobViewModel.isLoading && designJobViewModel.jobs.isEmpty {
                    ProgressView()
                }
            }
        }
    }
}

struct DesignJobRow: View {
    let job: DesignJobResponse
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(job.job_type.replacingOccurrences(of: "_", with: " ").capitalized)
                .font(.headline)
            
            Text(job.prompt)
                .font(.subheadline)
                .foregroundColor(.secondary)
                .lineLimit(2)
            
            HStack {
                StatusBadge(status: job.status)
                Spacer()
                Text(formatDate(job.created_at))
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
        }
        .padding(.vertical, 4)
    }
    
    private func formatDate(_ dateString: String) -> String {
        let formatter = ISO8601DateFormatter()
        guard let date = formatter.date(from: dateString) else {
            return dateString
        }
        let displayFormatter = DateFormatter()
        displayFormatter.dateStyle = .medium
        return displayFormatter.string(from: date)
    }
}

struct StatusBadge: View {
    let status: String
    
    var body: some View {
        Text(status.capitalized)
            .font(.caption)
            .padding(.horizontal, 8)
            .padding(.vertical, 4)
            .background(statusColor)
            .foregroundColor(.white)
            .cornerRadius(8)
    }
    
    private var statusColor: Color {
        switch status.lowercased() {
        case "completed":
            return .green
        case "processing":
            return .blue
        case "failed":
            return .red
        default:
            return .gray
        }
    }
}



