# Stack Overflow regression analysis

This is an independent revised research report using genuine public respondent data. It does not replace or pool the existing OECD aggregate report.

Open AI_Use_at_Work_Regression_Report.docx or the HTML report. The original supplied draft is untouched. Candidate and guide metadata come from that draft and need confirmation. The revised scope requires supervisor acceptance. The public archive has 49,191 rows; the publisher reports 49,009 analysed responses. This unresolved difference is disclosed, not silently corrected.

Reproduce from the repository root:

    python -m pip install -r requirements-stackoverflow.txt
    python scripts/download_stackoverflow.py
    python stackoverflow_analysis.py
    python -m unittest discover -s tests -p test_stackoverflow_analysis.py
    python scripts/build_stackoverflow_report.py --template outputs/stackoverflow2025/AI_Use_at_Work_Regression_Report.docx

Outputs appear in outputs/stackoverflow2025. Five primary logistic models adjust for grouped experience, organisation size and country; frequency is included only in user models. Primary estimates use HC1 intervals and Holm correction over five nominated contrasts. See report for definitions, restrictions, reference categories and limitations. No predictive or causal validation is claimed. Full coefficient CSVs include exploratory control-variable estimates.

Data licence: Stack Overflow Developer Survey 2025, Stack Exchange. Publisher identifies ODbL 1.0 for the database and DbCL 1.0 for contents. See https://survey.stackoverflow.co/ and https://opendatacommons.org/licenses/odbl/1-0/ . Retain attribution and applicable notices. Raw source CSVs are downloaded separately and are not included in the results package. Model-row extracts contain public ResponseId values and must not be used to identify respondents.
