# Workplace AI Adoption, Perceived Performance and Implementation Barriers

**A comparative secondary analysis of OECD employer and worker surveys.**

## Independent regression study using Stack Overflow 2025

A revised empirical draft, **AI Use at Work**, is available in `outputs/stackoverflow2025/AI_Use_at_Work_Regression_Report.docx` and its HTML/PDF versions. It uses genuine public respondent records and fits five exploratory logistic regressions on adoption, perceived agent productivity, debugging frustration, complex-task ratings and trust. This study has revised objectives and an employed-professional-developer population; supervisor acceptance of that scope remains pending. It does not pool records with OECD aggregates or describe Chennai managers.

Install `requirements-stackoverflow.txt`, run `python scripts/download_stackoverflow.py`, then `python stackoverflow_analysis.py`. Run the analysis checks with `python -m unittest discover -s tests -p test_stackoverflow_analysis.py`. Full definitions, missingness, diagnostics, coefficient tables, source hashes, attribution and report-regeneration steps are in `outputs/stackoverflow2025/README.md`. The downloaded archive contains 49,191 records versus the publisher's 49,009 headline count; the unresolved difference is disclosed throughout the revised report.

The sections below describe the preserved OECD version. Its build command does not generate the independent regression report.

Operations Management is the primary domain; descriptive Data Analytics is the method. The project reads genuine published OECD aggregates from 2022 fieldwork, checks them, compares finance/insurance and manufacturing, and generates a five-chapter report, charts, explanation page with read-aloud controls, and a submission ZIP.

## Evidence and boundaries

This OECD version replaces the uncollected Chennai primary-survey design, which is preserved under `archive/chennai_primary/` for history only. The GitHub repository retains its historical name; that name does not define the current population.

- Inputs: unchanged OECD PDF and supplementary workbook in `sources/`.
- Population: Austria, Canada, France, Germany, Ireland, the United Kingdom, and the United States; finance/insurance and manufacturing. These are not Chennai or India data.
- Unit: published sector/firm-size response estimates, not individual records.
- Outputs: weighted percentages and descriptive percentage-point comparisons.
- No causal claims, objective savings, significance tests, or primary questionnaire collection.
- A finance cost-motivation distribution totals 94%; it is disclosed and excluded from comparisons.

## Where the data come from and how extraction works

The original OECD study conducted the surveys in early 2022 and published the report in 2023. The user supplied the downloaded report PDF and supplementary Excel workbook. We did not conduct the original survey, retrieve individual responses, or collect Chennai managers' data.

The [official OECD study page](https://www.oecd.org/en/about/projects/aisurveysofemployersandworkers.html) provides the report and **Figures and data (.xlsx)** download. Our code reads the preserved local workbook at `sources/OECD_published_tables.xlsx` with openpyxl; it does not scrape a website, call a live OECD API, or automatically download new releases. It extracts selected worksheet cells, records source coordinates and subgroup sizes, checks distributions, and calculates percentages and descriptive comparisons. For example, `Figure 3_2!B33` contains approximately 0.567; multiplying by 100 gives 56.7%. SHA-256 checks identify the approved source files. Seven-country coverage belongs to the original survey; it does not mean every sector estimate is a separate observation for each country.

## Credentials and reuse rights

Checked against OECD's official guidance on 24 October 2026:

- **Published workbook and report:** the official page provides public downloads. Our current pipeline requires no OECD account, password, API key, or paid subscription to process those downloaded files.
- **Reuse conditions still apply:** public availability does not remove copyright. OECD's [data terms](https://www.oecd.org/en/about/terms-conditions.html) generally permit extraction and reuse with attribution, subject to any specific or third-party restrictions. Retain source citations and notices, identify adaptations, and do not imply OECD endorsement. This 2023 report predates the default CC licensing introduced on 1 July 2024; do not automatically label it CC BY 4.0. See the [OECD open-access policy](https://www.oecd.org/en/about/oecd-open-by-default-policy.html) and the specific source notices.
- **Respondent-level microdata:** this is a separate access route. OECD states that accredited researchers must apply, justify non-commercial research use, and comply with its Terms of Use. The application is linked under **Access to microdata** on the study page. Downloading the public workbook does not grant microdata access. We have neither obtained nor claimed this approval. Seek institutional/supervisor support; do not assume eligibility, payment requirements, or permission to redistribute microdata or upload them to Databricks/GitHub.

## Regression feasibility for each objective

No regression has been fitted with the current aggregate workbook. The existing 152 extracted rows are estimates from different questions and populations, not independent respondent records. The two sector percentages per indicator cannot support a meaningful adjusted respondent-level regression. Country labels or subgroup counts cannot reconstruct the missing joint observations. Regression is not automatically appropriate for every objective.

The following are conditional plans, not implemented models or findings. Review the actual approved microdata, codebook, sampling/weighting information, and subgroup availability before choosing predictors, coding outcomes, checking sample support, and revising the descriptive objectives to include associational questions.

| Objective | Candidate regression with suitable microdata | Required distinction |
|---|---|---|
| 1 Adoption patterns | Binary logistic regression for employer AI adoption; candidate predictors include sector, country, and firm size | Requires employer records containing both adoption states and predictors |
| 2 Performance perceptions | Ordered logistic regression for an ordinal performance rating, or binary logistic regression for a justified improved/not-improved outcome | Employer productivity and worker performance need separate models; an AI-related rating asked only of users cannot estimate a users-versus-nonusers adoption effect |
| 3 Task and work changes | Separate binary logistic models for automation/creation and ordered models for ordinal pace/control ratings | Employer and worker surveys remain separate; overlapping task indicators are not mutually exclusive outcomes |
| 4 Decision assistance | Binary logistic model for receiving assistance; separate ordinal models for quality/speed agreement among assisted workers | Assistance prevalence and perceptions among assisted workers use different populations; assistance itself is constant within the assisted-only subgroup |
| 5 Adoption barriers | Separate binary logistic models for each reported barrier, with suitable available employer covariates | Barriers can overlap and do not measure realized cost savings or return on investment |

If approved microdata become available, assess survey weights/design, missingness, sparse categories, model fit and assumptions, uncertainty, and justified multiple-comparison handling. Country controls do not alone solve survey-design or confounding issues; seven countries do not automatically justify ordinary cluster-robust inference. Any resulting coefficients would describe adjusted associations, not causal effects. Until then, retain the verified descriptive results rather than creating unsupported coefficients, p-values, or synthetic respondents.

## Questions answered

1. How does published AI adoption differ by sector and firm size?
2. What productivity and performance perceptions do the relevant employers/workers report?
3. What task changes, pace, and control are reported?
4. How prevalent is decision assistance, and what do assisted workers report about it?
5. What cost and skill barriers do employers report?

## Local setup and run

Python 3.10+:

```sh
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python build_report.py
.venv\Scripts\python -m unittest discover -s tests -v
```

macOS/Linux: use `.venv/bin/python` in the same commands. No environment variables, credentials, database, or API service are required. The three pinned libraries read Excel, generate PDF, and check PDF output. Standard-library code generates the CSV/JSON, SVG, HTML, and ZIP. Builds verify source SHA-256 hashes before reading the workbook.

## Databricks

Use **Buisness projects** as the folder inside your new Databricks workspace. Follow [DATABRICKS_SETUP.md](DATABRICKS_SETUP.md), clone this private repository there, and open `Databricks_OECD_Analysis.py`. It installs the same dependencies, runs the same pipeline, and displays the generated report inline. No Windows wheels or private tokens are committed. Cloud execution must be verified in your actual workspace; local tests do not certify Databricks execution.

## Outputs

| File/folder | Purpose |
|---|---|
| `report/PROJECT_REPORT.pdf` | Print-ready five-chapter report |
| `report/PROJECT_REPORT.html` | Navigable report; keep `figures/` beside `report/` |
| `report/PROJECT_REPORT.md` | Generated report text |
| `outputs/Project_Complete_Explainer.html` | Standalone interactive explanation with optional browser speech |
| `outputs/AI_Comparison_Dashboard.html` | Offline topic/indicator filters, sector charts, source categories, calculations, and subgroup sizes |
| `outputs/MBA_Secondary_Data_Submission_Package.zip` | Portable current package, including notebook and explainer |
| `results/observations.csv` | 152 source-traceable published estimates, not participants |
| `results/sector_comparisons.csv` | 16 descriptive comparisons |
| `results/data_quality.json` | Distribution checks and the excluded item |
| `results/VERIFICATION.json` | Build checks, not institutional approval |
| `figures/`, `references/`, `explanation/` | Charts, original source references, presentation/viva guide |

Open the HTML files directly in a browser. Available read-aloud voices depend on browser/device; some voices need a network connection.

The comparison dashboard provides 16 sector indicators and four adoption comparisons by firm size. Select a research topic, then an indicator, or inspect a row in the comparison table. Each view shows weighted percentages, manufacturing-minus-finance percentage-point differences, original unweighted subgroup sizes, the contributing response categories, and source worksheet/cells. Values are read-only. It works offline with no added dependencies. Run `python scripts/build_dashboard.py` to rebuild only this page from existing results; `python build_report.py` regenerates and includes it in the ZIP. Download the HTML from Databricks and open it in a browser for interaction.

## Architecture and reproducibility

`sources/` → `research_pipeline.py` → validation → descriptive calculations → `results/` + `figures/` + `report/` → `scripts/build_explainer.py` → ZIP via `build_report.py`.

The workbook remains unchanged. Proportions are multiplied by 100. Relevant answer categories are summed explicitly. Sector differences are manufacturing minus finance in percentage points. Original unweighted subgroup sizes are labels, not reconstructed weighted response counts. Existing source inconsistencies are never silently normalized. The builder checks required source cells and response totals, then records source hashes and results.

The active test suite covers source integrity, calculated values, source-quality handling, report/HTML structure, package contents, and notebook structure. Historical tests remain in the archived primary project. Generated PDF metadata can differ between builds; analysis values and source hashes are reproducible.

## Submission status and limitations

The descriptive secondary report and software are implemented. This is a bounded comparison of published survey findings, not a new causal study or comprehensive literature review. The references comprise the original report and supplementary workbook. Institution acceptance, identity details, declarations, signatures, and required formatting remain external. See [FINAL_SUBMISSION_STATUS.md](FINAL_SUBMISSION_STATUS.md) and [SUBMISSION_BLOCKERS.md](SUBMISSION_BLOCKERS.md).

Source: Lane, Williams, & Broecke (2023), OECD Working Paper No. 288, [DOI](https://doi.org/10.1787/ea0a0fe1-en), and its supplied supplementary workbook. OECD source rights and attribution remain applicable.
