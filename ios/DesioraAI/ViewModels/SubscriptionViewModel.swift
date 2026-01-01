import Foundation
import SwiftUI

@MainActor
class SubscriptionViewModel: ObservableObject {
    @Published var subscription: SubscriptionStatusResponse?
    @Published var isLoading = false
    @Published var errorMessage: String?
    
    private let subscriptionService = SubscriptionService.shared
    
    func loadSubscription() async {
        isLoading = true
        errorMessage = nil
        
        do {
            let subscription = try await subscriptionService.getStatus()
            self.subscription = subscription
        } catch {
            self.errorMessage = error.localizedDescription
        }
        
        isLoading = false
    }
    
    func cancelSubscription(reason: String? = nil) async {
        isLoading = true
        errorMessage = nil
        
        do {
            _ = try await subscriptionService.cancel(reason: reason)
            await loadSubscription() // Reload subscription
        } catch {
            self.errorMessage = error.localizedDescription
        }
        
        isLoading = false
    }
}




