# iPhone Duo Readiness

A skill for reviewing responsive SwiftUI and UIKit layouts. Finds common mistakes such as screen-based sizing, `isIpad` layout assumptions, fixed text heights, overlapping controls, missing scrolling, and incorrect safe-area handling.

## Installation

Run in your iOS project's root:

```bash
npx iphone-duo-readiness
```

Or without Node.js:

```bash
curl -fsSL https://raw.githubusercontent.com/kliuchev/iphone-duo-readiness/main/install.sh | bash
```

## Usage

Ask your coding agent:

```text
Use $iphone-duo-readiness to review the UI in /path/to/project.
```

Or reference the skill file directly:

```text
Read .agents/skills/iphone-duo-readiness/SKILL.md and review the UI in /path/to/project.
```

Returns source locations, what can break, and suggested fixes. Static code review only — no builds, simulators, or changes to your app.
