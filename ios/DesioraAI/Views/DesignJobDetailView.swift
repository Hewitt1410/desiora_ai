import SwiftUI

struct DesignJobDetailView: View {
    let jobId: Int
    @EnvironmentObject var designJobViewModel: DesignJobViewModel
    @State private var pollingTimer: Timer?
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                if let job = designJobViewModel.currentJob {
                    VStack(alignment: .leading, spacing: 12) {
                        Text(job.job_type.replacingOccurrences(of: "_", with: " ").capitalized)
                            .font(.title2)
                            .fontWeight(.bold)
                        
                        Text(job.prompt)
                            .font(.body)
                            .foregroundColor(.secondary)
                        
                        StatusBadge(status: job.status)
                        
                        if let errorMessage = job.error_message {
                            Text("Error: \(errorMessage)")
                                .foregroundColor(.red)
                                .padding()
                                .background(Color.red.opacity(0.1))
                                .cornerRadius(8)
                        }
                    }
                    .padding()
                    
                    if let resultUrls = job.result_urls, !resultUrls.isEmpty {
                        VStack(alignment: .leading, spacing: 12) {
                            Text("Results")
                                .font(.headline)
                                .padding(.horizontal)
                            
                            ScrollView(.horizontal, showsIndicators: false) {
                                HStack(spacing: 12) {
                                    ForEach(resultUrls, id: \.self) { urlString in
                                        AsyncImage(url: URL(string: urlString)) { image in
                                            image
                                                .resizable()
                                                .scaledToFit()
                                        } placeholder: {
                                            ProgressView()
                                        }
                                        .frame(width: 300, height: 300)
                                        .cornerRadius(8)
                                    }
                                }
                                .padding()
                            }
                        }
                    } else {
                        VStack {
                            if job.status == "processing" || job.status == "pending" {
                                ProgressView()
                                Text("Processing your design...")
                                    .foregroundColor(.secondary)
                                    .padding()
                            } else {
                                Text("No results yet")
                                    .foregroundColor(.secondary)
                                    .padding()
                            }
                        }
                        .frame(maxWidth: .infinity)
                        .padding()
                    }
                } else if designJobViewModel.isLoading {
                    ProgressView()
                        .frame(maxWidth: .infinity)
                        .padding()
                }
            }
        }
        .navigationTitle("Design Job")
        .navigationBarTitleDisplayMode(.inline)
        .onAppear {
            Task {
                await designJobViewModel.getJob(id: jobId)
            }
            startPolling()
        }
        .onDisappear {
            stopPolling()
        }
    }
    
    private func startPolling() {
        guard let job = designJobViewModel.currentJob,
              (job.status == "pending" || job.status == "processing") else {
            return
        }
        
        pollingTimer = Timer.scheduledTimer(withTimeInterval: 3.0, repeats: true) { _ in
            Task {
                await designJobViewModel.pollJob(id: jobId)
            }
        }
    }
    
    private func stopPolling() {
        pollingTimer?.invalidate()
        pollingTimer = nil
    }
}



