# Appendix B: Data Dictionary and Analysis Rules

Use coded UTF-8 CSV or a JSON array with one row per submitted unit report. Required columns may contain documented missing tokens for analytical items, A01, and B06, but eligibility must be affirmatively established. Table B.1 gives the authoritative importer schema; no response rows are supplied.

**Table B.1. Required import fields and codes**

| Field | Allowed values / meaning |
|---|---|
| record_id | Non-empty text code; no names/emails; record_id unique after whitespace trimming |
| organisation_code | Non-empty text code; use consistently for the same organisation |
| unit_code | Non-empty text code identifying the unit within its organisation; pair used for deduplication |
| submitted_at | ISO 8601 timestamp with timezone; earliest eligible submission retained |
| phase | main, pilot, test |
| questionnaire_version | Text 0.3; other versions need a reviewed mapping |
| C01 | no, yes |
| S01 | no, yes |
| S02 | no, unsure, yes |
| S03b | no, unsure, yes |
| S04 | no, yes |
| S05 | no, yes |
| S06 | no, unsure, yes |
| S03 | back-office service delivery, customer support, other, transaction processing |
| S07 | no, unknown ai status, yes |
| B06 | limited, none, sufficient; documented missing tokens allowed |
| A01 | no, not known, yes; documented missing tokens allowed |
| A02 | Integer 0–4; missing tokens allowed |
| A03 | Integer 0–4; missing tokens allowed |
| A04 | Integer 0–3; missing tokens allowed; changed also allowed |
| P01 | Integer 1–5; missing tokens allowed |
| P02 | Integer 1–5; missing tokens allowed |
| P03 | Integer 1–5; missing tokens allowed |
| E01 | Integer 1–5; missing tokens allowed |
| E02 | Integer 1–5; missing tokens allowed |
| E03 | Integer 1–5; missing tokens allowed |
| K01 | Integer 1–5; missing tokens allowed |
| K02 | Integer 1–5; missing tokens allowed |
| K03 | Integer 1–5; missing tokens allowed |
| D01 | Integer 1–5; missing tokens allowed |
| D02 | Integer 1–5; missing tokens allowed |
| D03 | Integer 1–5; missing tokens allowed |

Missing tokens: empty, Not known/unknown, Not applicable/NA, Prefer not to answer. They remain distinct missing reasons, never zero or the midpoint. A02 codes: 0 Never; 1 Less than monthly; 2 Monthly but less than weekly; 3 Weekly but less than daily; 4 Daily/almost daily. A03: 0 None; 1 >0–<25%; 2 25–<50%; 3 50–<75%; 4 75–100%. A04: 0 No use; 1 Isolated use; 2 Selected workflows; 3 Embedded workflows; changed non-scored. B06: none/limited/sufficient correspond to cost knowledge. S07 unknown ai status corresponds to the questionnaire's longer unknown-status option. Outcome codes 1–5 follow the questionnaire agreement scale.

A01 uses text yes/no/not known, not numeric 1/0; B06 uses none/limited/sufficient. Omitted or declined A01 leaves adoption unclassified; omitted or declined B06 masks cost answers and retains its missing reason. Eligibility uncertainty requires documented resolution in a reviewed coding copy before import. Optional additional export columns are retained privately, not included in aggregate reports. B04/B05 map to organisation_code/unit_code; the remaining contextual questions and free text are not analysed automatically. Export platforms must map their own headings/labels explicitly to these codes; the importer never guesses labels. Excel exports must be saved as UTF-8 CSV. Complete three-item means are scored only for researcher-supported domains. Alpha is an exploratory diagnostic and cannot establish construct validity. No grand efficiency score is produced. No cluster inference, regression, mediation, ROI, or automatic empirical conclusion is implemented.
