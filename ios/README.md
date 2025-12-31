# Desiora AI - iOS App

iOS application built with SwiftUI for the Desiora AI room design platform.

## Features

- ✅ Apple Sign-In
- ✅ Google Sign-In
- ✅ Photo capture & upload
- ✅ AI design job submission
- ✅ Real-time job status polling
- ✅ View design results
- ✅ Subscription management
- ✅ MVVM architecture
- ✅ Async/await for API calls
- ✅ Secure keychain storage

## Requirements

- iOS 15.0+
- Xcode 14.0+
- Swift 5.7+

## Setup

### 1. Configure Google Sign-In

1. Add your Google Client ID to `Info.plist`:
   - Update `CFBundleURLSchemes` with your Google Client ID

2. Configure Google Sign-In in `DesioraAIApp.swift`:
   ```swift
   GIDSignIn.sharedInstance.configuration = GIDConfiguration(clientID: "YOUR_CLIENT_ID")
   ```

### 2. Configure API URL

Update `ApiClient.swift` with your API base URL:
```swift
#if DEBUG
self.baseURL = "http://localhost:8000/api"
#else
self.baseURL = "https://api.desiora.ai/api"
#endif
```

### 3. Build and Run

1. Open `DesioraAI.xcodeproj` in Xcode
2. Select your target device or simulator
3. Build and run (⌘R)

## Project Structure

```
DesioraAI/
├── DesioraAIApp.swift          # App entry point
├── ContentView.swift            # Root view
├── Models/
│   └── ApiModels.swift          # API data models
├── Services/
│   ├── ApiClient.swift         # HTTP client
│   ├── AuthService.swift       # Authentication service
│   ├── DesignJobService.swift  # Design job service
│   ├── ImageService.swift      # Image upload service
│   ├── SubscriptionService.swift # Subscription service
│   ├── KeychainService.swift   # Keychain wrapper
│   └── TokenStorage.swift      # Token storage
├── ViewModels/
│   ├── AuthViewModel.swift     # Auth view model
│   ├── DesignJobViewModel.swift # Design job view model
│   └── SubscriptionViewModel.swift # Subscription view model
└── Views/
    ├── LoginView.swift         # Login screen
    ├── MainTabView.swift       # Main tab navigation
    ├── DashboardView.swift    # Job list
    ├── CreateDesignView.swift  # Create design job
    ├── DesignJobDetailView.swift # Job details
    ├── SubscriptionView.swift  # Subscription management
    └── ProfileView.swift      # User profile
```

## Architecture

### MVVM Pattern
- **Models**: Data structures for API responses
- **Views**: SwiftUI views for UI
- **ViewModels**: Business logic and state management
- **Services**: API and data layer

### Key Features

#### Secure Storage
- Uses iOS Keychain for token storage
- Encrypted storage via `KeychainService`

#### Async/Await
- All API calls use async/await
- ViewModels are marked with `@MainActor` for UI updates

#### Authentication
- Apple Sign-In with `AuthenticationServices`
- Google Sign-In with `GoogleSignIn` SDK
- Email/password authentication

#### Image Handling
- Camera capture
- Photo library selection
- S3 presigned URL upload

## Dependencies

- **GoogleSignIn**: Google Sign-In SDK
- **AuthenticationServices**: Apple Sign-In (built-in)

## License

MIT

