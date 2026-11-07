# Current project status

## Complete implementation

Canonical scope: **Workplace AI Adoption, Perceived Performance and Implementation Barriers: A Comparative Secondary Analysis of OECD Employer and Worker Surveys**. The source data concern 2022 fieldwork in seven OECD countries and two sectors. The report, software, dependencies, tests, notebook, and package use this design. The old Chennai questionnaire study is archived, not the current findings source.

Implemented: source hash verification, 152 source-cell extractions, 36 distribution checks (35 pass; one item excluded), 16 sector comparisons, firm-size comparisons, four charts, five-chapter PDF/HTML/Markdown report, references, presentation/viva guide, interactive explainer with browser speech, and a reproducible ZIP. These are software and descriptive-analysis achievements, not a new survey or causal study.

## Databricks status

Notebook and setup instructions are included. Target project folder: **Buisness projects** in a new user-created workspace. The pipeline is tested locally; live Databricks execution is not yet verified. No workspace, notebook run, or deployment is claimed without actual access.

## External requirements

Institutional acceptance of secondary data, required student/institution details, declarations, signatures, formatting, and final supervisor review. No genuine primary data are needed for the current descriptive outputs. Chennai conclusions or respondent-level inference would require a separately designed study and appropriate data.

Run `python build_report.py` to regenerate the current report, explainer, and ZIP. Run `python -m unittest discover -s tests -v` for the active secondary-analysis checks. Source integrity errors stop the build rather than silently changing the evidence. Use `git rev-parse HEAD` to identify the code revision; generated PDF timestamps are not a fixed content identifier.
