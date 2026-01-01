import SwiftUI

enum AppTheme: String, CaseIterable {
    case system
    case light
    case dark
    
    var colorScheme: ColorScheme? {
        switch self {
        case .system:
            return nil
        case .light:
            return .light
        case .dark:
            return .dark
        }
    }
    
    var displayName: String {
        switch self {
        case .system:
            return "System"
        case .light:
            return "Light"
        case .dark:
            return "Dark"
        }
    }
}

class ThemeManager: ObservableObject {
    @AppStorage("app_theme") private var themeRawValue: String = AppTheme.system.rawValue
    
    @Published var currentTheme: AppTheme {
        didSet {
            themeRawValue = currentTheme.rawValue
        }
    }
    
    init() {
        self.currentTheme = AppTheme(rawValue: themeRawValue) ?? .system
    }
    
    var colorScheme: ColorScheme? {
        currentTheme.colorScheme
    }
}


