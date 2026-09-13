#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const targetDir = process.argv[2] ? path.resolve(process.cwd(), process.argv[2]) : process.cwd();
const rootDir = path.resolve(__dirname, '..');

console.log(`📱 Installing iPhone Duo Readiness Skill into '${targetDir}'...`);

function copyRecursiveSync(src, dest) {
  const exists = fs.existsSync(src);
  const stats = exists && fs.statSync(src);
  const isDirectory = exists && stats.isDirectory();
  if (isDirectory) {
    if (!fs.existsSync(dest)) {
      fs.mkdirSync(dest, { recursive: true });
    }
    fs.readdirSync(src).forEach((childItemName) => {
      copyRecursiveSync(path.join(src, childItemName), path.join(dest, childItemName));
    });
  } else {
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    fs.copyFileSync(src, dest);
  }
}

try {
  // 1. Copy .agents/skills/iphone-duo-readiness
  const skillSrc = path.join(rootDir, '.agents', 'skills', 'iphone-duo-readiness');
  const skillDest = path.join(targetDir, '.agents', 'skills', 'iphone-duo-readiness');
  copyRecursiveSync(skillSrc, skillDest);

  // 2. Copy AGENTS.md & GEMINI.md
  ['AGENTS.md', 'GEMINI.md'].forEach(file => {
    const src = path.join(rootDir, file);
    if (fs.existsSync(src)) {
      fs.copyFileSync(src, path.join(targetDir, file));
    }
  });

  // 3. Copy Cursor rules
  const cursorRuleSrc = path.join(rootDir, '.cursor', 'rules', 'iphone-duo-readiness.mdc');
  if (fs.existsSync(cursorRuleSrc)) {
    copyRecursiveSync(cursorRuleSrc, path.join(targetDir, '.cursor', 'rules', 'iphone-duo-readiness.mdc'));
  }

  // 4. Copy Copilot instructions
  const copilotSrc = path.join(rootDir, '.github', 'copilot-instructions.md');
  if (fs.existsSync(copilotSrc)) {
    copyRecursiveSync(copilotSrc, path.join(targetDir, '.github', 'copilot-instructions.md'));
  }

  // Make python script executable
  const scriptPath = path.join(skillDest, 'scripts', 'analyze_ios_duo.py');
  if (fs.existsSync(scriptPath)) {
    try {
      fs.chmodSync(scriptPath, 0o755);
    } catch (e) {}
  }

  console.log('\n🎉 iPhone Duo Readiness Skill installed successfully!');
  console.log(`📁 Skill Location: ${skillDest}`);
  console.log('\nQuick Test Command:');
  console.log(`  python3 .agents/skills/iphone-duo-readiness/scripts/analyze_ios_duo.py .`);
} catch (err) {
  console.error('❌ Installation failed:', err.message);
  process.exit(1);
}
