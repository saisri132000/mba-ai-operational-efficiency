"""Critical checks for the canonical OECD project; no invented respondents."""
import csv
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest
import zipfile
from types import SimpleNamespace

from build_report import release
from research_pipeline import verify_sources

ROOT=Path(__file__).resolve().parent.parent

class HTMLCheck(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=[]; self.anchors=[]; self.images=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if 'id' in attrs:self.ids.append(attrs['id'])
        if tag=='a' and attrs.get('href','').startswith('#'):self.anchors.append(attrs['href'][1:])
        if tag=='img':self.images.append(attrs['src'])

class SecondaryProjectTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory()
        cls.root=Path(cls.temp.name)
        for folder in ('sources','scripts'):
            shutil.copytree(ROOT/folder,cls.root/folder,ignore=shutil.ignore_patterns('__pycache__'))
        for name in ('research_pipeline.py','build_report.py','README.md','requirements.txt',
                     'Databricks_OECD_Analysis.py','DATABRICKS_SETUP.md','FINAL_SUBMISSION_STATUS.md',
                     'SUBMISSION_BLOCKERS.md','SUBMISSION_HANDOFF.md'):
            shutil.copy2(ROOT/name,cls.root/name)
        cls.readme=(cls.root/'README.md').read_bytes()
        cls.archive=release(cls.root)
    @classmethod
    def tearDownClass(cls):cls.temp.cleanup()

    def test_approved_sources_match(self):
        self.assertEqual(len(verify_sources(self.root)),2)

    def test_modified_source_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);shutil.copytree(self.root/'sources',root/'sources')
            with (root/'sources/OECD_published_tables.xlsx').open('ab') as stream:stream.write(b'changed')
            with self.assertRaisesRegex(ValueError,'checksum mismatch'):verify_sources(root)

    def test_unexpected_manifest_entry_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'sources').mkdir()
            (root/'sources/source_manifest.json').write_text(json.dumps({'../outside':'fake'}))
            with self.assertRaisesRegex(ValueError,'exactly'):verify_sources(root)

    def test_all_values_trace_to_original_cells(self):
        import openpyxl
        workbook=openpyxl.load_workbook(self.root/'sources/OECD_published_tables.xlsx',data_only=True)
        with (self.root/'results/observations.csv').open(encoding='utf-8') as stream:rows=list(csv.DictReader(stream))
        self.assertEqual(len(rows),152)
        for row in rows:
            value=workbook[row['source_sheet']][row['source_cell']].value
            self.assertAlmostEqual(value,float(row['raw_proportion']))
            self.assertAlmostEqual(value*100,float(row['percentage']),places=4)
        workbook.close()

    def test_quality_issue_disclosed_without_normalization(self):
        quality=json.loads((self.root/'results/data_quality.json').read_text())
        failed=[row for row in quality['checks'] if row['status'].startswith('EXCLUDED')]
        self.assertEqual(len(quality['checks']),36)
        self.assertEqual(len(failed),1)
        self.assertAlmostEqual(failed[0]['total'],.94)
        self.assertIn('Staff-cost',failed[0]['metric'])

    def test_comparisons_and_rounding(self):
        with (self.root/'results/sector_comparisons.csv').open(encoding='utf-8') as stream:rows=list(csv.DictReader(stream))
        self.assertEqual(len(rows),16)
        for row in rows:
            self.assertAlmostEqual(float(row['manufacturing_percent'])-float(row['finance_percent']),float(row['manufacturing_minus_finance_pp']),places=2)
        self.assertEqual(rows[1]['finance_percent'],'56.7')
        self.assertEqual(rows[2]['finance_percent'],'79.3')
        self.assertFalse(any('Staff-cost' in r['metric'] for r in rows))

    def test_html_navigation_and_charts(self):
        page=(self.root/'report/PROJECT_REPORT.html').read_text(encoding='utf-8')
        check=HTMLCheck();check.feed(page)
        self.assertEqual(len(check.ids),len(set(check.ids)))
        self.assertTrue(all(a in check.ids for a in check.anchors))
        self.assertEqual(len(check.images),4)
        self.assertTrue(all((self.root/'report'/p).is_file() for p in check.images))

    def test_report_pdf_and_scope(self):
        from pypdf import PdfReader
        pages=PdfReader(self.root/'report/PROJECT_REPORT.pdf').pages
        self.assertGreaterEqual(len(pages),8)
        text=' '.join(p.extract_text() for p in pages)
        for phrase in ('Chapter 1','Chapter 5','79.30','Databricks','References','not establish'):
            self.assertIn(phrase,text)

    def test_build_does_not_overwrite_readme(self):
        self.assertEqual((self.root/'README.md').read_bytes(),self.readme)

    def test_explainer_includes_actual_results_and_speech(self):
        page=(self.root/'outputs/Project_Complete_Explainer.html').read_text(encoding='utf-8')
        self.assertEqual(page.count('id="read-aloud"'),1)
        self.assertIn('speechSynthesis',page)
        self.assertIn('Databricks_OECD_Analysis.py',page)
        check=HTMLCheck();check.feed(page)
        self.assertTrue(all(a in check.ids for a in check.anchors))

    def test_zip_contains_current_sources_not_legacy(self):
        with zipfile.ZipFile(self.archive) as archive:
            self.assertIsNone(archive.testzip())
            for name in ('Databricks_OECD_Analysis.py','research_pipeline.py','README.md','requirements.txt',
                         'outputs/Project_Complete_Explainer.html','outputs/AI_Comparison_Dashboard.html',
                         'sources/OECD_published_tables.xlsx'):
                self.assertEqual(archive.read(name),(self.root/name).read_bytes())
            self.assertFalse(any(name.startswith(('archive/','private/','work/')) for name in archive.namelist()))

    def test_dashboard_populations_calculations_and_links(self):
        from scripts.build_dashboard import dashboard_data
        data=dashboard_data(self.root)
        self.assertEqual(len(data),20)
        productivity=next(row for row in data if row['metric']=='Employer perceived productivity: positive')
        self.assertEqual(productivity['population'],'AI-adopting employers')
        self.assertEqual(productivity['finance'],56.7)
        self.assertEqual({row['unweighted_source_subgroup_n'] for row in productivity['evidence']},{291,452})
        sizes=[row for row in data if row['topic']=='Adoption by firm size']
        self.assertEqual(len(sizes),4)
        self.assertTrue(all(row['population']=='Employers in this firm-size band' for row in sizes))
        self.assertFalse(any(row['metric']=='Staff-cost motivation' for row in data))
        page=(self.root/'outputs/AI_Comparison_Dashboard.html').read_text(encoding='utf-8')
        check=HTMLCheck();check.feed(page)
        self.assertEqual(len(check.ids),len(set(check.ids)))
        self.assertIn('Source subgroup n',page)
        self.assertIn('94%',page)

    def test_dashboard_rejects_changed_summary(self):
        from scripts.build_dashboard import dashboard_data
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            shutil.copytree(self.root/'results',root/'results')
            path=root/'results/sector_comparisons.csv'
            path.write_text(path.read_text().replace('56.7,62.6','50.0,62.6'))
            with self.assertRaisesRegex(ValueError,'disagrees'):dashboard_data(root)

    def test_notebook_uses_shared_pipeline(self):
        source=(self.root/'Databricks_OECD_Analysis.py').read_text()
        compile(source,'Databricks_OECD_Analysis.py','exec')
        self.assertTrue(source.startswith('# Databricks notebook source'))
        self.assertIn('%pip install -r ./requirements.txt',source)
        self.assertIn('release(project_root)',source)
        self.assertNotIn('DATABRICKS_TOKEN',source)

    def test_notebook_python_workflow_locally(self):
        # Execute real notebook Python with UI-only helpers stubbed. This is not
        # a claim of cloud/compute/package-installation verification.
        notebook=(self.root/'Databricks_OECD_Analysis.py').read_text()
        values={}; rendered=[]
        widgets=SimpleNamespace(text=lambda key,value,label:values.setdefault(key,value),get=lambda key:values[key])
        dbutils=SimpleNamespace(widgets=widgets,library=SimpleNamespace(restartPython=lambda:None))
        old=Path.cwd()
        try:
            os.chdir(self.root)
            exec(compile(notebook,'Databricks_OECD_Analysis.py','exec'),{'dbutils':dbutils,'displayHTML':rendered.append})
        finally:os.chdir(old)
        self.assertEqual(len(rendered),2)
        self.assertIn('<svg',rendered[0])
        self.assertIn('56.7',rendered[1])

if __name__=='__main__':unittest.main()
