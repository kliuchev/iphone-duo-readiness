import json
from pathlib import Path
import plistlib
import subprocess
import sys
import tempfile
import unittest
from analyze_ios_duo import DuoAnalyzer


class AnalyzerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path

    def scan(self, path=None):
        analyzer = DuoAnalyzer(path or self.root)
        analyzer.scan()
        return analyzer.report()

    def test_empty_is_not_ready(self):
        report = self.scan()
        self.assertIsNone(report['overall_readiness'])
        self.assertEqual(report['assessment_status'], 'insufficient_evidence')
        self.assertTrue(all(v is None for v in report['pillar_scores'].values()))

    def test_comments_literals_and_nested_comments(self):
        self.write('App.swift', '// UIScreen.main\n/* outer /* UIScreen.main */ inner */\nlet s = #"UIScreen.main"#\nlet t = """\nUIScreen.main\n"""\nlet u = "escaped \\" UIScreen.main"\n')
        self.assertEqual(self.scan()['issues'], [])

    def test_one_screen_issue_with_real_line(self):
        self.write('App.swift', '// comment\nlet width = UIScreen.main.bounds.width\n')
        issues = self.scan()['issues']
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]['line'], 2)

    def test_multiline_rotation_and_width_only(self):
        self.write('App.swift', 'override var shouldAutorotate: Bool {\n return false\n}\n.frame(\n width: 390\n)')
        self.assertEqual({i['rule_id'] for i in self.scan()['issues']}, {'rotation_disabled', 'fixed_frame'})

    def test_excludes_skill_examples_and_tests(self):
        for name in ('.agents/a.swift', 'Examples/b.swift', 'Tests/c.swift', 'Pods/d.swift'):
            self.write(name, 'UIScreen.main')
        self.write('App.swift', 'WindowGroup { ContentView() }')
        report = self.scan()
        self.assertEqual(report['files_scanned'], 1)
        self.assertEqual(report['issues'], [])
        self.assertIsNone(report['overall_readiness'])

    def test_binary_and_xml_plists_kept_separate(self):
        for name, enabled, fmt in [('App-Info.plist', True, plistlib.FMT_BINARY), ('Other.plist', False, plistlib.FMT_XML)]:
            (self.root / name).write_bytes(plistlib.dumps({'UIApplicationSceneManifest': {'UIApplicationSupportsMultipleScenes': enabled}}, fmt=fmt))
        report = self.scan()
        self.assertEqual({c['multiple_scenes'] for c in report['configurations']}, {True, False})
        self.assertEqual(report['issues'], [])

    def test_single_file_and_objc(self):
        path = self.write('App.mm', 'CGRect bounds = [[UIScreen mainScreen] bounds];')
        self.assertEqual(len(self.scan(path)['issues']), 1)

    def test_errors_visible_and_cli_fails(self):
        self.write('Info.plist', '<?xml version="1.0"?><plist><dict>')
        self.assertEqual(self.scan()['assessment_status'], 'incomplete')
        result = subprocess.run([sys.executable, str(Path(__file__).with_name('analyze_ios_duo.py')), str(self.root / 'missing'), '--json'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertTrue(json.loads(result.stdout)['errors'])

    def test_missing_manifest_is_unknown(self):
        (self.root / 'Info.plist').write_bytes(plistlib.dumps({'Unrelated': True}))
        self.assertIsNone(self.scan()['configurations'][0]['multiple_scenes'])


if __name__ == '__main__':
    unittest.main()
