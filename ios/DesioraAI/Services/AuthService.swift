import Foundation
import AuthenticationServices
import GoogleSignIn

class AuthService {
    static let shared = AuthService()
    private let apiClient = ApiClient.shared
    private let tokenStorage = TokenStorage.shared
    
    private init() {}
    
    // MARK: - Email/Password Auth
    func login(email: String, password: String) async throws -> UserResponse {
        let request = LoginRequest(email: email, password: password)
        let response: TokenResponse = try await apiClient.request(
            endpoint: "/auth/login",
            method: .POST,
            body: request,
            requiresAuth: false
        )
        
        try tokenStorage.saveTokens(
            accessToken: response.access_token,
            refreshToken: response.refresh_token
        )
        
        return try await getCurrentUser()
    }
    
    func register(email: String, password: String, username: String?) async throws -> UserResponse {
        let request = RegisterRequest(email: email, password: password, username: username, full_name: nil)
        let response: TokenResponse = try await apiClient.request(
            endpoint: "/auth/register",
            method: .POST,
            body: request,
            requiresAuth: false
        )
        
        try tokenStorage.saveTokens(
            accessToken: response.access_token,
            refreshToken: response.refresh_token
        )
        
        return try await getCurrentUser()
    }
    
    // MARK: - Apple Sign In
    func signInWithApple(authorizationCode: String) async throws -> UserResponse {
        let request = OAuthRequest(code: authorizationCode, provider: "apple", redirect_uri: nil)
        let response: TokenResponse = try await apiClient.request(
            endpoint: "/auth/oauth/apple",
            method: .POST,
            body: request,
            requiresAuth: false
        )
        
        try tokenStorage.saveTokens(
            accessToken: response.access_token,
            refreshToken: response.refresh_token
        )
        
        return try await getCurrentUser()
    }
    
    // MARK: - Google Sign In
    func signInWithGoogle(idToken: String) async throws -> UserResponse {
        let request = OAuthRequest(code: idToken, provider: "google", redirect_uri: nil)
        let response: TokenResponse = try await apiClient.request(
            endpoint: "/auth/oauth/google",
            method: .POST,
            body: request,
            requiresAuth: false
        )
        
        try tokenStorage.saveTokens(
            accessToken: response.access_token,
            refreshToken: response.refresh_token
        )
        
        return try await getCurrentUser()
    }
    
    // MARK: - Get Current User
    func getCurrentUser() async throws -> UserResponse {
        return try await apiClient.request(
            endpoint: "/auth/me",
            method: .GET,
            requiresAuth: true
        )
    }
    
    // MARK: - Logout
    func logout() throws {
        try tokenStorage.clearTokens()
    }
}



