# Submission handoff

**AI Adoption and Operational Efficiency — Chennai IT-enabled services**

## A. What is complete

Five-chapter research-design report, pre-data abstract, nine-source review, aligned questions/measures, methods, limitations, pending-results/discussion frameworks, draft questionnaire, and import dictionary. No genuine data, empirical findings, external instrument validation, or institutional approval are claimed.

## B. What is automatically reproducible

Offline report; coded CSV/JSON validation, consent/eligibility checks, chronological unit deduplication, missingness audit, item summaries, and an adoption chart. Supported domains permit conditional Spearman/permutation/Holm outputs. Software tests use isolated synthetic fixtures. Setup and testing commands are in README.md.

## C. Exact external inputs still needed

Actual institutional/participant-information requirements; external instrument review/pilot; genuine access, recruitment/stopping and sampling justification; consented de-identified responses with truthful provenance; final measurement/inference decisions, disclosure review, discussion, and supervisor sign-off.

## D. Exact steps to insert genuine data

Preserve the original export locally under `data/raw/` or `private/raw/`. Create new `private/responses.csv` with `python research_pipeline.py --template private/responses.csv` or copy the header-only `data/templates/responses.csv` without overwriting an existing dataset. Map only real responses to `data/templates/DATA_DICTIONARY.md`. Keep pilot/test records separate and log corrections. Record the real file digest using `python -c "from research_pipeline import checksum; print(checksum('private/responses.csv'))"`.

Create `private/study.json` with `evidence_kind: "real"`, truthful `provenance`, and that `input_sha256`; initially use `supported_domains: []`, `independent_unit_inference: false`. Enable scoring/tests only with actual support and the required measurement/independence notes. A declaration is not validation.

## E. Exact regeneration workflow

From the configured repository environment:

```sh
python research_pipeline.py --input private/responses.csv --manifest private/study.json --out private/analysis
python build_report.py --input private/responses.csv --manifest private/study.json --output private/MBA_Project_Report.html
```

Review the audit and outputs, add genuine contextual results and empirical interpretation, and apply actual institution requirements. Intervals and cluster analysis need separately justified methods. Share only after disclosure review.

## F. Exact report output location

Current no-data edition: `outputs/MBA_Project_Report.html`, rebuilt with `python build_report.py`. After genuine input: `private/MBA_Project_Report.html`; audit/statistics under `private/analysis/`. Open the HTML offline; Print / Save as PDF uses the browser. No invented results fill pending sections.

## G. Final GitHub commit and branch

Branch: `main`. Repository: [mba-ai-operational-efficiency-chennai](https://github.com/Naramalakumarteja/mba-ai-operational-efficiency-chennai) (private). The release commit is titled **Release final research project submission package**. Obtain its exact SHA with `git log -1 --format=%H -- SUBMISSION_HANDOFF.md`; this identifies the commit containing this handoff without a self-referential hash inside the committed file. Compare with `git ls-remote origin refs/heads/main`. Genuine data and private analysis are excluded from GitHub.
