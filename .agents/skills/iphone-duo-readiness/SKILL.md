---
name: iphone-duo-readiness
description: Review iOS SwiftUI and UIKit source code for common nonresponsive UI mistakes. Find layout, sizing, text scaling, safe-area and keyboard issues and report exact locations with focused fixes. Use for responsive UI, adaptive layout, or iPhone Duo layout reviews.
---

# Static review of responsive iOS interfaces

Read the project's UI code and flag typical mistakes that prevent it adapting to different container sizes, text sizes, or safe areas. The result is a short code review with actionable file/line findings.

## Scope

This is a static source review. Read files and search code; do not build, run tests, launch the app/simulator, install tools, or inspect simulator devices as part of a review. Do not change the reviewed project unless the user asks for fixes. Runtime validation is a separate task only when explicitly requested.

Keep the review about layout and layout-related reachability of content/controls. Do not expand into audio, purchases, networking, general business logic, hardware research, scene lifecycle, or certification. The name does not require Duo-specific APIs, hinge detection, two-column navigation, multiple windows, or drag-and-drop. No readiness scores or pillar dashboards.

## Review

1. Locate the requested project and its UI sources. Read local instructions and source configuration only as needed to identify the active app and supported platforms. Prefer `rg --files` and targeted `rg` searches; skip dependencies, generated code, tests and examples.
2. Read [the layout checklist](references/duo_audit_checklist.md). Trace suspicious measurements and modifiers through parent containers and reusable views. Review main screens, onboarding, sheets, dialogs and settings as applicable; do not rely on a short regex whitelist of phone widths.
3. For each issue, identify what changes (width, available height, keyboard, text size, safe area, content length), the code's incorrect assumption, and the resulting clipping, overlap, unreadability or unreachable action. Derive this from source; runtime proof is not a prerequisite for a useful static finding. If the consequence depends on an unverified condition, say so in that finding rather than launching the app to resolve it.
4. Return the most useful findings first. Each should contain **file:line → problem → triggering condition / impact → focused fix**. Use inline code comments when available, without duplicating the whole report. Group repetitions of the same cause. Finish with one brief scope note: static review, app not run. If there are no concrete findings, say so.

Fixed constants are not automatically bugs: icon sizes, minimum tap targets, decorative shapes, readable max-width limits and intentional portrait-only design may be appropriate. `GeometryReader`, `ScrollView` and Auto Layout are not automatic passes either. Check whether they actually constrain and adapt the relevant content. Avoid claiming a layout breaks on a particular device based only on an imagined screen size.

For remediation examples consult [layout guidance](references/duo_architecture_patterns.md) when useful. Small local fixes are preferable to redesigning navigation. State the minimal change; do not rewrite the app during a review.

The legacy Python scanner is optional, only if specifically requested. It finds a few lexical candidates and misses most layout problems. Its JSON flags and null score fields are not the skill's report format.
