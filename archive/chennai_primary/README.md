# Artificial Intelligence Adoption and Operational Efficiency

An MBA research project on productivity, cost optimization, and managerial decision-making in Chennai IT-enabled service operations. Operations Management is the primary domain; Data Analytics is the analytical methodology.

## Overview and problem statement

The project examines whether reported operational AI use is associated with perceived efficiency. It separates actual use from perceptions of benefits and distinguishes productivity, process efficiency, cost optimization, and decision effectiveness. It is a cross-sectional survey design, not a causal study.

**Evidence status:** the research design and questionnaire are drafted. No participant review, pilot, main survey dataset, or empirical results exist. This repository is a working research-design deliverable, not a completed empirical dissertation or an institution-approved submission.

## Implemented features

- Existing Chapters 1–3 and scholarly references preserved.
- One maintained questionnaire source, integrated at build time as Appendix A.
- Pre-data abstract, aligned questions/measures, numbered tables, detailed methods, pending-results and discussion frameworks, and design conclusions without fabricated findings.
- Offline HTML report with section navigation, responsive layout, readable tables, and browser print/save-as-PDF.
- Source checks for chapter completeness, questionnaire items, duplicate appendix, and machine-specific paths.
- Automated tests of navigation, output, error handling, and raw HTML escaping.
- Coded CSV/JSON import with eligibility, consent, version, duplicate, adoption, and cost-route checks.
- Missing-reason audit, item distributions/medians, diagnostic internal consistency, and an adoption SVG chart.
- Conditional Spearman/permutation-test and Holm framework, gated by measurement support and independent-unit rationale.
- Genuine-evidence report integration; synthetic inputs are rejected from the research report.
- Header-only response template, authoritative import dictionary, and supervisor handoff.

## Technology and architecture

Python 3.10+ and Python-Markdown 3.11. No database, backend framework, cloud service, API key, or JavaScript dependency is needed. The small inline print action uses the browser's native print dialog.

Workflow: report Markdown + questionnaire Markdown → source validation → Markdown rendering → self-contained HTML. Historical review/recruitment documents remain available but are not required to view or build the main report.

Data workflow: researcher-coded input + SHA-256 provenance manifest → chronological eligibility/deduplication → private cleaned records and audit → item summaries and supported-domain analysis → private aggregate report. The new pipeline uses only Python's standard library; the rendering dependency is unchanged.

## Setup

From the repository folder:

```sh
python -m venv .venv
```

Activate on Windows PowerShell with `.\.venv\Scripts\Activate.ps1`, or on macOS/Linux with `source .venv/bin/activate`, then:

```sh
python -m pip install -r requirements.txt
```

No environment variables are required. No `.env` file should be created or committed.

## Build, run, and example usage

```sh
python build_report.py
```

Open `outputs/MBA_Project_Report.html` in a browser. It works offline without a server. Use section links to navigate and **Print / Save as PDF** for browser printing. For a local web preview:

```sh
python -m http.server 8000 --bind 127.0.0.1 --directory outputs
```

Visit `http://127.0.0.1:8000/MBA_Project_Report.html`. Stop the server with Ctrl+C. The server is a local read-only preview, not a survey collector. Rebuild after editing sources. An alternate HTML destination is supported with `python build_report.py --output outputs/preview.html`; other file extensions are rejected to protect source and configuration files.

## Tests and syntax checks

```sh
python -m unittest discover -s tests -v
python -m py_compile build_report.py research_pipeline.py tests/test_report.py tests/test_pipeline.py
```

Tests use no real participant data and do not validate the questionnaire scientifically. There is no configured linter or type-checking tool; neither is required to build this small document renderer.

## Project structure

```text
build_report.py                   Report builder and source validation
research_pipeline.py              Import, validation, cleaning, analysis, SVG/tables
SUBMISSION_BLOCKERS.md             Exact external evidence and requirements needed
FINAL_SUBMISSION_STATUS.md         Completed academic package and post-data procedure
SUBMISSION_HANDOFF.md              One-page supervisor/evaluator handoff
requirements.txt                  Single pinned rendering dependency
tests/test_report.py              Critical automated checks
tests/test_pipeline.py            Isolated synthetic software tests
outputs/
  MBA_Project_Chapters_1_to_3.md   Main report source (historical filename)
  MBA_Draft_Questionnaire.md       Canonical questionnaire source
  MBA_Project_Report.html         Generated offline report, ignored by Git
  other .md files                 Existing research support documents
data/
  README.md                       Exact input/validation/regeneration instructions
  raw/README.md                   Original-export storage instructions
  processed/README.md             Analysis-output storage instructions
  templates/responses.csv         Empty response header; no respondent rows
  templates/DATA_DICTIONARY.md     Authoritative field codes and missing-value rules
work/                             Ignored scratch area
private/                          Ignored genuine input and analysis output
```

The historical main-report filename is retained to preserve existing links. It now contains all five chapter headings, with Chapters 4–5 transparently documenting the lack of data. The standalone questionnaire is the authoritative source for the generated appendix.

## Privacy and GitHub delivery

Commit only report sources, code, tests, documentation, and the empty response template. Participant responses, contact details, code linkages, credentials, and exports belong outside this repository or in ignored local `private/`, `data/raw/`, `data/processed/`, or `responses/` folders. Only the five instruction/template files listed under `data/` are allowed by Git. Never add responses to the tracked template; create the genuine coded copy under `private/`. Ignore rules reduce accidents but do not replace staged-diff review. Generated HTML is rebuilt locally.

The configured GitHub repository is private: [mba-ai-operational-efficiency-chennai](https://github.com/Naramalakumarteja/mba-ai-operational-efficiency-chennai). Access and collaborator permissions are managed through GitHub.

## Limitations and future improvements

The unknown institution requirements, respondent access, external questionnaire review, pilot, justified sample target, and collected data prevent empirical completion. Perceptions cannot establish causal effects, verified financial savings, or sector-wide adoption rates. Final institution formatting requires actual requirements. The software does not collect surveys or certify provenance; it processes supplied coded records. Cluster inference, regression, confidence intervals, and automatic empirical conclusions are deliberately absent. A supported descriptive association is not proof of causality; no numeric findings exist until genuine input is supplied.

## Add genuine questionnaire responses and rerun

Appendix B of the generated report is the complete import data dictionary, also available in [data/templates/DATA_DICTIONARY.md](data/templates/DATA_DICTIONARY.md). Questionnaire text is in Appendix A. [data/README.md](data/README.md) explains every input rule; [SUBMISSION_HANDOFF.md](SUBMISSION_HANDOFF.md) gives the submission workflow and remaining external inputs. The bundled [responses.csv](data/templates/responses.csv) has no response rows. Create a new **empty** header-only private template (no generated responses):

```sh
python research_pipeline.py --template private/responses.csv
```

Map an actual survey export explicitly to these columns/codes. A01 requires text `yes`, `no`, or `not known`, rather than numeric 1/0. Keep the original export separately under `private/`. JSON input is also supported as an array of objects with the same keys. Excel must be exported to UTF-8 CSV; no column or category mappings are guessed. `submitted_at` must contain a timezone. Phase `pilot`/`test` is excluded from main analysis. Unknown eligibility is excluded until documented resolution in a reviewed coding copy. Invalid applicable answer codes are excluded with row-number reasons; malformed files/metadata fail explicitly. Documented missing A01/B06 answers retain eligible outcome data, with adoption unclassified or cost items skipped as appropriate. Those routes are applied before numerical checks for skipped answers. Optional contextual/free-text columns stay private and are not automatically analysed.

Metadata fields must be non-empty text, including JSON version codes such as `"0.3"`. Identifier whitespace is trimmed before duplicate checks; record identifiers must remain unique. Compute the checksum of the actual file:

```sh
python -c "from research_pipeline import checksum; print(checksum('private/responses.csv'))"
```

Create `private/study.json` yourself with these keys: `evidence_kind` (real only for actual research records), `provenance` (truthful collection/export account), `input_sha256` (the printed digest), `supported_domains` (initially an empty array), and `independent_unit_inference` (initially false). These instructions provide no invented provenance or checksum. Supported domains may be `productivity`, `process`, `cost`, and `decision`; enabling them requires `measurement_support_note` from genuine methodological assessment. Enabling inference requires `independence_note` explaining independence/exchangeability. Merely writing a note does not establish validity.

```sh
python research_pipeline.py --input private/responses.csv --manifest private/study.json --out private/analysis
python build_report.py --input private/responses.csv --manifest private/study.json --output private/MBA_Project_Report.html
```

The pipeline preserves input files and writes `cleaned.json`, `audit.json`, `analysis.json`, `results.md`, and `adoption.svg`. All are private/ignored. Full item distributions, missing reasons, and alpha diagnostics appear in `analysis.json`; the report displays item counts/medians, conditional associations, and the chart. The combined report replaces the pending-results chapter with computed aggregates but generates no final empirical judgment. Without input, `python build_report.py` still creates the honest no-evidence report. The researcher reviews disclosure risks before sharing; suppression is not automatic. The abstract, completed-procedure narrative, contextual results, and empirical discussion require genuine evidence and researcher edits as described in `FINAL_SUBMISSION_STATUS.md`.

Three-item domain means require complete answers and researcher support. Unknown/declined/not-applicable values remain missing; cost answers from insufficiently informed respondents are masked and logged. Duplicate units retain the earliest eligible timestamp, not the export's row order. Tests use exact permutations at N ≤ 7 and 1,999 seeded permutations otherwise. Holm adjustment keeps four planned comparisons; untested outcomes are not assigned observed p-values. More than one retained unit per organisation disables p-values. One unit per organisation alone does not establish independence: the researcher must justify it. No confidence intervals are generated. Alpha diagnostics do not establish validity or determine score support automatically.

## Synthetic software testing

Fixtures are generated only by `tests/test_pipeline.py` inside temporary directories under ignored `work/`; all carry synthetic provenance and are never bundled as research records. Synthetic pipeline output is prominently labelled and must remain under `work/`. The final report refuses synthetic manifests. For isolated integration testing only, `build_report.py --synthetic-check --input work/synthetic.json --manifest work/test-manifest.json --output work/synthetic-check.html` renders a clearly labelled test report. This mode cannot write to research output directories. No persistent demo dataset or simulated final findings is shipped. The software cannot prove whether a researcher falsely labels input; provenance remains an external responsibility.
