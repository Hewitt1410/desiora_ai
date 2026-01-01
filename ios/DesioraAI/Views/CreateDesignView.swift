import SwiftUI
import PhotosUI

struct CreateDesignView: View {
    @EnvironmentObject var designJobViewModel: DesignJobViewModel
    @State private var selectedImage: UIImage?
    @State private var showingImagePicker = false
    @State private var showingCamera = false
    @State private var selectedStyle = "modern"
    @State private var selectedRoomType = "living_room"
    @State private var customPrompt = ""
    
    let styles = ["modern", "minimalist", "rustic", "scandinavian", "industrial", "bohemian", "traditional", "contemporary"]
    let roomTypes = ["living_room", "bedroom", "kitchen", "bathroom", "dining_room", "office"]
    
    var body: some View {
        NavigationView {
            Form {
                Section(header: Text("Image")) {
                    if let image = selectedImage {
                        Image(uiImage: image)
                            .resizable()
                            .scaledToFit()
                            .frame(height: 200)
                            .cornerRadius(8)
                    }
                    
                    HStack {
                        Button("Select from Gallery") {
                            showingImagePicker = true
                        }
                        .buttonStyle(.bordered)
                        
                        Button("Take Photo") {
                            showingCamera = true
                        }
                        .buttonStyle(.bordered)
                    }
                }
                
                Section(header: Text("Design Style")) {
                    Picker("Style", selection: $selectedStyle) {
                        ForEach(styles, id: \.self) { style in
                            Text(style.capitalized).tag(style)
                        }
                    }
                }
                
                Section(header: Text("Room Type")) {
                    Picker("Room Type", selection: $selectedRoomType) {
                        ForEach(roomTypes, id: \.self) { room in
                            Text(room.replacingOccurrences(of: "_", with: " ").capitalized).tag(room)
                        }
                    }
                }
                
                Section(header: Text("Custom Prompt (Optional)")) {
                    TextEditor(text: $customPrompt)
                        .frame(height: 100)
                }
                
                Section {
                    Button(action: {
                        guard let image = selectedImage else { return }
                        Task {
                            await designJobViewModel.createJob(
                                image: image,
                                style: selectedStyle,
                                roomType: selectedRoomType,
                                prompt: customPrompt
                            )
                        }
                    }) {
                        if designJobViewModel.isLoading {
                            HStack {
                                ProgressView()
                                Text("Creating...")
                            }
                            .frame(maxWidth: .infinity)
                        } else {
                            Text("Create Design Job")
                                .frame(maxWidth: .infinity)
                        }
                    }
                    .buttonStyle(.borderedProminent)
                    .disabled(selectedImage == nil || designJobViewModel.isLoading)
                }
            }
            .navigationTitle("Create Design")
            .sheet(isPresented: $showingImagePicker) {
                ImagePicker(image: $selectedImage, sourceType: .photoLibrary)
            }
            .sheet(isPresented: $showingCamera) {
                ImagePicker(image: $selectedImage, sourceType: .camera)
            }
            .navigationDestination(item: $designJobViewModel.currentJob) { job in
                DesignJobDetailView(jobId: job.id)
                    .environmentObject(designJobViewModel)
            }
        }
    }
}

struct ImagePicker: UIViewControllerRepresentable {
    @Binding var image: UIImage?
    let sourceType: UIImagePickerController.SourceType
    @Environment(\.dismiss) var dismiss
    
    func makeUIViewController(context: Context) -> UIImagePickerController {
        let picker = UIImagePickerController()
        picker.sourceType = sourceType
        picker.delegate = context.coordinator
        return picker
    }
    
    func updateUIViewController(_ uiViewController: UIImagePickerController, context: Context) {}
    
    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }
    
    class Coordinator: NSObject, UIImagePickerControllerDelegate, UINavigationControllerDelegate {
        let parent: ImagePicker
        
        init(_ parent: ImagePicker) {
            self.parent = parent
        }
        
        func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey : Any]) {
            if let image = info[.originalImage] as? UIImage {
                parent.image = image
            }
            parent.dismiss()
        }
        
        func imagePickerControllerDidCancel(_ picker: UIImagePickerController) {
            parent.dismiss()
        }
    }
}




