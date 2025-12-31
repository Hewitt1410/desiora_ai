import SwiftUI

struct SubscriptionView: View {
    @EnvironmentObject var subscriptionViewModel: SubscriptionViewModel
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 20) {
                    if let subscription = subscriptionViewModel.subscription {
                        // Current Plan
                        VStack(alignment: .leading, spacing: 12) {
                            Text("Current Plan")
                                .font(.headline)
                            
                            Text(subscription.subscription.plan.capitalized)
                                .font(.title2)
                                .fontWeight(.bold)
                            
                            Text("Status: \(subscription.subscription.status.capitalized)")
                                .foregroundColor(.secondary)
                        }
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .padding()
                        .background(Color.blue.opacity(0.1))
                        .cornerRadius(12)
                        
                        // Usage Quota
                        VStack(alignment: .leading, spacing: 12) {
                            Text("Usage Quota")
                                .font(.headline)
                            
                            HStack {
                                Text("\(subscription.quota_info.used) / \(subscription.quota_info.quota)")
                                Spacer()
                                Text("\(subscription.quota_info.remaining) remaining")
                                    .foregroundColor(.secondary)
                            }
                            
                            ProgressView(value: subscription.quota_info.percentage_used / 100.0)
                            
                            if !subscription.can_use_ai_job {
                                Text("You've reached your quota limit. Please upgrade your plan.")
                                    .foregroundColor(.orange)
                                    .font(.caption)
                            }
                        }
                        .padding()
                        .background(Color.gray.opacity(0.1))
                        .cornerRadius(12)
                        
                        // Cancel Subscription
                        if subscription.subscription.status == "active" {
                            Button(action: {
                                Task {
                                    await subscriptionViewModel.cancelSubscription()
                                }
                            }) {
                                Text("Cancel Subscription")
                                    .foregroundColor(.red)
                                    .frame(maxWidth: .infinity)
                            }
                            .buttonStyle(.bordered)
                        }
                        
                        // Available Plans
                        VStack(alignment: .leading, spacing: 12) {
                            Text("Available Plans")
                                .font(.headline)
                            
                            PlanCard(plan: "Weekly", price: "$9.99", quota: "100 jobs/week")
                            PlanCard(plan: "Monthly", price: "$29.99", quota: "500 jobs/month")
                            PlanCard(plan: "Yearly", price: "$299.99", quota: "6000 jobs/year")
                        }
                        .padding()
                    } else if subscriptionViewModel.isLoading {
                        ProgressView()
                            .frame(maxWidth: .infinity)
                            .padding()
                    }
                }
                .padding()
            }
            .navigationTitle("Subscription")
            .refreshable {
                await subscriptionViewModel.loadSubscription()
            }
        }
    }
}

struct PlanCard: View {
    let plan: String
    let price: String
    let quota: String
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(plan)
                .font(.headline)
            Text(price)
                .font(.title3)
                .fontWeight(.bold)
            Text(quota)
                .font(.caption)
                .foregroundColor(.secondary)
            
            Button("Upgrade") {
                // Handle upgrade
            }
            .buttonStyle(.borderedProminent)
            .frame(maxWidth: .infinity, alignment: .trailing)
        }
        .padding()
        .background(Color.gray.opacity(0.1))
        .cornerRadius(12)
    }
}

