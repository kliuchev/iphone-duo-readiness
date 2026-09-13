#!/usr/bin/env bash
# Universal Installer Script for iPhone Duo Readiness AI Agent Skill
set -e

REPO_URL="https://github.com/kliuchev/iphone-duo-readiness.git"
TARGET_DIR="${1:-.}"

echo "📱 Installing iPhone Duo Readiness Skill into '${TARGET_DIR}'..."

IS_LOCAL=0
# Check if running locally inside the source repository where SKILL.md already exists
if [ -f "AGENTS.md" ] && [ -f ".agents/skills/iphone-duo-readiness/SKILL.md" ]; then
    IS_LOCAL=1
fi

# Ensure target directories exist
mkdir -p "${TARGET_DIR}/.agents/skills/iphone-duo-readiness"
mkdir -p "${TARGET_DIR}/.cursor/rules"
mkdir -p "${TARGET_DIR}/.github"

if [ "${IS_LOCAL}" -eq 1 ]; then
    echo "Copying from local directory..."
    cp -R .agents/skills/iphone-duo-readiness/* "${TARGET_DIR}/.agents/skills/iphone-duo-readiness/"
    cp AGENTS.md GEMINI.md "${TARGET_DIR}/" 2>/dev/null || true
    cp .cursor/rules/iphone-duo-readiness.mdc "${TARGET_DIR}/.cursor/rules/" 2>/dev/null || true
    cp .github/copilot-instructions.md "${TARGET_DIR}/.github/" 2>/dev/null || true
else
    echo "Downloading latest skill release from GitHub..."
    TMP_DIR=$(mktemp -d)
    git clone --depth 1 "${REPO_URL}" "${TMP_DIR}" </dev/null >/dev/null 2>&1
    cp -R "${TMP_DIR}/.agents/skills/iphone-duo-readiness/"* "${TARGET_DIR}/.agents/skills/iphone-duo-readiness/"
    cp "${TMP_DIR}/AGENTS.md" "${TMP_DIR}/GEMINI.md" "${TARGET_DIR}/" 2>/dev/null || true
    cp "${TMP_DIR}/.cursor/rules/iphone-duo-readiness.mdc" "${TARGET_DIR}/.cursor/rules/" 2>/dev/null || true
    cp "${TMP_DIR}/.github/copilot-instructions.md" "${TARGET_DIR}/.github/" 2>/dev/null || true
    rm -rf "${TMP_DIR}"
fi

chmod +x "${TARGET_DIR}/.agents/skills/iphone-duo-readiness/scripts/analyze_ios_duo.py" 2>/dev/null || true

echo ""
echo "🎉 iPhone Duo Readiness Skill installed successfully!"
echo "📁 Skill Location: ${TARGET_DIR}/.agents/skills/iphone-duo-readiness"
echo ""
echo "Quick Test Command:"
echo "  python3 ${TARGET_DIR}/.agents/skills/iphone-duo-readiness/scripts/analyze_ios_duo.py ${TARGET_DIR}"
