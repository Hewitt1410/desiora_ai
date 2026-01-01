import Foundation

class TokenStorage {
    static let shared = TokenStorage()
    
    private let keychain = KeychainService.shared
    private let accessTokenKey = "access_token"
    private let refreshTokenKey = "refresh_token"
    
    private init() {}
    
    func saveTokens(accessToken: String, refreshToken: String) throws {
        try keychain.save(token: accessToken, forKey: accessTokenKey)
        try keychain.save(token: refreshToken, forKey: refreshTokenKey)
    }
    
    func getAccessToken() -> String? {
        return try? keychain.get(forKey: accessTokenKey)
    }
    
    func getRefreshToken() -> String? {
        return try? keychain.get(forKey: refreshTokenKey)
    }
    
    func clearTokens() throws {
        try keychain.delete(forKey: accessTokenKey)
        try keychain.delete(forKey: refreshTokenKey)
    }
    
    func hasTokens() -> Bool {
        return getAccessToken() != nil
    }
}


