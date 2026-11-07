"""Critical tests for source consistency, portability, and usable HTML output."""

import tempfile
import unittest
import subprocess
import sys
import re
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

from build_report import build, load_sources, render, validate_source


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.links = []
        self.tables = 0
        self.scripts = 0

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if "id" in attributes:
            self.ids.append(attributes["id"])
        if tag == "a":
            self.links.append(attributes.get("href", ""))
        self.tables += tag == "table"
        self.scripts += tag == "script"


class ReportTests(unittest.TestCase):
    def test_current_sources_are_valid(self):
        validate_source(load_sources())

    def test_academic_structure_and_reference_sequence(self):
        source = load_sources()
        self.assertIn('## Abstract — research-design edition', source)
        self.assertLess(source.index('# Chapter 5:'), source.index('# References'))
        bibliography = source.split('# References', 1)[1].split('# Project validation status', 1)[0]
        self.assertEqual(len(re.findall(r'^\w[^\n]+https://', bibliography, re.M)), 9)
        for caption in ('Table 1.2.', 'Table 2.1.', 'Table 3.2.', 'Table 4.1.', 'Table 5.1.', 'Table A.1.'):
            self.assertIn(caption, source)

    def test_submission_status_has_exactly_three_sections(self):
        status = (Path(__file__).resolve().parents[1] / 'FINAL_SUBMISSION_STATUS.md').read_text(encoding='utf-8')
        self.assertEqual(re.findall(r'^#+ (.+)$', status, re.M),
                         ['1. COMPLETED', '2. REQUIRES EXTERNAL INPUT', '3. HOW TO COMPLETE AFTER DATA ARRIVES'])

    def test_questionnaire_is_included_once(self):
        source = load_sources()
        self.assertEqual(source.count("A07b. Did operational AI use stop"), 1)

    def test_missing_source_has_clear_error(self):
        with self.assertRaisesRegex(ValueError, "Required source is missing"):
            load_sources(Path("not-a-real-report.md"))

    def test_missing_chapter_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Chapter 4"):
            validate_source(load_sources().replace("# Chapter 4:", "# Missing chapter:"))

    def test_machine_paths_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "Machine-specific"):
            validate_source(load_sources() + "\nC:/Users/example/report.md")

    def test_html_navigation_and_tables(self):
        page = PageParser()
        page.feed(render(load_sources()))
        self.assertEqual(len(page.ids), len(set(page.ids)))
        internal = [link[1:] for link in page.links if link.startswith("#")]
        self.assertGreaterEqual(len(internal), 7)
        self.assertTrue(all(anchor in page.ids for anchor in internal))
        self.assertGreaterEqual(page.tables, 5)
        self.assertTrue(any(link.startswith("https://doi.org/") for link in page.links))

    def test_raw_html_is_not_executed(self):
        page = PageParser()
        page.feed(render(load_sources() + "\n<script>alert('unsafe')</script>\n"))
        self.assertEqual(page.scripts, 0)

    def test_commands_are_formatted_as_code_and_appendix_title_is_subordinate(self):
        page = render(load_sources())
        self.assertIn('<pre><code class="language-sh">python research_pipeline.py', page)
        self.assertIn('<h2 id="mba-research-questionnaire-v03">', page)
        self.assertNotIn('<h1 id="mba-research-questionnaire-v03">', page)

    def test_build_writes_portable_file(self):
        with tempfile.TemporaryDirectory() as directory:
            output = build(Path(directory) / "nested" / "report.html")
            text = output.read_text(encoding="utf-8")
            self.assertTrue(text.startswith("<!doctype html>"))
            self.assertNotIn("C:/Users/", text)
            self.assertIn('name="viewport"', text)
            self.assertIn("window.print()", text)
            self.assertNotRegex(text, r'<(?:link|script)[^>]+(?:src|href)="https?://')

    def test_unreadable_output_fails_instead_of_reporting_success(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / 'directory.html'
            destination.mkdir()
            with self.assertRaises(OSError):
                build(destination)

    def test_preview_starts_and_serves_honest_report(self):
        with tempfile.TemporaryDirectory() as directory:
            build(Path(directory) / 'report.html')
            process = subprocess.Popen(
                [sys.executable, '-u', '-m', 'http.server', '0', '--bind', '127.0.0.1',
                 '--directory', directory], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True)
            try:
                line = process.stdout.readline()
                match = re.search(r'port (\d+)', line)
                self.assertIsNotNone(match, line)
                with urllib.request.urlopen(f'http://127.0.0.1:{match[1]}/report.html', timeout=5) as response:
                    self.assertEqual(response.status, 200)
                    page = response.read().decode('utf-8')
                self.assertIn('Appendix B: Data Dictionary', page)
                self.assertIn('No survey data have been collected', page)
                self.assertNotIn('SYNTHETIC SOFTWARE TEST ONLY', page)
            finally:
                process.terminate()
                process.wait(timeout=5)
                process.stdout.close()

    def test_empty_sources_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / 'report.md'
            questionnaire = Path(directory) / 'questionnaire.md'
            report.write_text('', encoding='utf-8')
            questionnaire.write_text('Questionnaire', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'must not be empty'):
                load_sources(report, questionnaire)

    def test_report_cannot_overwrite_source_or_configuration(self):
        from build_report import REPORT, QUESTIONNAIRE
        for path in (REPORT, QUESTIONNAIRE, REPORT.parent.parent / 'requirements.txt'):
            original = path.read_bytes()
            with self.subTest(path=path), self.assertRaisesRegex(ValueError, '.html'):
                build(path)
            self.assertEqual(path.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
