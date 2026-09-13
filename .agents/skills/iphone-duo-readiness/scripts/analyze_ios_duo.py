#!/usr/bin/env python3
"""
iPhone Duo iOS Project Readiness Analyzer
------------------------------------------
Scans Swift/UIKit/SwiftUI codebases and Info.plist configurations to evaluate
compatibility with dual-screen / foldable hardware (iPhone Duo).

Output: Comprehensive readiness report with scores across 5 core pillars,
issue locations, and recommended fixes.
"""

import os
import re
import json
import sys
import argparse
from pathlib import Path

# Pillar Definitions & Weights
PILLARS = {
    "multi_scene": {
        "title": "Multi-Window & Scene Architecture",
        "weight": 25,
        "description": "Supports multiple scenes, UIWindowSceneDelegate, and dynamic window activation."
    },
    "adaptive_layout": {
        "title": "Adaptive Layout & Size Classes",
        "weight": 25,
        "description": "Uses flexible constraints/containers and avoids hardcoded screen bounds."
    },
    "screen_api": {
        "title": "Modern Screen & Bounds API Usage",
        "weight": 20,
        "description": "Avoids deprecated APIs like UIScreen.main and legacy keyWindow access."
    },
    "duo_hinge": {
        "title": "Dual-Screen & Hinge/Posture Adaptivity",
        "weight": 15,
        "description": "Handles display seams, safe area insets, and device postures (Book, Tabletop)."
    },
    "multitasking": {
        "title": "Multitasking & Drag-and-Drop Integration",
        "weight": 15,
        "description": "Supports drag-and-drop between scenes and side-by-side data sharing."
    }
}

# Regex Patterns for Analysis
PATTERNS = {
    # Anti-patterns (Negative indicators)
    "uiscreen_main": {
        "regex": r'UIScreen\.main',
        "severity": "CRITICAL",
        "pillar": "screen_api",
        "message": "UIScreen.main is deprecated in iOS 16+ and breaks in multi-window / dual-screen setups. Use view.window.windowScene.screen or geometry insets.",
        "penalty": 5
    },
    "key_window": {
        "regex": r'UIApplication\.shared\.keyWindow',
        "severity": "HIGH",
        "pillar": "screen_api",
        "message": "UIApplication.shared.keyWindow is deprecated and unsafe on dual-screen setups. Derive window from UIWindowScene.",
        "penalty": 4
    },
    "hardcoded_screen_width": {
        "regex": r'UIScreen\.main\.bounds\.(width|height)',
        "severity": "CRITICAL",
        "pillar": "screen_api",
        "message": "Hardcoded screen bounds lookup assumption. Dynamic dual-display windows change bounds continuously.",
        "penalty": 5
    },
    "fixed_frame_dimensions": {
        "regex": r'\.frame\s*\(\s*width:\s*(375|390|414|430|393|428|360)\s*,\s*height:',
        "severity": "MEDIUM",
        "pillar": "adaptive_layout",
        "message": "Hardcoded view frame dimensions based on single-screen iPhone sizes. Use flexible frames or relative layout metrics.",
        "penalty": 3
    },
    "orientation_lock": {
        "regex": r'shouldAutorotate\s*=>\s*false|supportedInterfaceOrientations.*portraitOnly',
        "severity": "HIGH",
        "pillar": "adaptive_layout",
        "message": "Hardcoded portrait orientation locking prevents iPhone Duo dual-landscape/portrait transitions.",
        "penalty": 4
    },
    
    # Positive Indicators
    "scene_delegate": {
        "regex": r'UIWindowSceneDelegate|SceneDelegate',
        "pillar": "multi_scene",
        "reward": 6
    },
    "request_scene": {
        "regex": r'requestSceneSessionActivation',
        "pillar": "multi_scene",
        "reward": 5
    },
    "navigation_split_view": {
        "regex": r'NavigationSplitView|UISplitViewController',
        "pillar": "adaptive_layout",
        "reward": 7
    },
    "size_class_env": {
        "regex": r'@Environment\(\s*\\\.horizontalSizeClass\s*\)|traitCollectionDidChange',
        "pillar": "adaptive_layout",
        "reward": 6
    },
    "view_that_fits": {
        "regex": r'ViewThatFits|LayoutBuilder|GeometryReader',
        "pillar": "adaptive_layout",
        "reward": 4
    },
    "safe_area_insets": {
        "regex": r'safeAreaInsets|safeAreaPadding|safeAreaInset',
        "pillar": "duo_hinge",
        "reward": 5
    },
    "drag_drop": {
        "regex": r'UIDragInteraction|UIDropInteraction|\.onDrag|\.onDrop|dropDestination',
        "pillar": "multitasking",
        "reward": 6
    }
}

class DuoAnalyzer:
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.issues = []
        self.positive_findings = []
        self.files_scanned = 0
        self.plist_found = False
        self.multi_scene_enabled = False
        self.supported_orientations_valid = False
        self.pillar_scores = {key: 100 for key in PILLARS.keys()}

    def scan(self):
        for root, dirs, files in os.walk(self.root_dir):
            # Skip build/derived data/pods directories
            dirs[:] = [d for d in dirs if d not in ['.git', 'DerivedData', 'Pods', '.build', 'Carthage', 'fastlane']]
            
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix in ['.swift', '.m', '.h']:
                    self.scan_source_file(file_path)
                elif file.endswith('Info.plist'):
                    self.scan_plist_file(file_path)

        self.calculate_final_scores()

    def scan_source_file(self, path):
        self.files_scanned += 1
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
        except Exception:
            return

        rel_path = path.relative_to(self.root_dir)

        for idx, line in enumerate(lines, 1):
            for pattern_id, rule in PATTERNS.items():
                if re.search(rule["regex"], line):
                    if "penalty" in rule:
                        self.issues.append({
                            "file": str(rel_path),
                            "line": idx,
                            "code": line.strip(),
                            "severity": rule["severity"],
                            "pillar": rule["pillar"],
                            "message": rule["message"],
                            "penalty": rule["penalty"]
                        })
                        self.pillar_scores[rule["pillar"]] -= rule["penalty"]
                    elif "reward" in rule:
                        self.positive_findings.append({
                            "file": str(rel_path),
                            "line": idx,
                            "pillar": rule["pillar"],
                            "code": line.strip()
                        })

    def scan_plist_file(self, path):
        self.plist_found = True
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            if "UIApplicationSupportsMultipleScenes" in content:
                if "<true/>" in content.split("UIApplicationSupportsMultipleScenes")[1][:50]:
                    self.multi_scene_enabled = True
                    self.positive_findings.append({
                        "file": str(path.relative_to(self.root_dir)),
                        "line": 0,
                        "pillar": "multi_scene",
                        "code": "UIApplicationSupportsMultipleScenes = true"
                    })
                else:
                    self.issues.append({
                        "file": str(path.relative_to(self.root_dir)),
                        "line": 0,
                        "code": "UIApplicationSupportsMultipleScenes = false",
                        "severity": "CRITICAL",
                        "pillar": "multi_scene",
                        "message": "UIApplicationSupportsMultipleScenes is disabled in Info.plist. iPhone Duo requires multi-scene support.",
                        "penalty": 20
                    })
                    self.pillar_scores["multi_scene"] -= 20
            else:
                self.issues.append({
                    "file": str(path.relative_to(self.root_dir)),
                    "line": 0,
                    "code": "Missing UIApplicationSupportsMultipleScenes",
                    "severity": "HIGH",
                    "pillar": "multi_scene",
                    "message": "Info.plist does not define UIApplicationSupportsMultipleScenes manifest.",
                    "penalty": 15
                })
                self.pillar_scores["multi_scene"] -= 15
        except Exception:
            pass

    def calculate_final_scores(self):
        # Clamp pillar scores between 0 and 100
        for pillar in self.pillar_scores:
            self.pillar_scores[pillar] = max(0, min(100, self.pillar_scores[pillar]))

        # Calculate weighted overall index
        total_score = 0
        total_weight = 0
        for key, info in PILLARS.items():
            total_score += self.pillar_scores[key] * (info["weight"] / 100.0)
            total_weight += info["weight"]

        self.overall_readiness = round(total_score, 1)

    def generate_markdown_report(self):
        lines = []
        lines.append("# 📱 iPhone Duo Readiness Audit Report")
        lines.append(f"**Target Directory:** `{self.root_dir.resolve()}`")
        lines.append(f"**Files Scanned:** {self.files_scanned}")
        lines.append(f"**Overall Readiness Score:** `{self.overall_readiness}%`\n")

        # Rating badge logic
        if self.overall_readiness >= 85:
            badge = "🟢 **DUO-READY**: The project handles dynamic scenes, adaptive layouts, and modern APIs well."
        elif self.overall_readiness >= 60:
            badge = "🟡 **PARTIALLY READY**: Needs multi-scene and layout adaptations for dual screen."
        else:
            badge = "🔴 **NOT READY**: Contains critical blockers (legacy UIScreen APIs, single window locks)."
        lines.append(f"> {badge}\n")

        lines.append("## 📊 Pillar Breakdown\n")
        lines.append("| Pillar | Weight | Score | Status |")
        lines.append("| :--- | :--- | :--- | :--- |")

        for key, info in PILLARS.items():
            score = self.pillar_scores[key]
            status = "✅ Pass" if score >= 80 else ("⚠️ Warning" if score >= 50 else "❌ Action Required")
            lines.append(f"| **{info['title']}** | {info['weight']}% | `{score}%` | {status} |")

        lines.append("\n## 🚨 Diagnostic Findings & Issues\n")
        if not self.issues:
            lines.append("🎉 No critical anti-patterns or blockers detected!")
        else:
            # Group by severity
            severities = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
            for sev in severities:
                sev_issues = [i for i in self.issues if i["severity"] == sev]
                if sev_issues:
                    lines.append(f"### {sev} Severity ({len(sev_issues)})\n")
                    for issue in sev_issues:
                        lines.append(f"- **[{issue['pillar'].upper()}]** `{issue['file']}:{issue['line']}`")
                        lines.append(f"  - **Issue:** {issue['message']}")
                        lines.append(f"  - **Code:** `{issue['code']}`\n")

        lines.append("\n## 🛠 Recommended Next Steps for iPhone Duo Adaptation")
        lines.append("1. **Enable Multi-Scene Support**: Ensure `Info.plist` sets `UIApplicationSupportsMultipleScenes = true` and adopt `UIWindowSceneDelegate`.")
        lines.append("2. **Eliminate `UIScreen.main`**: Replace deprecated single screen references with scene window context or `GeometryReader`.")
        lines.append("3. **Adopt Two-Pane Layouts**: Refactor rigid stack views into `NavigationSplitView` (SwiftUI) or `UISplitViewController` (UIKit).")
        lines.append("4. **Add Hinge & Seam Awareness**: Ensure UI controls do not intersect display fold lines.")
        lines.append("5. **Enable Multi-Window Drag & Drop**: Allow data transfers between left and right screens.")

        return "\n".join(lines)

    def generate_json_report(self):
        return json.dumps({
            "overall_readiness": self.overall_readiness,
            "files_scanned": self.files_scanned,
            "pillar_scores": self.pillar_scores,
            "issues": self.issues,
            "positive_findings": self.positive_findings
        }, indent=2)

def main():
    parser = argparse.ArgumentParser(description="Analyze iOS Project for iPhone Duo Readiness")
    parser.add_argument("path", nargs="?", default=".", help="Path to iOS project root directory")
    parser.add_argument("--json", action="store_true", help="Output raw JSON format")
    args = parser.parse_args()

    analyzer = DuoAnalyzer(args.path)
    analyzer.scan()

    if args.json:
        print(analyzer.generate_json_report())
    else:
        print(analyzer.generate_markdown_report())

if __name__ == "__main__":
    main()
