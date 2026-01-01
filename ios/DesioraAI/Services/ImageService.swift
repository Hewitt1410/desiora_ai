import Foundation
import UIKit

class ImageService {
    static let shared = ImageService()
    private let apiClient = ApiClient.shared
    
    private init() {}
    
    func uploadImage(image: UIImage, filename: String) async throws -> String {
        // Step 1: Get presigned URL
        guard let imageData = image.jpegData(compressionQuality: 0.8) else {
            throw ImageError.invalidImage
        }
        
        let presignRequest = PresignUploadRequest(
            filename: filename,
            content_type: "image/jpeg",
            file_size: imageData.count
        )
        
        let presignResponse: PresignUploadResponse = try await apiClient.request(
            endpoint: "/images/presign-upload",
            method: .POST,
            body: presignRequest,
            requiresAuth: true
        )
        
        // Step 2: Upload to S3
        guard let uploadURL = URL(string: presignResponse.upload_url) else {
            throw ImageError.invalidURL
        }
        
        var uploadRequest = URLRequest(url: uploadURL)
        uploadRequest.httpMethod = "PUT"
        uploadRequest.setValue("image/jpeg", forHTTPHeaderField: "Content-Type")
        uploadRequest.httpBody = imageData
        
        let (_, response) = try await URLSession.shared.data(for: uploadRequest)
        
        guard let httpResponse = response as? HTTPURLResponse,
              (200...299).contains(httpResponse.statusCode) else {
            throw ImageError.uploadFailed
        }
        
        // Step 3: Confirm upload
        let confirmRequest = ConfirmUploadRequest(s3_key: presignResponse.s3_key)
        let _: [String: String] = try await apiClient.request(
            endpoint: "/images/confirm-upload",
            method: .POST,
            body: confirmRequest,
            requiresAuth: true
        )
        
        return presignResponse.s3_key
    }
}

enum ImageError: Error, LocalizedError {
    case invalidImage
    case invalidURL
    case uploadFailed
    
    var errorDescription: String? {
        switch self {
        case .invalidImage:
            return "Invalid image"
        case .invalidURL:
            return "Invalid upload URL"
        case .uploadFailed:
            return "Failed to upload image"
        }
    }
}



