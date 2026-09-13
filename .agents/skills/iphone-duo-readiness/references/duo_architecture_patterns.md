# Focused layout fixes

- Replace screen-derived content widths with the current container's proposed size or relative constraints. `windowScene.screen.bounds` still measures a screen.
- Replace exact heights around text with minimum heights and allow wrapping. Use semantic text styles or scalable metrics for meaningful text; do not enlarge decorative art merely because text scales.
- Put a header, main control and footer in a shared stack/layout so they reserve space for each other. An offset on a greeting or independently bottom-aligned picker does not reserve that space.
- Where content can exceed available height, make it scrollable or offer a compact arrangement. Keep the main action reachable; do not blindly wrap flexible spacers/GeometryReader in an unbounded ScrollView.
- Keep backgrounds edge-to-edge while positioning interactive content inside the container's safe area. Do not add the same safe-area inset again to content already inset by its parent.
- Preserve the product's navigation. NavigationStack is fine for a single flow. A list/detail product may benefit from NavigationSplitView; it is not a prerequisite for responsiveness.

[SwiftUI example](../examples/swiftui_duo_migration.swift): a scrollable detail view with flexible width and semantic fonts, within list/detail navigation.
[UIKit example](../examples/uikit_duo_migration.swift): a scroll view with container-relative constraints and a Dynamic Type label.

Use these examples only when they fit the finding. Reviews describe the minimal fix without modifying or running the app.
