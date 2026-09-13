# GitHub Copilot Custom Instructions for iPhone Duo Readiness

When generating iOS Swift, SwiftUI, or UIKit code for this repository:

- Always adopt multi-scene architectures (`UIWindowSceneDelegate` / `WindowGroup`).
- Never use deprecated single-screen APIs such as `UIScreen.main` or `UIApplication.shared.keyWindow`.
- Support responsive two-pane navigation layouts using `NavigationSplitView` or `UISplitViewController`.
- Support cross-window drag-and-drop using `Transferable` and `UIDragInteraction`.
- Follow the full skill runbook in `.agents/skills/iphone-duo-readiness/SKILL.md`.
