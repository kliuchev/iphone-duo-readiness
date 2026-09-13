#!/usr/bin/env python3
"""Collect static review candidates; never infer hardware readiness from tokens."""
import argparse
import json
import os
from pathlib import Path
import plistlib
import re
from xml.parsers.expat import ExpatError

STRING_START = re.compile(r'(\#*)("""|")')

PILLARS = ('multi_scene', 'adaptive_layout', 'screen_api', 'duo_hinge', 'multitasking')
EXCLUDED = {'.git', '.agents', '.codex', 'DerivedData', 'Pods', '.build', 'build',
            'Carthage', 'node_modules', 'vendor', 'Examples', 'examples', 'Tests', 'tests'}
RULES = (
    ('screen_lookup', 'screen_api', r'\bUIScreen\s*\.\s*main\b|\[\s*UIScreen\s+mainScreen\s*\]',
     'Review screen lookup: layout needs container bounds; screen properties need the originating scene.'),
    ('global_key_window', 'screen_api', r'\bUIApplication\s*\.\s*shared\s*\.\s*keyWindow\b|\[\s*\[\s*UIApplication\s+sharedApplication\s*\]\s+keyWindow\s*\]',
     'Review global key-window access; prefer the originating view/window.'),
    ('fixed_frame', 'adaptive_layout', r'\.frame\s*\([^)]*?\b(?:width|height)\s*:\s*(?:360|375|390|393|414|428|430)(?:\.0)?\b',
     'Review a viewport-sized constant; fixed dimensions can be intentional for individual controls.'),
    ('rotation_disabled', 'adaptive_layout', r'\bshouldAutorotate\s*:\s*Bool\s*\{\s*(?:return\s+)?false\b|\bshouldAutorotate\s*\{\s*return\s+NO\b',
     'Review disabled rotation against supported product/device workflows.'),
    ('portrait_mask', 'adaptive_layout', r'\bsupportedInterfaceOrientations\s*:\s*UIInterfaceOrientationMask\s*\{\s*(?:return\s+)?\.portrait\b',
     'Review portrait-only orientation policy in the app target.'),
)
SIGNALS = (
    ('multi_scene', r'\b(?:WindowGroup|UIWindowSceneDelegate|requestSceneSessionActivation)\b'),
    ('adaptive_layout', r'\b(?:NavigationSplitView|UISplitViewController|GeometryReader|ViewThatFits|horizontalSizeClass|leadingAnchor)\b'),
    ('duo_hinge', r'\b(?:safeAreaInsets|safeAreaPadding|safeAreaInset|safeAreaLayoutGuide)\b'),
    ('multitasking', r'\b(?:UIDragInteraction|UIDropInteraction|Transferable)\b|\.(?:onDrag|onDrop|draggable|dropDestination)\b'),
)


def code_only(source):
    """Mask comments/literals, preserving offsets and lines (not a Swift parser).

    Handles nested block comments and Swift raw/multiline strings. Interpolated
    expressions and regex literals are not parsed; inspect these manually.
    """
    result = list(source)
    i = 0
    while i < len(source):
        start = i
        if source.startswith('//', i):
            end = source.find('\n', i)
            i = len(source) if end < 0 else end
        elif source.startswith('/*', i):
            depth = 1
            i += 2
            while i < len(source) and depth:
                if source.startswith('/*', i):
                    depth += 1
                    i += 2
                elif source.startswith('*/', i):
                    depth -= 1
                    i += 2
                else:
                    i += 1
        else:
            match = STRING_START.match(source, i)
            if match:
                hashes, quote = match.groups()
                closing = quote + hashes
                i += len(match.group())
                while i < len(source):
                    if source.startswith('\\' + hashes, i):
                        i += 2 + len(hashes)
                    elif source.startswith(closing, i):
                        i += len(closing)
                        break
                    else:
                        i += 1
            elif source[i] == "'":
                i += 1
                while i < len(source):
                    if source[i] == '\\':
                        i += 2
                    elif source[i] == "'":
                        i += 1
                        break
                    else:
                        i += 1
            else:
                i += 1
                continue
        for j in range(start, min(i, len(source))):
            if source[j] != '\n':
                result[j] = ' '
    return ''.join(result)


class DuoAnalyzer:
    def __init__(self, root_dir, exclude=()):
        self.root_dir = Path(root_dir)
        self.exclude = EXCLUDED | set(exclude)
        self.issues = []
        self.positive_findings = []  # Backward-compatible name: signals, not passes.
        self.configurations = []
        self.errors = []
        self.files_scanned = 0
        self.pillar_scores = dict.fromkeys(PILLARS)
        self.overall_readiness = None

    def relative(self, path):
        return str(path.relative_to(self.root_dir)) if self.root_dir.is_dir() else path.name

    def scan(self):
        if not self.root_dir.exists():
            self.errors.append({'file': str(self.root_dir), 'message': 'Input does not exist'})
        elif self.root_dir.is_file():
            self.scan_file(self.root_dir)
        else:
            def walk_error(error):
                self.errors.append({'file': str(error.filename), 'message': str(error)})
            for root, dirs, files in os.walk(self.root_dir, onerror=walk_error):
                dirs[:] = sorted(d for d in dirs if d not in self.exclude and not Path(root, d).is_symlink())
                for name in sorted(files):
                    path = Path(root, name)
                    if not path.is_symlink():
                        self.scan_file(path)
        self.assessment_status = ('incomplete' if self.errors else
                                  'needs_review' if self.files_scanned else 'insufficient_evidence')

    def scan_file(self, path):
        try:
            if path.suffix in {'.swift', '.m', '.mm', '.h'}:
                source = path.read_text(encoding='utf-8')
                self.files_scanned += 1
                clean = code_only(source)
                for rule_id, pillar, pattern, message in RULES:
                    for match in re.finditer(pattern, clean):
                        self.issues.append({'rule_id': rule_id, 'file': self.relative(path),
                                            'line': clean.count('\n', 0, match.start()) + 1,
                                            'pillar': pillar, 'severity': 'REVIEW',
                                            'confidence': 'heuristic', 'message': message})
                for pillar, pattern in SIGNALS:
                    for match in re.finditer(pattern, clean):
                        self.positive_findings.append({'file': self.relative(path),
                            'line': clean.count('\n', 0, match.start()) + 1,
                            'pillar': pillar, 'code': match.group(), 'status': 'unverified_signal'})
            elif path.suffix == '.plist':
                with path.open('rb') as stream:
                    config = plistlib.load(stream)
                if not isinstance(config, dict):
                    raise ValueError('Plist root is not a dictionary')
                manifest = config.get('UIApplicationSceneManifest', {})
                if not isinstance(manifest, dict):
                    raise ValueError('UIApplicationSceneManifest is not a dictionary')
                enabled = manifest.get('UIApplicationSupportsMultipleScenes')
                if enabled is not None and not isinstance(enabled, bool):
                    raise ValueError('UIApplicationSupportsMultipleScenes is not a boolean')
                self.configurations.append({'file': self.relative(path),
                    'multiple_scenes': enabled,
                    'orientations': {k: v for k, v in config.items() if k.startswith('UISupportedInterfaceOrientations')},
                    'status': 'target_and_effective_build_settings_unverified'})
        except (OSError, UnicodeError, ValueError, ExpatError, plistlib.InvalidFileException) as error:
            self.errors.append({'file': self.relative(path), 'message': str(error)})

    def report(self):
        return {'schema_version': 2, 'overall_readiness': None,
                'assessment_status': self.assessment_status, 'files_scanned': self.files_scanned,
                'pillar_scores': self.pillar_scores, 'issues': self.issues,
                'positive_findings': self.positive_findings, 'configurations': self.configurations,
                'errors': self.errors, 'limitations': [
                    'Static candidates only; no readiness or certification verdict.',
                    'No target membership, build settings, generated plist, or conditional-compilation evaluation.',
                    'Limited Swift/Objective-C lexical patterns; interpolation expressions, regex literals and indirect calls need manual review.',
                    'Scene correctness, navigation, accessibility, posture and drag/drop require manual/runtime checks.',
                    'Excluded directory names: ' + ', '.join(sorted(self.exclude))]}

    def generate_json_report(self):
        return json.dumps(self.report(), indent=2)

    def generate_markdown_report(self):
        lines = ['# iOS / iPhone Duo static review',
                 f'Status: **{self.assessment_status}**; source files read: {self.files_scanned}.',
                 'Readiness score: unavailable. All five review areas require evidence.', '', '## Candidates']
        for issue in self.issues:
            lines.append(f"- `{issue['file']}:{issue['line']}` [{issue['rule_id']}]: {issue['message']}")
        if not self.issues:
            lines.append('No matching candidates; this does not establish compatibility.')
        lines.extend(['', '## Configuration observations'])
        for config in self.configurations:
            lines.append(f"- `{config['file']}`: {json.dumps(config, sort_keys=True)}")
        lines.extend(['', '## Read/parse errors'])
        lines.extend(f"- `{error['file']}`: {error['message']}" for error in self.errors)
        lines.extend(['', '## Limits'])
        lines.extend('- ' + item for item in self.report()['limitations'])
        return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', nargs='?', default='.')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--exclude', action='append', default=[], metavar='DIRECTORY_NAME')
    args = parser.parse_args()
    analyzer = DuoAnalyzer(args.path, args.exclude)
    analyzer.scan()
    print(analyzer.generate_json_report() if args.json else analyzer.generate_markdown_report())
    return 2 if analyzer.errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
