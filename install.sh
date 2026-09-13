#!/usr/bin/env bash
# Universal Installer Script for iPhone Duo Readiness AI Agent Skill
set -e

REPO_URL="https://github.com/kliuchev/iphone-duo-readiness.git"
RAW_URL="https://raw.githubusercontent.com/kliuchev/iphone-duo-readiness/main"
TARGET_DIR="${1:-.}"

echo "📱 Installing iPhone Duo Readiness Skill into '${TARGET_DIR}'..."

# Ensure target directories exist
mkdir -p "${TARGET_DIR}/.agents/skills/iphone-duo-readiness"
mkdir -p "${TARGET_DIR}/.cursor/rules"
mkdir -p "${TARGET_DIR}/.github"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" 2>/dev/null && pwd || echo "")"

if [ -n "${SCRIPT_DIR}" ] && [ -d "${SCRIPT_DIR}/.agents/skills/iphone-duo-readiness" ]; then
    echo "Copying from local repository..."
    cp -R "${SCRIPT_DIR}/.agents/skills/iphone-duo-readiness/"* "${TARGET_DIR}/.agents/skills/iphone-duo-readiness/"
    cp "${SCRIPT_DIR}/AGENTS.md" "${SCRIPT_DIR}/GEMINI.md" "${TARGET_DIR}/" 2>/dev/null || true
    cp "${SCRIPT_DIR}/.cursor/rules/iphone-duo-readiness.mdc" "${TARGET_DIR}/.cursor/rules/" 2>/dev/null || true
    cp "${SCRIPT_DIR}/.github/copilot-instructions.md" "${TARGET_DIR}/.github/" 2>/dev/null || true
else
    echo "Downloading latest skill release from GitHub..."
    TMP_DIR=$(mktemp -d)
    git clone --depth 1 "${REPO_URL}" "${TMP_DIR}"
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
