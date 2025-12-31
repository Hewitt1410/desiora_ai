import SwiftUI
import GoogleSignIn

@main
struct DesioraAIApp: App {
    @StateObject private var authViewModel = AuthViewModel()
    
    init() {
        // Configure Google Sign-In
        // Replace with your actual Google Client ID
        if let path = Bundle.main.path(forResource: "GoogleService-Info", ofType: "plist"),
           let plist = NSDictionary(contentsOfFile: path),
           let clientId = plist["CLIENT_ID"] as? String {
            GIDSignIn.sharedInstance.configuration = GIDConfiguration(clientID: clientId)
        }
    }
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(authViewModel)
        }
    }
}
