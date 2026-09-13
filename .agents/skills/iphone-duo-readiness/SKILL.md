---
name: iphone-duo-readiness
description: >-
  Analyzes an iOS project (UIKit or SwiftUI) to evaluate its readiness for iPhone Duo
  (dual-screen / foldable hardware), identifies compatibility issues, calculates a 5-pillar
  readiness score, and generates step-by-step Swift refactoring code.
---

# 📱 iPhone Duo iOS Project Readiness Skill

Use this skill when asked to audit an iOS codebase for **iPhone Duo** (dual-screen / foldable hardware), assess multi-window/multi-screen compatibility, identify layout blockers, or migrate legacy single-screen UIKit/SwiftUI code to dynamic dual-display posture architectures.

---

## 🎯 Overview of iPhone Duo Hardware & OS Model

iPhone Duo introduces a dual-display form factor with a central hinge seam and dynamic posture states:
- **Dual-Portrait Mode**: Side-by-side screens in portrait orientation.
- **Dual-Landscape / Book Mode**: Side-by-side screens in landscape orientation.
- **Tabletop / Fold Mode**: Upper screen displays primary content; lower screen acts as control/keyboard/canvas.
- **Span vs Split**: App can run in a single window on screen A, span across screen A + B over the seam, or run two simultaneous instances in separate scene sessions.

---

## 📋 Audit Workflow for AI Agents

Follow these 5 sequential phases when invoked to audit a repository or single file:

### Phase 1: Automated Static Code Analysis
Run the built-in scanner script from the workspace root:

```bash
python3 .agents/skills/iphone-duo-readiness/scripts/analyze_ios_duo.py .
```

If python is unavailable or if auditing a single file/snippet manually, perform a pattern search for these anti-patterns:
- `UIScreen.main` or `UIScreen.main.bounds`
- `UIApplication.shared.keyWindow`
- Hardcoded frame widths/heights (`375`, `390`, `414`, `430`)
- `UIApplicationSupportsMultipleScenes = false` in `Info.plist`
- Hardcoded orientation locks (`portraitOnly`, `shouldAutorotate = false`)

---

### Phase 2: 5-Pillar Architectural Deep-Dive

Evaluate the codebase across the 5 core pillars of iPhone Duo compatibility:

#### 1. Multi-Window & Scene Architecture (Weight: 25%)
- [ ] `Info.plist` contains `UIApplicationSupportsMultipleScenes = true`.
- [ ] App uses `UIWindowSceneDelegate` / `SceneDelegate` or SwiftUI `WindowGroup`.
- [ ] App can request new scenes dynamically via `UIApplication.shared.requestSceneSessionActivation`.
- [ ] State restoration (`NSUserActivity`) is implemented for scene session lifecycle.

#### 2. Adaptive Layout & Size Classes (Weight: 25%)
- [ ] SwiftUI uses `NavigationSplitView`, `ViewThatFits`, or relative layout containers.
- [ ] UIKit uses `UISplitViewController` or Auto Layout constraints (`leadingAnchor`, `trailingAnchor`).
- [ ] Views adapt cleanly between Compact and Regular `horizontalSizeClass` and `verticalSizeClass`.
- [ ] No hardcoded view dimensions derived from static single-screen iPhone viewports.

#### 3. Modern Screen & Bounds APIs (Weight: 20%)
- [ ] Zero usage of deprecated `UIScreen.main` (replaced by scene-aware screen/window bounds or `GeometryReader`).
- [ ] Key window access is derived from active `UIWindowScene`.

#### 4. Dual-Screen & Seam/Hinge Adaptivity (Weight: 15%)
- [ ] UI controls and primary text avoid the central display seam / hinge occlusion zone.
- [ ] Safe area insets (`safeAreaInsets` / `safeAreaPadding`) are respected.
- [ ] Layout responds to posture changes (Book, Tabletop, Extended canvas).

#### 5. Multitasking & Drag-and-Drop (Weight: 15%)
- [ ] Supports drag-and-drop between left and right screens (`UIDragInteraction`, `UIDropInteraction`, `.onDrag`, `.onDrop`).
- [ ] Cross-window item activation and side-by-side interaction supported.

---

### Phase 3: Calculate the iPhone Duo Readiness Index

Calculate the readiness score using the formula in [duo_scoring_rubric.md](./references/duo_scoring_rubric.md):

$$\text{Readiness Index} = \sum_{p \in \text{Pillars}} \text{Score}_p \times \text{Weight}_p$$

Score Categories:
- **85 - 100%**: 🟢 **DUO-READY** (Minor optimizations only).
- **60 - 84%**: 🟡 **PARTIALLY READY** (Requires scene & layout refactoring).
- **0 - 59%**: 🔴 **NOT READY** (Contains critical multi-window / screen API blockers).

---

### Phase 4: Generate Diagnostic Audit Report

Format the diagnostic report for the user using this standard markdown structure:

```markdown
# 📱 iPhone Duo Readiness Report

**Overall Readiness Score:** [Score]% [Badge]

## 📊 Pillar Breakdown
| Pillar | Weight | Score | Status |
| :--- | :--- | :--- | :--- |
| Multi-Window & Scene Architecture | 25% | X% | [Pass/Warn/Fail] |
| Adaptive Layout & Size Classes | 25% | X% | [Pass/Warn/Fail] |
| Modern Screen APIs | 20% | X% | [Pass/Warn/Fail] |
| Dual-Screen & Seam/Hinge Adaptivity | 15% | X% | [Pass/Warn/Fail] |
| Multitasking & Drag-and-Drop | 15% | X% | [Pass/Warn/Fail] |

## 🚨 Critical Blockers & Anti-Patterns
- [File:Line] issue description and remediation.

## 🛠 Actionable Code Refactoring Plan
Step-by-step instructions with code diffs.
```

---

### Phase 5: Produce Code Refactoring Solutions

Refer to reference guides and examples for concrete Swift refactoring recipes:
- Architectural patterns: [duo_architecture_patterns.md](./references/duo_architecture_patterns.md)
- Detailed checklist: [duo_audit_checklist.md](./references/duo_audit_checklist.md)
- SwiftUI before/after: [swiftui_duo_migration.swift](./examples/swiftui_duo_migration.swift)
- UIKit before/after: [uikit_duo_migration.swift](./examples/uikit_duo_migration.swift)

---

## 💡 Quick Code Refactoring Cheat Sheet

### 1. Replacing `UIScreen.main`
❌ **Bad (Legacy UIKit)**:
```swift
let screenWidth = UIScreen.main.bounds.width
```
✅ **Good (Duo-Ready UIKit)**:
```swift
guard let windowScene = view.window?.windowScene else { return }
let sceneWidth = windowScene.screen.bounds.width
```

### 2. Replacing Single Stack View with Two-Pane Navigation (SwiftUI)
❌ **Bad (Single Screen Only)**:
```swift
NavigationStack {
    List(items) { item in
        NavigationLink(item.title, destination: DetailView(item: item))
    }
}
```
✅ **Good (Duo-Ready Two-Pane Split)**:
```swift
NavigationSplitView {
    List(items, selection: $selectedItem) { item in
        Text(item.title)
    }
} detail: {
    if let item = selectedItem {
        DetailView(item: item)
    } else {
        ContentUnavailableView("Select an Item", systemImage: "sidebar.left")
    }
}
.navigationSplitViewStyle(.balanced)
```

### 3. Avoiding Hinge Seam Occlusion (SwiftUI)
```swift
struct HingeAwareContainer<Content: View>: View {
    let content: Content
    
    var body: some View {
        GeometryReader { proxy in
            let isDualScreen = proxy.size.width > 700
            if isDualScreen {
                HStack(spacing: 24) { // 24pt seam buffer zone
                    content
                }
            } else {
                content
            }
        }
    }
}
```
