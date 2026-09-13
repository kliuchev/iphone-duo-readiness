# 📱 iPhone Duo 25-Point Comprehensive Technical Audit Checklist

Use this checklist when conducting an exhaustive code review of an iOS project (SwiftUI or UIKit) for iPhone Duo dual-screen hardware readiness.

---

## Pillar 1: Multi-Window & Scene Architecture (25 Points)

- [ ] **1.1 Scene Manifest in Info.plist**: `UIApplicationSupportsMultipleScenes` is set to `true` under `UIApplicationSceneManifest`.
- [ ] **1.2 UIWindowSceneDelegate Adoption**: App uses `UIWindowSceneDelegate` / `SceneDelegate` for window lifecycle rather than single `UIApplicationDelegate.window`.
- [ ] **1.3 SwiftUI WindowGroup Multi-Windowing**: SwiftUI entrypoint uses `WindowGroup` with support for multiple scene instances.
- [ ] **1.4 Dynamic Scene Requesting**: App implements `UIApplication.shared.requestSceneSessionActivation` for launching secondary windows on demand (e.g., opening a document/detail in the second screen).
- [ ] **1.5 State Restoration & Persistence**: Implement `stateRestorationActivity(for sceneSession:)` and `NSUserActivity` so scenes preserve scroll offset, active tab, and draft data upon detachment/reattachment.

---

## Pillar 2: Adaptive Layout & Size Classes (25 Points)

- [ ] **2.1 Size Class Responsiveness**: Layouts adapt seamlessly between Compact (`.compact`) and Regular (`.regular`) horizontal and vertical size classes.
- [ ] **2.2 Master-Detail / Two-Pane Containers**: Uses `NavigationSplitView` (SwiftUI) or `UISplitViewController` (UIKit) instead of forced single `NavigationStack` / `UINavigationController`.
- [ ] **2.3 ViewThatFits & Relative Containers**: Uses `ViewThatFits`, `LayoutBuilder`, or `GeometryReader` instead of hardcoded pixel metrics.
- [ ] **2.4 Auto Layout Relative Anchors**: UIKit code uses `leadingAnchor`, `trailingAnchor`, and multiplier constraints instead of fixed frame widths.
- [ ] **2.5 Orientation Flexibility**: App allows all interface orientations (`UIInterfaceOrientationMaskAll`) and does not hardcode `shouldAutorotate = false` or `portraitOnly`.

---

## Pillar 3: Modern Screen & Bounds APIs (20 Points)

- [ ] **3.1 No `UIScreen.main` References**: Zero usage of `UIScreen.main` in codebase. All screen queries route through `windowScene.screen` or container bounds.
- [ ] **3.2 No `UIScreen.main.bounds`**: Screen size measurements are bound to the containing `UIWindowScene` or `GeometryProxy`, enabling correct bounds during dual-screen split.
- [ ] **3.3 Safe Key Window Access**: Eliminates `UIApplication.shared.keyWindow` in favor of scene window discovery (`view.window` or `connectedScenes`).
- [ ] **3.4 Dynamic Scale Factor**: Uses `traitCollection.displayScale` or scene scale factor instead of assuming single fixed scale factor.
- [ ] **3.5 Modern Screen Recording / Capture APIs**: Uses scene-based capture observation instead of global screen notifications.

---

## Pillar 4: Dual-Screen & Seam/Hinge Adaptivity (15 Points)

- [ ] **4.1 Seam/Hinge Occlusion Clearance**: Important interactive controls, CTA buttons, and readable body text maintain a safe buffer zone (16–32pt) around the central display fold line.
- [ ] **4.2 Safe Area Insets Integration**: Layout respects `safeAreaInsets` / `.safeAreaPadding()` across display boundaries.
- [ ] **4.3 Posture State Machine**: Code handles device posture transitions:
  - **Book Posture**: Side-by-side reading or two-pane editing.
  - **Tabletop Posture**: Top display for content video/canvas; bottom display for controls/keyboard.
  - **Single Display Posture**: Folded back into standard single screen mode.
- [ ] **4.4 Dynamic Aspect Ratio Transitions**: Smooth layout recalculation without visual jumps during posture changes (`viewWillTransition(to:with:)` or `.onChange(of: geometry)`).
- [ ] **4.5 Two-Page Reading Support**: Canvas or reader apps support page-turning across dual displays with aligned margins.

---

## Pillar 5: Multitasking & Drag-and-Drop Integration (15 Points)

- [ ] **5.1 Cross-Scene Drag-and-Drop**: Supports dragging items (text, images, links, documents) from Screen A scene into Screen B scene using `UIDragInteraction` / `UIDropInteraction` or `.onDrag` / `.onDrop`.
- [ ] **5.2 Transferable Protocol**: SwiftUI models conform to `Transferable` for smooth system-wide inter-app and inter-window drag operations.
- [ ] **5.3 Side-by-Side Multitasking**: App gracefully shares screen space with secondary apps without crashing or corrupting UI layout.
- [ ] **5.4 Keyboard Shortcut & Command Support**: Supports hardware keyboard shortcuts (`UIKeyCommand` / `.keyboardShortcut()`) when operating in dual-screen laptop/tabletop configuration.
- [ ] **5.5 Background Scene Pause/Resume**: App handles inactive/background state per-scene independently without interrupting active scene sessions.
