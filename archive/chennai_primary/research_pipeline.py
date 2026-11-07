"""Import coded questionnaire records and produce auditable, private analysis output.

No participant data are bundled. Real/synthetic provenance is declared by the
researcher, never inferred from values. Default analysis is descriptive only.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
import itertools
import json
import math
from pathlib import Path
import random
import statistics as st
import sys
from datetime import datetime
from html import escape

DOMAINS = {'productivity': ['P01', 'P02', 'P03'],
           'process': ['E01', 'E02', 'E03'], 'cost': ['K01', 'K02', 'K03'],
           'decision': ['D01', 'D02', 'D03']}
ITEMS = [item for items in DOMAINS.values() for item in items]
SCREEN = ['C01', 'S01', 'S02', 'S03b', 'S04', 'S05', 'S06']
META = ['record_id', 'organisation_code', 'unit_code', 'submitted_at', 'phase', 'questionnaire_version']
REQUIRED = META + SCREEN + ['S03', 'S07', 'B06', 'A01', 'A02', 'A03', 'A04'] + ITEMS
MISSING = {'': 'omitted', 'not known': 'not_known', 'unknown': 'not_known',
           'not applicable': 'not_applicable', 'na': 'not_applicable',
           'prefer not to answer': 'declined'}
ACTIVITIES = {'customer support', 'transaction processing', 'back-office service delivery'}
ENUMS = {**{field: {'yes', 'no'} for field in SCREEN},
         **{field: {'yes', 'no', 'unsure'} for field in ('S02', 'S03b', 'S06')},
         'S03': ACTIVITIES | {'other'},
         'S07': {'yes', 'unknown ai status', 'no'},
         'B06': {'none', 'limited', 'sufficient'}, 'A01': {'yes', 'no', 'not known'},
         'phase': {'main', 'pilot', 'test'}}
RANGES = {'A02': (0, 4), 'A03': (0, 4), 'A04': (0, 3), **{item: (1, 5) for item in ITEMS}}
LABELS = {'A02': ['Never', 'Less than monthly', 'Monthly', 'Weekly', 'Daily/almost daily']}


def checksum(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_records(path):
    path = Path(path)
    if path.suffix.lower() == '.csv':
        with path.open(encoding='utf-8-sig', newline='') as handle:
            reader = csv.DictReader(handle, strict=True)
            try:
                if not reader.fieldnames or len(set(reader.fieldnames)) != len(reader.fieldnames):
                    raise ValueError('CSV needs unique column headings.')
                rows = list(reader)
            except csv.Error as exc:
                raise ValueError('Malformed CSV; use a correctly escaped UTF-8 export.') from exc
            if any(None in row or any(v is None for v in row.values()) for row in rows):
                raise ValueError('CSV rows must have the same number of fields as the header.')
    elif path.suffix.lower() == '.json':
        rows = json.loads(path.read_text(encoding='utf-8-sig'))
    else:
        raise ValueError('Use a UTF-8 coded CSV or JSON array; export Excel as CSV first.')
    if not isinstance(rows, list) or not rows:
        raise ValueError('Input must contain at least one record; no empty dataset results are generated.')
    for index, row in enumerate(rows, 1):
        if not isinstance(row, dict) or set(REQUIRED) - row.keys():
            raise ValueError(f'Record {index} lacks required questionnaire/metadata fields.')
    return rows


def numeric(value, field):
    text = str(value if value is not None else '').strip().lower()
    if text in MISSING:
        return None, MISSING[text]
    if field == 'A04' and text == 'changed':
        return None, 'changed'
    try:
        number = float(text)
    except ValueError as exc:
        raise ValueError(f'{field}: use an integer code or documented missing value.') from exc
    low, high = RANGES[field]
    if not math.isfinite(number) or not number.is_integer() or not low <= number <= high:
        raise ValueError(f'{field}: code outside allowed range {low}–{high}.')
    return int(number), None


def clean_records(raw):
    """Return coded eligible records plus a row-number audit, without identifiers."""
    accepted, audit, seen, ids = [], [], set(), set()
    ordered = []
    for number, row in enumerate(raw, 1):
        try:
            if any(not isinstance(row[k], str) or not row[k].strip() for k in META):
                raise ValueError('Metadata must contain non-empty text identifiers, timestamps and version codes.')
            row = dict(row)
            for key in META:
                row[key] = row[key].strip()
            stamp = datetime.fromisoformat(row['submitted_at'].replace('Z', '+00:00'))
            if stamp.tzinfo is None:
                raise ValueError('submitted_at requires a timezone.')
            if row['record_id'] in ids:
                raise ValueError('record_id must be unique.')
            ids.add(row['record_id'])
            ordered.append((stamp, number, row))
        except (ValueError, TypeError) as exc:
            raise ValueError(f'Record {number}: invalid metadata ({exc})') from exc
    for _, number, raw_row in sorted(ordered, key=lambda entry: (entry[0], entry[1])):
        row = {key: str(value if value is not None else '').strip() for key, value in raw_row.items()}
        events, errors, reasons = [], [], {}
        for field, choices in ENUMS.items():
            row[field] = row[field].lower()
            if field in ('A01', 'B06') and row[field] in MISSING:
                reasons[field] = MISSING[row[field]]
                row[field] = None
                continue
            if row[field] not in choices:
                errors.append(f'invalid_{field}')
        if row['questionnaire_version'] != '0.3':
            errors.append('questionnaire_version_not_0.3')
        for field in RANGES:
            if field in ('A02', 'A03', 'A04') and (row['S07'] == 'unknown ai status' or row['A01'] in (None, 'not known')):
                if str(row[field]).strip():
                    events.append(f'{field}_removed_by_unknown_adoption_route')
                row[field], reasons[field] = None, 'adoption_unknown'
                continue
            if field in DOMAINS['cost'] and row['B06'] != 'sufficient':
                if str(row[field]).strip():
                    events.append(f'{field}_removed_by_cost_route')
                row[field], reasons[field] = None, 'skipped_by_design'
                continue
            try:
                row[field], reasons[field] = numeric(row[field], field)
            except ValueError:
                errors.append(f'invalid_{field}')
        if errors:
            audit.append({'input_row': number, 'status': 'excluded', 'reasons': errors})
            continue
        if row['phase'] != 'main' or any(row[f] != 'yes' for f in SCREEN) or row['S03'] not in ACTIVITIES or row['S07'] == 'no':
            audit.append({'input_row': number, 'status': 'excluded', 'reasons': ['non_main_or_eligibility_not_confirmed']})
            continue
        key = (row['organisation_code'], row['unit_code'])
        if key in seen:
            audit.append({'input_row': number, 'status': 'excluded', 'reasons': ['duplicate_unit_later_submission']})
            continue
        if row['S07'] == 'unknown ai status' or row['A01'] in (None, 'not known'):
            for field in ('A02', 'A03', 'A04'):
                row[field], reasons[field] = None, 'adoption_unknown'
            events.append('unknown_adoption_not_scored')
        elif row['A01'] == 'no':
            # No silent zero filling: export must contain explicit confirmed non-use codes.
            if any(row[field] != 0 for field in ('A02', 'A03', 'A04')):
                for field in ('A02', 'A03', 'A04'):
                    row[field], reasons[field] = None, 'contradictory_adoption'
                events.append('non_use_codes_not_confirmed')
        elif row['A02'] == 0 or row['A03'] == 0 or row['A04'] == 0:
            for field in ('A02', 'A03', 'A04'):
                row[field], reasons[field] = None, 'contradictory_adoption'
            events.append('use_conflicts_with_zero_codes')
        if row['B06'] != 'sufficient':
            for field in DOMAINS['cost']:
                if row[field] is not None:
                    events.append(f'{field}_removed_by_cost_route')
                row[field], reasons[field] = None, 'skipped_by_design'
        row['missing_reasons'] = reasons
        accepted.append(row)
        seen.add(key)
        audit.append({'input_row': number, 'status': 'included', 'reasons': events})
    return accepted, audit


def ranks(values):
    order = sorted(range(len(values)), key=values.__getitem__)
    output = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i + 1
        while j < len(order) and values[order[j]] == values[order[i]]:
            j += 1
        for index in order[i:j]:
            output[index] = (i + 1 + j) / 2
        i = j
    return output


def spearman(x, y):
    if len(x) != len(y):
        raise ValueError('Paired arrays must have equal lengths.')
    if len(x) < 3 or len(set(x)) < 2 or len(set(y)) < 2:
        return None
    a, b = ranks(x), ranks(y)
    ma, mb = st.mean(a), st.mean(b)
    denominator = math.sqrt(sum((v-ma)**2 for v in a) * sum((v-mb)**2 for v in b))
    return sum((v-ma)*(w-mb) for v, w in zip(a, b)) / denominator


def permutation_p(x, y, seed=20261005, draws=1999):
    observed = spearman(x, y)
    if observed is None:
        return None
    if len(x) <= 7:
        values = itertools.permutations(y)
        extreme = sum(abs(spearman(x, list(v))) >= abs(observed)-1e-12 for v in values)
        return extreme / math.factorial(len(y))
    rng, extreme = random.Random(seed), 0
    for _ in range(draws):
        sample = list(y)
        rng.shuffle(sample)
        extreme += abs(spearman(x, sample)) >= abs(observed)-1e-12
    return (extreme + 1) / (draws + 1)


def holm(values):
    order = sorted(range(len(values)), key=lambda i: 1 if values[i] is None else values[i])
    result, running = [None] * len(values), 0.0
    for rank, index in enumerate(order):
        p = 1 if values[index] is None else values[index]
        running = max(running, min(1, (len(values)-rank)*p))
        if values[index] is not None:
            result[index] = running
    return result


def domain_score(row, name):
    values = [row[item] for item in DOMAINS[name]]
    return st.mean(values) if all(v is not None for v in values) else None


def alpha(matrix):
    if len(matrix) < 3:
        return None
    variance = st.variance([sum(row) for row in matrix])
    if variance == 0:
        return None
    return 1.5 * (1 - sum(st.variance(column) for column in zip(*matrix)) / variance)


def analyse(rows, manifest):
    supported = manifest.get('supported_domains', [])
    if not isinstance(supported, list) or set(supported) - DOMAINS.keys():
        raise ValueError('supported_domains must list recognised domain names.')
    note = manifest.get('measurement_support_note', '')
    if supported and (not isinstance(note, str) or not note.strip()):
        raise ValueError('Domain scoring requires a measurement_support_note from the researcher.')
    infer = manifest.get('independent_unit_inference', False)
    if not isinstance(infer, bool):
        raise ValueError('independent_unit_inference must be a boolean.')
    independence_note = manifest.get('independence_note', '')
    if infer and (not isinstance(independence_note, str) or not independence_note.strip()):
        raise ValueError('Inference requires an explicit independence/exchangeability rationale.')
    orgs = Counter(row['organisation_code'] for row in rows)
    independent = bool(rows) and all(count == 1 for count in orgs.values())
    items = {}
    for item in ITEMS:
        values = [row[item] for row in rows if row[item] is not None]
        items[item] = {'n': len(values), 'missing': len(rows)-len(values),
                       'median': st.median(values) if values else None,
                       'distribution': {str(i): values.count(i) for i in range(1, 6)},
                       'missing_reasons': dict(Counter(row['missing_reasons'][item] for row in rows if row[item] is None))}
    associations = {}
    for name in DOMAINS:
        pairs = [(row['A02'], domain_score(row, name)) for row in rows]
        pairs = [(x, y) for x, y in pairs if x is not None and y is not None]
        matrix = [[row[item] for item in DOMAINS[name]] for row in rows if all(row[item] is not None for item in DOMAINS[name])]
        x, y = [v[0] for v in pairs], [v[1] for v in pairs]
        enabled = name in supported
        rho = spearman(x, y) if enabled else None
        p = permutation_p(x, y) if enabled and infer and independent else None
        associations[name] = {'n': len(pairs) if enabled else None, 'rho': rho, 'p': p,
            'alpha_diagnostic': alpha(matrix), 'measurement_supported_by_researcher': enabled,
            'status': 'not_scored_no_measurement_support' if not enabled else
                      'not_estimable' if rho is None else 'independent_permutation' if p is not None else 'descriptive_only'}
    adjusted = holm([entry['p'] for entry in associations.values()])
    for entry, value in zip(associations.values(), adjusted):
        entry['holm_p'] = value
    return {'retained_units': len(rows), 'organisations': len(orgs),
        'largest_organisation_units': max(orgs.values(), default=0),
        'organisation_dependence_present': not independent if rows else None,
        'inference_requested': infer, 'inference_permitted': infer and independent,
        'adoption_frequency': {str(i): sum(row['A02'] == i for row in rows) for i in range(5)},
        'adoption_unknown': sum(row['A02'] is None for row in rows),
        'items': items, 'associations': associations}


def fmt(value):
    return 'Not estimated' if value is None else f'{value:.4g}' if isinstance(value, float) else str(value)


def results_markdown(result):
    synthetic = result['evidence_kind'] == 'synthetic'
    label = 'SYNTHETIC SOFTWARE TEST — NOT RESEARCH FINDINGS' if synthetic else 'Researcher-declared genuine input — authenticity not independently verified'
    a = result['analysis']
    text = f'## Imported evidence and analysis\n\n**{label}**\n\n'
    text += f"Imported records: {result['imported_records']}; retained eligible main-phase units: {a['retained_units']}; organisations: {a['organisations']}. These counts come only from the supplied file.\n\n"
    text += f"Adoption frequency unclassified/missing: {a['adoption_unknown']}. Largest contributing organisation: {a['largest_organisation_units']} retained units. Organisation dependence flagged: {a['organisation_dependence_present']}. Inference requested: {a['inference_requested']}; organisation structure permits it: {a['inference_permitted']}. These flags do not establish statistical assumptions.\n\n"
    text += '### 4.1 Item descriptions\n\n**Table 4.1. Outcome-item summaries from supplied records**\n\n| Item | Valid N | Missing | Median |\n|---|---|---|---|\n'
    for item, summary in a['items'].items():
        text += f"| {item} | {summary['n']} | {summary['missing']} | {fmt(summary['median'])} |\n"
    text += '\n### 4.2 Supported-domain associations\n\n**Table 4.2. Conditional adoption–outcome associations**\n\n| Domain | N | Spearman rho | Raw p | Holm p | Status |\n|---|---|---|---|---|---|\n'
    for name, summary in a['associations'].items():
        text += f"| {name} | {fmt(summary['n'])} | {fmt(summary['rho'])} | {fmt(summary['p'])} | {fmt(summary['holm_p'])} | {summary['status']} |\n"
    text += '\nTables 4.1 and 4.2 use analysis-specific counts. Full item distributions, missing reasons, and alpha diagnostics are retained in the private analysis file. Scores are withheld unless the researcher supplies measurement support. Internal consistency is diagnostic, not validation. Exact permutation tests use all permutations at N ≤ 7; larger samples use 1,999 seeded shuffles with a plus-one correction. Holm adjustment retains the original family of four. Tests require independent, exchangeable observations under the independence null and a researcher rationale; more than one unit per organisation disables inferential p-values. They are not a general test of zero rank correlation under dependence. No confidence intervals are implemented; none is fabricated. No causal or population-representative conclusion is generated. Researcher disclosure review is required before sharing aggregates.\n'
    return text


def chart(result):
    counts = result['analysis']['adoption_frequency']
    maximum = max(counts.values(), default=0) or 1
    label = 'SYNTHETIC TEST ONLY' if result['evidence_kind'] == 'synthetic' else 'Supplied sample: reported AI-use frequency'
    elements = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 260" role="img"><title>{escape(label)}</title><rect width="640" height="260" fill="white"/><text x="15" y="25" font-size="16">{escape(label)}</text>']
    for i in range(5):
        y, count = 45+i*38, counts[str(i)]
        elements.append(f'<text x="15" y="{y+17}" font-size="12">{escape(LABELS["A02"][i])}</text><rect x="165" y="{y}" width="{400*count/maximum}" height="22" fill="#125e69"/><text x="{175+400*count/maximum}" y="{y+17}" font-size="12">{count}</text>')
    elements.append('</svg>')
    return ''.join(elements)


def dictionary_markdown():
    text = '# Appendix B: Data Dictionary and Analysis Rules\n\n'
    text += 'Use coded UTF-8 CSV or a JSON array with one row per submitted unit report. Required columns may contain documented missing tokens for analytical items, A01, and B06, but eligibility must be affirmatively established. Table B.1 gives the authoritative importer schema; no response rows are supplied.\n\n**Table B.1. Required import fields and codes**\n\n| Field | Allowed values / meaning |\n|---|---|\n'
    for field in REQUIRED:
        if field in ENUMS:
            meaning = ', '.join(sorted(ENUMS[field]))
            if field in ('A01', 'B06'):
                meaning += '; documented missing tokens allowed'
        elif field in RANGES:
            low, high = RANGES[field]
            meaning = f'Integer {low}–{high}; missing tokens allowed' + ('; changed also allowed' if field == 'A04' else '')
        elif field == 'submitted_at':
            meaning = 'ISO 8601 timestamp with timezone; earliest eligible submission retained'
        elif field == 'questionnaire_version':
            meaning = 'Text 0.3; other versions need a reviewed mapping'
        elif field == 'organisation_code':
            meaning = 'Non-empty text code; use consistently for the same organisation'
        elif field == 'unit_code':
            meaning = 'Non-empty text code identifying the unit within its organisation; pair used for deduplication'
        else:
            meaning = 'Non-empty text code; no names/emails; record_id unique after whitespace trimming'
        text += f'| {field} | {meaning} |\n'
    text += '\nMissing tokens: empty, Not known/unknown, Not applicable/NA, Prefer not to answer. They remain distinct missing reasons, never zero or the midpoint. A02 codes: 0 Never; 1 Less than monthly; 2 Monthly but less than weekly; 3 Weekly but less than daily; 4 Daily/almost daily. A03: 0 None; 1 >0–<25%; 2 25–<50%; 3 50–<75%; 4 75–100%. A04: 0 No use; 1 Isolated use; 2 Selected workflows; 3 Embedded workflows; changed non-scored. B06: none/limited/sufficient correspond to cost knowledge. S07 unknown ai status corresponds to the questionnaire\'s longer unknown-status option. Outcome codes 1–5 follow the questionnaire agreement scale.\n\n'
    text += 'A01 uses text yes/no/not known, not numeric 1/0; B06 uses none/limited/sufficient. Omitted or declined A01 leaves adoption unclassified; omitted or declined B06 masks cost answers and retains its missing reason. Eligibility uncertainty requires documented resolution in a reviewed coding copy before import. Optional additional export columns are retained privately, not included in aggregate reports. B04/B05 map to organisation_code/unit_code; the remaining contextual questions and free text are not analysed automatically. Export platforms must map their own headings/labels explicitly to these codes; the importer never guesses labels. Excel exports must be saved as UTF-8 CSV. Complete three-item means are scored only for researcher-supported domains. Alpha is an exploratory diagnostic and cannot establish construct validity. No grand efficiency score is produced. No cluster inference, regression, mediation, ROI, or automatic empirical conclusion is implemented.\n'
    return text


def run(input_path, manifest_path, out):
    input_path, manifest_path, out = Path(input_path), Path(manifest_path), Path(out)
    manifest = json.loads(manifest_path.read_text(encoding='utf-8-sig'))
    if not isinstance(manifest, dict) or manifest.get('evidence_kind') not in {'real', 'synthetic'}:
        raise ValueError('Manifest requires evidence_kind real or synthetic; neither is inferred.')
    if not isinstance(manifest.get('provenance'), str) or not manifest['provenance'].strip():
        raise ValueError('Manifest requires a provenance account supplied by the researcher.')
    if manifest.get('input_sha256') != checksum(input_path):
        raise ValueError('Input checksum does not match manifest; confirm provenance for this exact file.')
    if out.resolve() in (input_path.resolve(), manifest_path.resolve()):
        raise ValueError('Output directory cannot overwrite input files.')
    for name in ('analysis.json', 'cleaned.json', 'audit.json', 'results.md', 'adoption.svg'):
        if (out/name).resolve() in (input_path.resolve(), manifest_path.resolve()):
            raise ValueError('Generated files must not overwrite input or provenance files.')
    # Protect potentially sensitive raw and aggregate data by requiring ignored private storage.
    root = Path(__file__).resolve().parent
    private = root / ('work' if manifest['evidence_kind'] == 'synthetic' else 'private')
    if not out.resolve().is_relative_to(private.resolve()):
        raise ValueError('Write real analysis under private/ and synthetic test analysis under work/.')
    if manifest['evidence_kind'] == 'real' and not input_path.resolve().is_relative_to((root/'private').resolve()):
        raise ValueError('Genuine response files must be placed under private/; test files cannot be promoted by accident.')
    raw = read_records(input_path)
    rows, audit = clean_records(raw)
    result = {'schema_version': 1, 'evidence_kind': manifest['evidence_kind'],
              'input_sha256': checksum(input_path), 'manifest_sha256': checksum(manifest_path),
              'imported_records': len(raw), 'analysis': analyse(rows, manifest)}
    out.mkdir(parents=True, exist_ok=True)
    (out/'analysis.json').write_text(json.dumps(result, indent=2, allow_nan=False), encoding='utf-8')
    (out/'cleaned.json').write_text(json.dumps(rows, indent=2, allow_nan=False), encoding='utf-8')
    (out/'audit.json').write_text(json.dumps(audit, indent=2), encoding='utf-8')
    (out/'results.md').write_text(results_markdown(result), encoding='utf-8')
    (out/'adoption.svg').write_text(chart(result), encoding='utf-8')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path)
    parser.add_argument('--manifest', type=Path)
    parser.add_argument('--out', type=Path)
    parser.add_argument('--template', type=Path, help='Write an empty CSV header, never response rows.')
    args = parser.parse_args()
    try:
        if args.template:
            if args.template.exists():
                raise ValueError('Template destination already exists; no file overwritten.')
            args.template.parent.mkdir(parents=True, exist_ok=True)
            with args.template.open('w', encoding='utf-8', newline='') as handle:
                csv.writer(handle).writerow(REQUIRED)
            print('Empty coded-response template created; no respondents or responses generated.')
            return 0
        if not all((args.input, args.manifest, args.out)):
            raise ValueError('Supply --input, --manifest and --out, or use --template.')
        result = run(args.input, args.manifest, args.out)
    except (ValueError, OSError, TypeError, csv.Error) as exc:
        print(f'Analysis failed: {exc}', file=sys.stderr)
        return 1
    print(f"Analysis written ({result['evidence_kind']}); no empirical conclusion is inferred.")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
