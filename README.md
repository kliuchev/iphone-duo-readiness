# 📱 Universal iPhone Duo Readiness Skill for AI Coding Agents

An open-standard **AI Agent Skill** designed to analyze iOS projects (SwiftUI & UIKit), determine readiness for dual-screen / foldable hardware (**iPhone Duo**), pinpoint compatibility blockers, and generate production-ready Swift code refactorings.

Compatible with **all AI Coding Agents**:
- 🤖 **Antigravity (AGY)**
- 🧠 **Claude Code**
- ⚡ **Cursor IDE**
- 🐙 **GitHub Copilot**
- 🌪 **Windsurf / Cascade**
- 🦙 **Roo Code / Cline**
- 💬 **ChatGPT / Custom GPTs / Open WebUI**

---

## 🚀 Quick Start & Installation in Any iOS Repository

### Option A: One-Liner Install (Recommended)
Run this single command inside the root folder of any iOS project:

```bash
curl -sSL https://raw.githubusercontent.com/kliuchev/iphone-duo-readiness/main/install.sh | bash
```

### Option B: NPX Installer
```bash
npx iphone-duo-readiness
```

### Option C: Manual Copy
```bash
cp -R .agents/skills/iphone-duo-readiness /path/to/your/ios-project/.agents/skills/
```

### Global Machine-Wide Installation (Antigravity / AGY)
```bash
mkdir -p ~/.gemini/config/skills
cp -R .agents/skills/iphone-duo-readiness ~/.gemini/config/skills/
```

---

## 🔍 How to Run the Audit

### 1. Automated Python Code Scanner
Run the standalone scanner script from the project directory:

```bash
python3 .agents/skills/iphone-duo-readiness/scripts/analyze_ios_duo.py .
```

To export raw JSON metrics:
```bash
python3 .agents/skills/iphone-duo-readiness/scripts/analyze_ios_duo.py . --json > duo_report.json
```

### 2. Prompting Any AI Agent
Ask your AI agent in natural language:

> *"Check this iOS project for iPhone Duo readiness. What issues exist, what is the readiness score, and how do we fix them?"*

The agent will automatically load `.agents/skills/iphone-duo-readiness/SKILL.md` and execute the 5-phase analysis pipeline.

---

## 📊 5-Pillar Readiness Index

| Pillar | Weight | Key Criteria |
| :--- | :--- | :--- |
| **1. Multi-Window & Scene Architecture** | **25%** | `Info.plist` `UIApplicationSupportsMultipleScenes = true`, `UIWindowSceneDelegate`, dynamic scene activation |
| **2. Adaptive Layout & Size Classes** | **25%** | `NavigationSplitView`, `UISplitViewController`, dynamic size class switching, flexible view bounds |
| **3. Modern Screen APIs** | **20%** | Deprecation of `UIScreen.main` and `keyWindow`, scene-based screen geometry |
| **4. Dual-Screen & Seam Adaptivity** | **15%** | Seam/hinge clearance, safe area margins, Tabletop / Book posture support |
| **5. Multitasking & Drag-and-Drop** | **15%** | Inter-scene data sharing via `Transferable`, `UIDragInteraction`, `UIDropInteraction` |

---

## 📁 Repository Structure

```text
.
├── AGENTS.md                                   # Universal agent skill registry
├── GEMINI.md                                   # Antigravity agent configuration
├── README.md                                   # Documentation and usage guide
├── install.sh                                  # 1-liner curl installer
├── package.json                                # NPM package manifest
├── bin/
│   └── cli.js                                  # NPX installer script
├── .cursor/
│   └── rules/
│       └── iphone-duo-readiness.mdc            # Cursor IDE native rule
├── .github/
│   └── copilot-instructions.md                 # GitHub Copilot custom instructions
└── .agents/
    └── skills/
        └── iphone-duo-readiness/
            ├── SKILL.md                        # Primary AI Agent Skill instruction file
            ├── scripts/
                └── analyze_ios_duo.py          # Python code scanner
            ├── references/
            │   ├── duo_audit_checklist.md      # 25-point audit checklist
            │   ├── duo_architecture_patterns.md # Swift architecture recipes
            │   └── duo_scoring_rubric.md       # Scoring weights and formula
            └── examples/
                ├── swiftui_duo_migration.swift # SwiftUI Before vs After migration
                └── uikit_duo_migration.swift   # UIKit Before vs After migration
```
