# Project explanation and viva guide

## Four-line explanation

This Operations Management project analyzes genuine published OECD employer and worker survey tables about workplace AI.
It compares adoption, perceived performance, task changes, decision assistance, and barriers across two sectors.
The code reproduces verified percentages, tables, charts, and the report from the supplied workbook.
It achieves a transparent secondary-data analysis; it does not prove causation, measure actual savings, or represent Chennai.

## 350-400 word explanation

My project is titled “Workplace AI Adoption, Perceived Performance and Implementation Barriers: A Comparative Secondary Analysis of OECD Employer and Worker Surveys.” Its primary domain is Operations Management, and its analytical approach is descriptive Data Analytics. The purpose is to understand how workplace AI adoption relates to reported operational experiences, while keeping the conclusions within the limits of the available evidence.

The project originally considered collecting questionnaire responses from managers in Chennai IT and IT-enabled services. Since genuine primary responses were unavailable, this completed report uses a clearly declared secondary-data design. It analyzes the OECD employer and worker survey report and its supplementary spreadsheet. The original fieldwork took place in 2022 across seven OECD countries, covering finance and insurance and manufacturing. These results are therefore not findings about Chennai or India.

The research questions cover adoption by sector and firm size, perceived productivity and performance, task automation and creation, decision assistance, and implementation barriers. The analysis reads published weighted proportions from identified spreadsheet cells. It converts them into percentages, combines relevant response categories transparently, checks distribution totals, and calculates descriptive percentage-point differences between sectors. Employer and worker populations are kept separate because their questions and denominators differ.

The results show employer AI adoption of 41.7 percent in finance and insurance and 29.0 percent in manufacturing. Among AI-adopting employers, 56.7 percent and 62.6 percent respectively report positive productivity effects. Among AI-using workers, 79.3 percent and 79.8 percent report improved own performance. Decision-assisted workers commonly report better and faster decisions. Automation and task creation occur together, while costs and skills are prominent barriers.

These numbers describe respondents’ reported experiences; they do not establish that AI caused productivity improvements or generated measured cost savings. The workbook contains aggregate estimates rather than individual records, so the project does not invent correlations, significance tests, or respondent-level reliability statistics. A source inconsistency in one finance cost-motivation item is disclosed and excluded from comparative conclusions.

The main achievement is a reproducible, evidence-based analysis with traceable calculations, tables, charts, and a complete report. The managerial recommendations are to begin with bounded pilots, train workers, retain human oversight, and measure actual operational outcomes before claiming benefits. Institutional acceptance of the secondary-data approach and required submission formatting still need external confirmation.

## Five-minute presentation structure

0:00-0:40: State the title, operational problem, and revised secondary-data scope.

0:40-1:30: Explain the OECD source, 2022 fieldwork, sectors, countries, and different subgroup denominators.

1:30-2:20: Explain cell extraction, weighted percentages, composite responses, percentage-point differences, and validation.

2:20-3:40: Show Tables 1-6 and the four charts. Highlight adoption, perceived performance, decisions, and barriers.

3:40-4:30: Explain limitations: perceptions, aggregates, no causal test, no Chennai inference, and the excluded source item.

4:30-5:00: Close with operational recommendations and reproducibility. Do not say that you collected the original survey.

## Likely viva questions and answers

**Why secondary data?** Genuine primary responses were unavailable; the OECD provides documented published evidence. The revised design is declared throughout the report.

**Did you collect respondents?** No. The original OECD study recruited participants. My contribution is the secondary extraction, validation, analysis, interpretation, and reproducible package.

**What is your unit of analysis?** A published sector or firm-size estimate, not an individual respondent or a Chennai team.

**Does AI cause better productivity?** This study cannot establish causation. It reports perceptions among surveyed users/adopters and descriptive sector differences.

**Why no regression or Cronbach's alpha?** The supplied workbook has aggregate percentages, not the individual responses required for those analyses.

**What does a difference of 5.90 mean?** Manufacturing's positive employer-productivity percentage exceeds finance by 5.90 percentage points. It is not a percent productivity increase or a statistically significant effect.

**Can you claim cost savings?** No. Reported costs are adoption barriers or motivations, not audited savings or return on investment.

**What source problem did you find?** A finance staff-cost motivation distribution sums to 94 percent. I preserved it, flagged it, and excluded it from comparative conclusions.

**Why use Databricks?** It is the requested notebook execution environment for the same validated Python pipeline. The dataset is small and does not require distributed processing. A local run remains supported; the platform does not make aggregate perceptions causal.

**What remains?** Institutional acceptance, identity/declaration details, signatures where required, and institution-specific formatting. No missing data is concealed.

**How can an evaluator reproduce it?** Install the three listed Python dependencies, run python build_report.py, and inspect the generated report and cell-level CSV audit.
