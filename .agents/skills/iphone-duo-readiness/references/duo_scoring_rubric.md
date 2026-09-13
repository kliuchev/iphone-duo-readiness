# 📊 iPhone Duo Readiness Scoring Rubric & Formula

This document defines the mathematical evaluation model and scoring criteria used by AI agents to grade iOS repositories for iPhone Duo compatibility.

---

## Evaluation Formula

The Overall Readiness Index ($R$) is calculated as the weighted sum of scores across 5 core pillars:

$$R = (S_{\text{scene}} \times 0.25) + (S_{\text{layout}} \times 0.25) + (S_{\text{api}} \times 0.20) + (S_{\text{hinge}} \times 0.15) + (S_{\text{drop}} \times 0.15)$$

Where each pillar score $S \in [0, 100]$.

---

## Pillar Weighting Breakdown

| Pillar ID | Pillar Name | Weight | Focus Areas |
| :--- | :--- | :--- | :--- |
| `S_scene` | Multi-Window & Scene Architecture | **25%** | `Info.plist` scene manifest, `UIWindowSceneDelegate`, `WindowGroup`, `requestSceneSessionActivation` |
| `S_layout` | Adaptive Layout & Size Classes | **25%** | `NavigationSplitView`, `UISplitViewController`, `horizontalSizeClass`, removing fixed width bounds |
| `S_api` | Modern Screen & Bounds APIs | **20%** | Deprecation of `UIScreen.main` and `keyWindow`, using scene-aware window geometry |
| `S_hinge` | Dual-Screen & Seam/Hinge Adaptivity | **15%** | Seam buffer clearance, safeAreaInsets, posture state handling (Book/Tabletop) |
| `S_drop` | Multitasking & Drag-and-Drop | **15%** | Inter-scene data transfer, `UIDragInteraction`, `Transferable`, background lifecycle |

---

## Scoring Penalties & Deductions Table

| Violation | Severity | Pillar Impacted | Penalty Points |
| :--- | :--- | :--- | :--- |
| `UIScreen.main` or `UIScreen.main.bounds` | CRITICAL | `S_api` | -5 per occurrence (max -50) |
| `UIApplication.shared.keyWindow` | HIGH | `S_api` | -4 per occurrence (max -30) |
| `UIApplicationSupportsMultipleScenes = false` | CRITICAL | `S_scene` | -20 (flat) |
| Missing Scene Manifest in `Info.plist` | HIGH | `S_scene` | -15 (flat) |
| Hardcoded portrait orientation lock (`portraitOnly`) | HIGH | `S_layout` | -15 (flat) |
| Hardcoded fixed frame width (`.frame(width: 390)`) | MEDIUM | `S_layout` | -3 per occurrence (max -30) |
| Placing interactive UI directly over central seam | MEDIUM | `S_hinge` | -10 per occurrence |
| No Drag & Drop protocol (`Transferable`) | LOW | `S_drop` | -10 (flat) |

---

## Readiness Tiers & Certification Badges

- **90% - 100% (Tier S - Duo Certified)**: Fully optimized for dual-screen multi-scene execution, posture transitions, and inter-window drag & drop.
- **75% - 89% (Tier A - Duo Compatible)**: Responsive and multi-scene enabled; requires minor hinge alignment or posture enhancements.
- **50% - 74% (Tier B - Partially Ready)**: Contains legacy screen calls or rigid stack layouts that impair dual display experience.
- **0% - 49% (Tier C - Blocked / Not Ready)**: Locked to single screen / single window with deprecated `UIScreen.main` dependencies.
