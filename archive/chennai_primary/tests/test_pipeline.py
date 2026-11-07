"""Synthetic software fixtures only, never participant evidence or final findings."""
import csv
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from research_pipeline import (REQUIRED, ITEMS, checksum, clean_records, read_records,
                               analyse, spearman, ranks, holm, permutation_p, run,
                               dictionary_markdown)

ROOT = Path(__file__).resolve().parents[1]


def fixture(index=0):
    """Construct an explicitly synthetic questionnaire route for unit tests."""
    row = {key: '' for key in REQUIRED}
    row.update(record_id=f'SYNTHETIC-{index}', organisation_code=f'TEST-ORG-{index}',
               unit_code=f'TEST-UNIT-{index}', submitted_at=f'2026-10-05T10:{index:02}:00+05:30',
               phase='main', questionnaire_version='0.3', S03='customer support',
               S07='yes', B06='sufficient', A01='yes', A02='2', A03='2', A04='2')
    for key in ['C01', 'S01', 'S02', 'S03b', 'S04', 'S05', 'S06']:
        row[key] = 'yes'
    for key in ITEMS:
        row[key] = str(index % 5 + 1)
    return row


class PipelineTests(unittest.TestCase):
    def test_submission_template_is_header_only_and_dictionary_is_current(self):
        template = ROOT/'data/templates/responses.csv'
        with template.open(encoding='utf-8-sig', newline='') as handle:
            self.assertEqual(list(csv.reader(handle)), [REQUIRED])
        self.assertEqual((ROOT/'data/templates/DATA_DICTIONARY.md').read_text(encoding='utf-8'),
                         dictionary_markdown())
        with self.assertRaisesRegex(ValueError, 'at least one'):
            read_records(template)

    def test_data_ignore_rules_keep_response_files_private(self):
        public = ['data/README.md', 'data/raw/README.md', 'data/processed/README.md',
                  'data/templates/responses.csv', 'data/templates/DATA_DICTIONARY.md']
        confidential = ['data/raw/export.csv', 'data/raw/nested/export.xlsx',
                        'data/processed/analysis.json', 'data/templates/populated.csv',
                        'data/responses.csv', 'private/responses.csv', 'private/study.json']
        result = subprocess.run(['git', 'check-ignore', '--no-index', '--stdin', '-z'], cwd=ROOT,
                                input=('\0'.join(public + confidential) + '\0').encode('utf-8'),
                                capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(set(result.stdout.decode('utf-8').rstrip('\0').split('\0')), set(confidential))

    def test_malformed_quoted_csv_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'malformed.csv'
            valid_values = [fixture()[field] for field in REQUIRED[:-1]]
            for text in ('"unterminated header',
                         ','.join(REQUIRED) + '\n' + ','.join(valid_values) + ',"1'):
                path.write_text(text, encoding='utf-8')
                with self.subTest(text=text[:30]), self.assertRaisesRegex(ValueError, 'Malformed CSV'):
                    read_records(path)

    @classmethod
    def setUpClass(cls):
        # A fresh checkout has no ignored scratch directory.
        (ROOT / 'work').mkdir(exist_ok=True)

    def test_eligible_and_non_user_routes(self):
        row = fixture()
        row.update(A01='no', A02='0', A03='0', A04='0')
        cleaned, audit = clean_records([row])
        self.assertEqual(cleaned[0]['A02'], 0)
        self.assertEqual(audit[0]['status'], 'included')

    def test_cost_route_and_missing_reasons(self):
        row = fixture()
        row.update(B06='limited', P01='Not known', P02='Not applicable')
        cleaned, _ = clean_records([row])
        self.assertIsNone(cleaned[0]['K01'])
        self.assertEqual(cleaned[0]['missing_reasons']['K01'], 'skipped_by_design')
        self.assertEqual(cleaned[0]['missing_reasons']['P01'], 'not_known')
        self.assertEqual(cleaned[0]['missing_reasons']['P02'], 'not_applicable')

    def test_skipped_routing_answers_preserve_eligible_outcomes(self):
        row = fixture()
        row.update(A01='Prefer not to answer', B06='', A02='invalid skipped code',
                   K01='invalid skipped code')
        cleaned, audit = clean_records([row])
        self.assertEqual(len(cleaned), 1)
        self.assertEqual(cleaned[0]['P01'], 1)
        self.assertIsNone(cleaned[0]['A02'])
        self.assertIsNone(cleaned[0]['K01'])
        self.assertEqual(cleaned[0]['missing_reasons']['A01'], 'declined')
        self.assertEqual(cleaned[0]['missing_reasons']['B06'], 'omitted')
        self.assertEqual(cleaned[0]['missing_reasons']['K01'], 'skipped_by_design')
        self.assertIn('K01_removed_by_cost_route', audit[0]['reasons'])

    def test_unknown_ai_route_precedes_numeric_validation(self):
        row = fixture()
        row.update(S07='unknown ai status', A02='invalid skipped code')
        cleaned, _ = clean_records([row])
        self.assertEqual(len(cleaned), 1)
        self.assertIsNone(cleaned[0]['A02'])

    def test_adoption_contradiction_does_not_become_zero(self):
        row = fixture()
        row.update(A01='no')
        cleaned, _ = clean_records([row])
        self.assertIsNone(cleaned[0]['A02'])
        self.assertEqual(cleaned[0]['missing_reasons']['A02'], 'contradictory_adoption')

    def test_unknown_ai_and_changed_integration(self):
        unknown, changed = fixture(), fixture(1)
        unknown['S07'] = 'unknown ai status'
        changed['A04'] = 'changed'
        cleaned, _ = clean_records([unknown, changed])
        self.assertIsNone(cleaned[0]['A02'])
        self.assertIsNone(cleaned[1]['A04'])
        self.assertEqual(cleaned[1]['A02'], 2)

    def test_eligibility_phase_and_invalid_values(self):
        denied, pilot, invalid = fixture(), fixture(1), fixture(2)
        denied['C01'] = 'no'
        pilot['phase'] = 'pilot'
        invalid['P01'] = 'NaN'
        cleaned, audit = clean_records([denied, pilot, invalid])
        self.assertFalse(cleaned)
        self.assertEqual(len(audit), 3)

    def test_duplicate_keeps_earliest_eligible_not_export_order(self):
        earlier, later = fixture(), fixture(1)
        later['organisation_code'] = earlier['organisation_code']
        later['unit_code'] = earlier['unit_code']
        cleaned, _ = clean_records([later, earlier])
        self.assertEqual(cleaned[0]['record_id'], 'SYNTHETIC-0')
        self.assertEqual(len(cleaned), 1)

    def test_timestamp_and_duplicate_record_id_errors(self):
        row = fixture()
        row['submitted_at'] = '2026-10-05T10:00:00'
        with self.assertRaisesRegex(ValueError, 'timezone'):
            clean_records([row])
        with self.assertRaisesRegex(ValueError, 'unique'):
            clean_records([fixture(), fixture()])

    def test_metadata_null_objects_and_normalised_duplicates_are_rejected(self):
        for value in (None, '', '  ', 1, [], {}):
            row = fixture()
            row['record_id'] = value
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, 'non-empty text'):
                clean_records([row])
        first, second = fixture(), fixture(1)
        second['record_id'] = '  ' + first['record_id'] + '  '
        with self.assertRaisesRegex(ValueError, 'unique'):
            clean_records([first, second])
        first['organisation_code'] = '  TEST-ORG-0  '
        cleaned, _ = clean_records([first])
        self.assertEqual(cleaned[0]['organisation_code'], 'TEST-ORG-0')

    def test_ties_constant_and_negative_correlations(self):
        self.assertEqual(ranks([1, 1, 3]), [1.5, 1.5, 3])
        self.assertAlmostEqual(spearman([1, 2, 3], [3, 2, 1]), -1)
        self.assertAlmostEqual(spearman([1, 1, 3], [1, 1, 3]), 1)
        self.assertIsNone(spearman([1, 1, 1], [1, 2, 3]))
        self.assertIsNone(spearman([1, 2], [1, 2]))

    def test_exact_permutation_and_holm(self):
        self.assertAlmostEqual(permutation_p([1, 2, 3], [1, 2, 3]), 1/3)
        values = holm([.01, .04, None, .03])
        self.assertEqual(values, [.04, .09, None, .09])

    def test_measurement_gate_and_cluster_gate(self):
        raw = [fixture(i) for i in range(5)]
        for i, row in enumerate(raw):
            row['A02'] = str(i % 4 + 1)
        cleaned, _ = clean_records(raw)
        default = analyse(cleaned, {})
        self.assertIsNone(default['associations']['productivity']['rho'])
        supported = {'supported_domains': ['productivity'], 'measurement_support_note': 'Synthetic test only',
                     'independent_unit_inference': True, 'independence_note': 'Synthetic test only'}
        result = analyse(cleaned, supported)
        self.assertIsNotNone(result['associations']['productivity']['p'])
        cleaned[1]['organisation_code'] = cleaned[0]['organisation_code']
        clustered = analyse(cleaned, supported)
        self.assertIsNone(clustered['associations']['productivity']['p'])

    def test_json_csv_and_schema_errors(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'input.csv'
            with path.open('w', encoding='utf-8', newline='') as handle:
                writer = csv.DictWriter(handle, fieldnames=REQUIRED)
                writer.writeheader()
                writer.writerow(fixture())
            self.assertEqual(len(read_records(path)), 1)
            path.write_text('P01,P01\n1,1\n', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'unique'):
                read_records(path)
            path = Path(directory)/'input.json'
            path.write_text('[]', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'at least one'):
                read_records(path)
            path.write_text('[{}]', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'lacks required'):
                read_records(path)

    def test_end_to_end_synthetic_output_and_checksum(self):
        (ROOT/'work').mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT/'work') as directory:
            folder = Path(directory)
            source, manifest = folder/'synthetic.json', folder/'manifest.json'
            source.write_text(json.dumps([fixture(i) for i in range(4)]), encoding='utf-8')
            config = {'evidence_kind': 'synthetic', 'provenance': 'Unit-test generated, not respondents',
                      'input_sha256': checksum(source)}
            manifest.write_text(json.dumps(config), encoding='utf-8')
            result = run(source, manifest, folder/'analysis')
            self.assertEqual(result['evidence_kind'], 'synthetic')
            self.assertIn('NOT RESEARCH FINDINGS', (folder/'analysis/results.md').read_text())
            self.assertTrue((folder/'analysis/adoption.svg').is_file())
            config['input_sha256'] = 'wrong'
            manifest.write_text(json.dumps(config), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'checksum'):
                run(source, manifest, folder/'other')

    def test_output_privacy_gate(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'work') as directory:
            source, manifest = Path(directory)/'synthetic.json', Path(directory)/'manifest.json'
            source.write_text(json.dumps([fixture()]), encoding='utf-8')
            manifest.write_text(json.dumps({'evidence_kind': 'synthetic', 'provenance': 'Synthetic test',
                                           'input_sha256': checksum(source)}), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'under work'):
                run(source, manifest, ROOT/'outputs/leak')

    def test_cli_failure_returns_nonzero(self):
        result = subprocess.run([sys.executable, str(ROOT/'research_pipeline.py')], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Analysis failed', result.stderr)

    def test_required_measurement_and_inference_rationale(self):
        rows, _ = clean_records([fixture()])
        with self.assertRaisesRegex(ValueError, 'measurement_support_note'):
            analyse(rows, {'supported_domains': ['productivity']})
        with self.assertRaisesRegex(ValueError, 'independence'):
            analyse(rows, {'independent_unit_inference': True})
        with self.assertRaisesRegex(ValueError, 'boolean'):
            analyse(rows, {'independent_unit_inference': 'yes'})

    def test_synthetic_input_cannot_enter_final_report(self):
        from build_report import build
        with tempfile.TemporaryDirectory(dir=ROOT/'work') as directory:
            source, manifest = Path(directory)/'synthetic.json', Path(directory)/'manifest.json'
            source.write_text(json.dumps([fixture()]), encoding='utf-8')
            manifest.write_text(json.dumps({'evidence_kind': 'synthetic', 'provenance': 'Synthetic test',
                                           'input_sha256': checksum(source)}), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'prohibited'):
                build(Path(directory)/'final.html', source, manifest)
            self.assertFalse((Path(directory)/'final.html').exists())

    def test_integrated_synthetic_check_is_isolated_and_labelled(self):
        from build_report import build
        with tempfile.TemporaryDirectory(dir=ROOT/'work') as directory:
            source, manifest = Path(directory)/'synthetic.json', Path(directory)/'manifest.json'
            source.write_text(json.dumps([fixture(i) for i in range(4)]), encoding='utf-8')
            manifest.write_text(json.dumps({'evidence_kind': 'synthetic', 'provenance': 'Synthetic test',
                                           'input_sha256': checksum(source)}), encoding='utf-8')
            output = build(Path(directory)/'synthetic-check.html', source, manifest, synthetic_check=True)
            page = output.read_text(encoding='utf-8')
            self.assertIn('SYNTHETIC SOFTWARE TEST ONLY', page)
            self.assertIn('NOT RESEARCH FINDINGS', page)
            self.assertIn('data:image/svg+xml;base64,', page)
            self.assertIn('Appendix B: Data Dictionary', page)
            self.assertIn('Table 4.1. Outcome-item summaries', page)
            self.assertIn('Figure 4.1. Reported AI-use frequency', page)
            self.assertNotIn('No genuine respondent data are available in this edition', page)
            self.assertNotIn('No participant dataset is present', page)
            self.assertNotIn('genuine data, real-data analysis, and final empirical conclusions remain pending', page)
            self.assertNotIn('5.4 Evidence-based discussion procedure — pending data', page)
            self.assertIn('5.4 Evidence-based discussion procedure — pending interpretation', page)
            with self.assertRaisesRegex(ValueError, 'synthetic checks require work'):
                build(ROOT/'outputs/not-research.html', source, manifest, synthetic_check=True)

    def test_monte_carlo_is_reproducible(self):
        x, y = list(range(8)), [1, 1, 2, 2, 3, 3, 4, 4]
        self.assertEqual(permutation_p(x, y, draws=49), permutation_p(x, y, draws=49))

    def test_short_row_and_nonfinite_response(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory)/'input.csv'
            source.write_text('a,b\n1\n', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'same number'):
                read_records(source)
        row = fixture()
        row['D01'] = 'Infinity'
        cleaned, audit = clean_records([row])
        self.assertFalse(cleaned)
        self.assertIn('invalid_D01', audit[0]['reasons'])

    def test_cli_template_and_complete_synthetic_workflow(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'work') as directory:
            folder = Path(directory)
            template = folder/'empty.csv'
            command = [sys.executable, str(ROOT/'research_pipeline.py')]
            created = subprocess.run(command + ['--template', str(template)], capture_output=True, text=True)
            self.assertEqual(created.returncode, 0, created.stderr)
            self.assertEqual(len(template.read_text().splitlines()), 1)
            overwritten = subprocess.run(command + ['--template', str(template)], capture_output=True, text=True)
            self.assertNotEqual(overwritten.returncode, 0)
            source, manifest = folder/'synthetic.json', folder/'manifest.json'
            source.write_text(json.dumps([fixture(i) for i in range(3)]), encoding='utf-8')
            manifest.write_text(json.dumps({'evidence_kind': 'synthetic', 'provenance': 'CLI synthetic test only',
                                           'input_sha256': checksum(source)}), encoding='utf-8')
            analysed = subprocess.run(command + ['--input', str(source), '--manifest', str(manifest),
                                                  '--out', str(folder/'analysis')], capture_output=True, text=True)
            self.assertEqual(analysed.returncode, 0, analysed.stderr)
            generated = subprocess.run([sys.executable, str(ROOT/'build_report.py'), '--synthetic-check',
                                       '--input', str(source), '--manifest', str(manifest),
                                       '--output', str(folder/'synthetic.html')], capture_output=True, text=True)
            self.assertEqual(generated.returncode, 0, generated.stderr)
            self.assertIn('SYNTHETIC SOFTWARE TEST ONLY', (folder/'synthetic.html').read_text(encoding='utf-8'))
