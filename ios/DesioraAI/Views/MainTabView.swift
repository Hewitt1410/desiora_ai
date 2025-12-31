import SwiftUI

struct MainTabView: View {
    @StateObject private var designJobViewModel = DesignJobViewModel()
    @StateObject private var subscriptionViewModel = SubscriptionViewModel()
    @EnvironmentObject var authViewModel: AuthViewModel
    
    var body: some View {
        TabView {
            DashboardView()
                .environmentObject(designJobViewModel)
                .tabItem {
                    Label("Dashboard", systemImage: "house.fill")
                }
            
            CreateDesignView()
                .environmentObject(designJobViewModel)
                .tabItem {
                    Label("Create", systemImage: "plus.circle.fill")
                }
            
            SubscriptionView()
                .environmentObject(subscriptionViewModel)
                .tabItem {
                    Label("Subscription", systemImage: "creditcard.fill")
                }
            
            ProfileView()
                .environmentObject(authViewModel)
                .tabItem {
                    Label("Profile", systemImage: "person.fill")
                }
        }
        .onAppear {
            Task {
                await designJobViewModel.loadJobs()
                await subscriptionViewModel.loadSubscription()
            }
        }
    }
}

