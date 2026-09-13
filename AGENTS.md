# Universal AI Agent Customization Registry (AGENTS.md)

This project contains specialized AI agent skills located in `.agents/skills/`.

## Available Skills

### `iphone-duo-readiness`
- **Location**: [.agents/skills/iphone-duo-readiness/SKILL.md](file://.agents/skills/iphone-duo-readiness/SKILL.md)
- **Description**: Analyzes an iOS codebase (UIKit or SwiftUI) to evaluate readiness for iPhone Duo (dual-screen / foldable hardware), detects compatibility issues, calculates a 5-pillar readiness index, and generates Swift refactoring solutions.
- **Trigger**: When asked to check iPhone Duo compatibility, multi-window readiness, screen API deprecations, dynamic posture layouts, or dual-screen navigation.
- **Scanner Command**:
  ```bash
  python3 .agents/skills/iphone-duo-readiness/scripts/analyze_ios_duo.py .
  ```
