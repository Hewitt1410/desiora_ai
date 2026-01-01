import Foundation
import SwiftUI

@MainActor
class DesignJobViewModel: ObservableObject {
    @Published var jobs: [DesignJobResponse] = []
    @Published var currentJob: DesignJobResponse?
    @Published var isLoading = false
    @Published var errorMessage: String?
    
    private let designJobService = DesignJobService.shared
    private let imageService = ImageService.shared
    
    func createJob(
        image: UIImage,
        style: String,
        roomType: String,
        prompt: String
    ) async {
        isLoading = true
        errorMessage = nil
        
        do {
            // Upload image first
            let filename = "\(UUID().uuidString).jpg"
            let imageUrl = try await imageService.uploadImage(image: image, filename: filename)
            
            // Create job
            let job = try await designJobService.createJob(
                jobType: "room_design",
                prompt: prompt.isEmpty ? "Redesign this \(roomType) in \(style) style" : prompt,
                imageUrl: imageUrl,
                style: style,
                roomType: roomType
            )
            
            self.currentJob = job
        } catch {
            self.errorMessage = error.localizedDescription
        }
        
        isLoading = false
    }
    
    func loadJobs() async {
        isLoading = true
        errorMessage = nil
        
        do {
            let response = try await designJobService.listJobs()
            self.jobs = response.jobs
        } catch {
            self.errorMessage = error.localizedDescription
        }
        
        isLoading = false
    }
    
    func getJob(id: Int) async {
        isLoading = true
        errorMessage = nil
        
        do {
            let job = try await designJobService.getJob(id: id)
            self.currentJob = job
        } catch {
            self.errorMessage = error.localizedDescription
        }
        
        isLoading = false
    }
    
    func pollJob(id: Int) async {
        do {
            let job = try await designJobService.getJob(id: id)
            self.currentJob = job
        } catch {
            // Silently fail for polling
        }
    }
}



