import Foundation

class SubscriptionService {
    static let shared = SubscriptionService()
    private let apiClient = ApiClient.shared
    
    private init() {}
    
    func getStatus() async throws -> SubscriptionStatusResponse {
        return try await apiClient.request(
            endpoint: "/subscriptions/status",
            method: .GET,
            requiresAuth: true
        )
    }
    
    func cancel(reason: String? = nil) async throws -> CancelSubscriptionResponse {
        let request = CancelSubscriptionRequest(reason: reason)
        return try await apiClient.request(
            endpoint: "/subscriptions/cancel",
            method: .POST,
            body: request,
            requiresAuth: true
        )
    }
}




