# Genuine-response submission inputs

This directory ships instructions and a **header-only response template**, never participant records. The template is generated from the existing importer's required columns. [DATA_DICTIONARY.md](templates/DATA_DICTIONARY.md) lists every field, allowed code, and missing-value rule. [responses.csv](templates/responses.csv) contains one header line and no response rows; an empty template is intentionally rejected as an analysis dataset.

```text
data/
  README.md
  raw/README.md                    Original-export storage instructions
  processed/README.md              Analysis-output storage instructions
  templates/responses.csv          Empty UTF-8 CSV header
  templates/DATA_DICTIONARY.md      Import schema from the implemented pipeline
private/                          Local only, ignored by Git
  responses.csv                   Reviewed genuine coded input, when available
  study.json                      Actual provenance/checksum and analysis decisions
  analysis/                       Generated private audit/statistics/chart
  MBA_Project_Report.html         Generated supplied-data research report
```

## Add real data

1. Preserve an actual export unchanged under `data/raw/` or `private/raw/`. All raw files except this directory's README are ignored. Keep contact linkages separate with restricted access.
2. Copy the empty template to **new** `private/responses.csv` (do not overwrite an existing dataset), or use `python research_pipeline.py --template private/responses.csv`, which refuses to overwrite. Add only genuine coded rows. The importer requires genuine coded input under `private/`; the public template is not an empirical dataset.
3. Map the actual export explicitly to the schema. CSV is UTF-8 (a BOM is accepted), comma-delimited, with unique exact headings and correctly quoted fields. Every row has the same field count. Excel must be saved as UTF-8 CSV. JSON is a non-empty array of records with the same required keys; metadata values must be text.
4. Complete actual consent/eligibility review, collection protocol, and instrument/measurement decisions. Keep pilot/test records separate. Document every correction in a reviewed coding copy without changing the original export.
5. Obtain the actual digest:

   ```sh
   python -c "from research_pipeline import checksum; print(checksum('private/responses.csv'))"
   ```

6. Create `private/study.json` with truthful `evidence_kind: "real"`, `provenance`, and `input_sha256` from that file. Start with `supported_domains: []` and `independent_unit_inference: false`. Domain scoring needs actual measurement support and `measurement_support_note`; inference needs a defensible independence/exchangeability assessment and `independence_note`. No example provenance, digest, or study approval is supplied.

## Validation and duplicate rules

Missing analytical answers are empty, Not known/unknown, Not applicable/NA, or Prefer not to answer. They retain separate reasons and never become zero or the midpoint. A04 also permits the non-scored `changed` category. A01 uses text yes/no/not known; B06 uses none/limited/sufficient. Missing A01 leaves adoption unclassified; missing/insufficient B06 masks cost items. Routes are applied before numeric checks for skipped fields. Consent and eligibility must be affirmative; uncertain/other eligibility requires documented resolution before import.

Required metadata are non-empty text codes, a timezone-aware ISO 8601 `submitted_at`, phase, and version `0.3`. Record IDs must be globally unique after whitespace trimming. For the same organisation/unit pair, the earliest eligible valid-coded record is retained; timestamp ties use original row order. Invalid applicable answer codes exclude a row with an audit reason. Malformed files, missing headers, or invalid metadata stop import for correction. Invalid answers are never silently corrected from guesses.

## Regenerate analysis and report

After setup in the root README, run from the repository root:

```sh
python research_pipeline.py --input private/responses.csv --manifest private/study.json --out private/analysis
python build_report.py --input private/responses.csv --manifest private/study.json --output private/MBA_Project_Report.html
```

The pipeline preserves inputs and writes private `cleaned.json`, `audit.json`, `analysis.json`, `results.md`, and `adoption.svg`. The HTML embeds the computed chart and tables. The researcher reviews exclusions, scoring, assumptions, and disclosure risk before sharing. Contextual tables, confidence intervals, empirical discussion, and institutional acceptance are not automatic. No input means the ordinary report remains an honest research-design edition.

Git permits only the five documented instruction/template files under `data/`; added datasets and other templates remain ignored. Do not fill and commit `data/templates/responses.csv`. Stage reviewed source files explicitly and inspect the staged diff; ignore rules cannot prevent editing an already tracked template.
