# 🏗 iPhone Duo Production Architecture Patterns (SwiftUI & UIKit)

This document provides modular, production-ready Swift code patterns for adapting iOS apps to iPhone Duo dual-screen hardware.

---

## 1. SwiftUI `TwoPaneView` Container

A reusable container that automatically splits into two independent panes when running on an expanded iPhone Duo display or wide viewport, while collapsing gracefully into a single navigation stack on compact screens.

```swift
import SwiftUI

public struct TwoPaneView<Primary: View, Secondary: View>: View {
    @Environment(\.horizontalSizeClass) private var horizontalSizeClass
    
    let primary: Primary
    let secondary: Secondary
    let seamWidth: CGFloat
    
    public init(
        seamWidth: CGFloat = 24,
        @ViewBuilder primary: () -> Primary,
        @ViewBuilder secondary: () -> Secondary
    ) {
        self.seamWidth = seamWidth
        self.primary = primary()
        self.secondary = secondary()
    }
    
    public var body: some View {
        GeometryReader { proxy in
            let isDualScreen = horizontalSizeClass == .regular || proxy.size.width > 680
            
            if isDualScreen {
                HStack(spacing: 0) {
                    primary
                        .frame(maxWidth: .infinity, maxHeight: .infinity)
                    
                    // Central Hinge Seam Buffer Zone
                    Color.clear
                        .frame(width: seamWidth)
                        .accessibilityHidden(true)
                    
                    secondary
                        .frame(maxWidth: .infinity, maxHeight: .infinity)
                }
            } else {
                primary
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
            }
        }
    }
}
```

---

## 2. Dynamic Scene Activation (Multi-Window Launcher)

Launch a secondary window/scene on the adjacent screen of iPhone Duo when a user taps an item.

```swift
import UIKit
import SwiftUI

public final class DuoSceneManager {
    public static let shared = DuoSceneManager()
    private init() {}
    
    /// Requests activation of a detail scene session on the adjacent display
    public func openDetailInNewWindow(itemID: String, userActivityType: String) {
        let userActivity = NSUserActivity(activityType: userActivityType)
        userActivity.userInfo = ["selected_item_id": itemID]
        
        let options = UIScene.ActivationRequestOptions()
        options.requestingScene = UIApplication.shared.connectedScenes
            .compactMap { $0 as? UIWindowScene }
            .first { $0.activationState == .foregroundActive }
        
        UIApplication.shared.requestSceneSessionActivation(
            nil, // nil creates a new session
            userActivity: userActivity,
            options: options
        ) { error in
            print("Failed to activate Duo scene session: \(error.localizedDescription)")
        }
    }
}
```

---

## 3. Posture State Machine (Tabletop / Book / Flat)

Detect device orientation and posture changes to adapt UI layout (e.g. video player on top, controls on bottom during Tabletop posture).

```swift
import SwiftUI
import Combine

public enum DuoDevicePosture: String, CaseIterable {
    case flat = "Flat"
    case book = "Book (Dual Portrait)"
    case tabletop = "Tabletop (Fold Angle)"
    case singleScreen = "Single Screen"
}

public final class PostureObserver: ObservableObject {
    @Published public private(set) var currentPosture: DuoDevicePosture = .flat
    private var cancellables = Set<AnyCancellable>()
    
    public init() {
        // Observe size changes & safe area shifts to infer posture
        NotificationCenter.default.publisher(for: UIDevice.orientationDidChangeNotification)
            .sink { [weak self] _ in
                self?.evaluatePosture()
            }
            .store(in: &cancellables)
    }
    
    public func evaluatePosture() {
        let orientation = UIDevice.current.orientation
        if orientation.isLandscape {
            self.currentPosture = .tabletop
        } else if orientation.isPortrait {
            self.currentPosture = .book
        } else {
            self.currentPosture = .flat
        }
    }
}
```

---

## 4. Transferable Drag-and-Drop between Scenes

Conform data models to `Transferable` to enable fluid drag-and-drop between left and right screen scenes on iPhone Duo.

```swift
import SwiftUI
import UniformTypeIdentifiers

public struct DuoDocumentItem: Codable, Transferable, Identifiable {
    public var id: UUID
    public var title: String
    public var content: String
    
    public static var transferRepresentation: some TransferRepresentation {
        CodableRepresentation(contentType: .utf8PlainText)
    }
}

struct DuoDragDropView: View {
    @State private var items: [DuoDocumentItem] = []
    
    var body: some View {
        List(items) { item in
            Text(item.title)
                .draggable(item)
        }
        .dropDestination(for: DuoDocumentItem.self) { droppedItems, location in
            for item in droppedItems {
                if !items.contains(where: { $0.id == item.id }) {
                    items.append(item)
                }
            }
            return true
        }
    }
}
```
