import Foundation

class DesignJobService {
    static let shared = DesignJobService()
    private let apiClient = ApiClient.shared
    
    private init() {}
    
    func createJob(
        jobType: String,
        prompt: String,
        imageUrl: String,
        style: String,
        roomType: String
    ) async throws -> DesignJobResponse {
        let parameters: [String: String] = [
            "image_url": imageUrl,
            "style": style,
            "room_type": roomType
        ]
        
        let request = DesignJobCreateRequest(
            job_type: jobType,
            prompt: prompt,
            parameters: parameters
        )
        
        return try await apiClient.request(
            endpoint: "/designs",
            method: .POST,
            body: request,
            requiresAuth: true
        )
    }
    
    func getJob(id: Int) async throws -> DesignJobResponse {
        return try await apiClient.request(
            endpoint: "/designs/\(id)",
            method: .GET,
            requiresAuth: true
        )
    }
    
    func listJobs(page: Int = 1, pageSize: Int = 20, status: String? = nil) async throws -> DesignJobListResponse {
        var endpoint = "/designs?page=\(page)&page_size=\(pageSize)"
        if let status = status {
            endpoint += "&status=\(status)"
        }
        
        return try await apiClient.request(
            endpoint: endpoint,
            method: .GET,
            requiresAuth: true
        )
    }
}


