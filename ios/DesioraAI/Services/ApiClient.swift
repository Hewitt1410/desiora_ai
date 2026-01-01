import Foundation

class ApiClient {
    static let shared = ApiClient()
    
    private let baseURL: String
    private let session: URLSession
    private let tokenStorage = TokenStorage.shared
    
    private init() {
        #if DEBUG
        self.baseURL = "http://localhost:8000/api"
        #else
        self.baseURL = "https://api.desiora.ai/api"
        #endif
        
        let configuration = URLSessionConfiguration.default
        configuration.timeoutIntervalForRequest = 30
        configuration.timeoutIntervalForResource = 60
        self.session = URLSession(configuration: configuration)
    }
    
    func request<T: Codable>(
        endpoint: String,
        method: HTTPMethod = .GET,
        body: Codable? = nil,
        requiresAuth: Bool = true
    ) async throws -> T {
        guard let url = URL(string: "\(baseURL)\(endpoint)") else {
            throw ApiError.invalidURL
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = method.rawValue
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        if requiresAuth {
            if let token = tokenStorage.getAccessToken() {
                request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
            }
        }
        
        if let body = body {
            request.httpBody = try JSONEncoder().encode(body)
        }
        
        let (data, response) = try await session.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw ApiError.invalidResponse
        }
        
        if httpResponse.statusCode == 401 && requiresAuth {
            // Try to refresh token
            if let refreshToken = tokenStorage.getRefreshToken() {
                let refreshRequest = RefreshTokenRequest(refresh_token: refreshToken)
                let tokenResponse: TokenResponse = try await self.request(
                    endpoint: "/auth/refresh",
                    method: .POST,
                    body: refreshRequest,
                    requiresAuth: false
                )
                try tokenStorage.saveTokens(
                    accessToken: tokenResponse.access_token,
                    refreshToken: tokenResponse.refresh_token
                )
                
                // Retry original request
                request.setValue("Bearer \(tokenResponse.access_token)", forHTTPHeaderField: "Authorization")
                let (retryData, retryResponse) = try await session.data(for: request)
                
                guard let retryHttpResponse = retryResponse as? HTTPURLResponse,
                      (200...299).contains(retryHttpResponse.statusCode) else {
                    throw ApiError.httpError(statusCode: (retryResponse as? HTTPURLResponse)?.statusCode ?? 0)
                }
                
                return try JSONDecoder().decode(T.self, from: retryData)
            } else {
                throw ApiError.unauthorized
            }
        }
        
        guard (200...299).contains(httpResponse.statusCode) else {
            if let error = try? JSONDecoder().decode(APIError.self, from: data) {
                throw ApiError.serverError(message: error.detail)
            }
            throw ApiError.httpError(statusCode: httpResponse.statusCode)
        }
        
        return try JSONDecoder().decode(T.self, from: data)
    }
}

enum HTTPMethod: String {
    case GET = "GET"
    case POST = "POST"
    case PUT = "PUT"
    case DELETE = "DELETE"
}

enum ApiError: Error, LocalizedError {
    case invalidURL
    case invalidResponse
    case httpError(statusCode: Int)
    case serverError(message: String)
    case unauthorized
    case decodingError
    
    var errorDescription: String? {
        switch self {
        case .invalidURL:
            return "Invalid URL"
        case .invalidResponse:
            return "Invalid response"
        case .httpError(let statusCode):
            return "HTTP error: \(statusCode)"
        case .serverError(let message):
            return message
        case .unauthorized:
            return "Unauthorized"
        case .decodingError:
            return "Failed to decode response"
        }
    }
}



