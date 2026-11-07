## 1. COMPLETED

The research-design edition has a five-chapter academic narrative: a pre-data abstract, problem and bounded contribution, aligned objectives/questions/hypotheses, a nine-source literature synthesis, detailed methodology, pending-results framework, discussion procedure, limitations, research-conduct recommendations, and design conclusions. Tables have chapter/appendix captions. References are alphabetised and consistently cited; NIST authorship and the Science issue number were verified. There is no empirical figure or fabricated statistical result in this edition.

Appendix A contains the internally reviewed v0.3 questionnaire. Appendix B is generated from the actual import schema. Recruitment/review/protocol documents distinguish required fields, optional context, planned participant activity, and implemented analysis. The existing pipeline supports coded CSV/JSON, eligibility and chronological deduplication, route-aware missingness, item summaries, diagnostic alpha, conditional Spearman/permutation/Holm outputs, private audit files, and reproducible offline reports. Synthetic checks are isolated and labelled; they cannot enter the ordinary research report. These are implementation and internal-review achievements, not evidence of external validation or collection.

[SUBMISSION_HANDOFF.md](SUBMISSION_HANDOFF.md) gives the supervisor-facing release workflow. [data/README.md](data/README.md) and the bundled header-only CSV/dictionary provide the exact response format without any respondent records. Original exports and computed data remain ignored; genuine coded input belongs under `private/`.

## 2. REQUIRES EXTERNAL INPUT

- **Actual institutional and participant-information requirements:** handbook/template/rubric, student/institution/supervisor/contact details, required permissions and consent arrangements, retention/withdrawal procedure, and deadline. Place truthful materials under `private/requirements/`; no institution rules or approvals are assumed.
- **External instrument review and pilot evidence:** dated review/cognitive-interview/pilot records under `private/validation/`, followed by justified wording/coding and domain-support decisions. Current items are not formally validated. A revised instrument needs an explicit version mapping before main import.
- **Real access and collection protocol:** accessible organisations/units, permissions, collection dates, stopping rule, invitation denominators where known, and sample/inference justification under `private/protocol.md` and restricted recruitment logs. No response target or independence assumption is established automatically.
- **Genuine consented, de-identified records and provenance:** original export and coded UTF-8 CSV or JSON under `private/`, plus `private/study.json` declaring truthful provenance and the exact file checksum. No genuine respondent records are supplied.
- **Final empirical and supervisory judgment:** achieved-design assessment, supported scoring/inference decisions, suitable uncertainty analysis if needed, disclosure review, discussion/conclusions, and submission sign-off. Record decisions under `private/discussion.md` or make approved report-source edits. Software cannot certify validity or acceptance.

## 3. HOW TO COMPLETE AFTER DATA ARRIVES

1. Review real requirements and the collection protocol. Complete participant information, instrument review/pilot, version/coding decisions, and recruitment justification before main use. Supplying a file does not retrospectively establish those activities.
2. Preserve the original export unchanged. Map a reviewed copy to Appendix B's required columns and categories. JSON metadata must be text; timestamps need timezones. Keep pilot/test records separate. Log corrections and legitimate eligibility resolutions; never guess answers.
3. If useful, create a header-only template with `python research_pipeline.py --template private/responses.csv`; this creates no response rows and refuses to overwrite an existing file. Add only genuine coded records.
4. Compute the actual digest with `python -c "from research_pipeline import checksum; print(checksum('private/responses.csv'))"`. Create `private/study.json` with `evidence_kind: "real"`, truthful `provenance`, and that `input_sha256`. Initially use `supported_domains: []` and `independent_unit_inference: false`. Enable domains/inference only with actual assessment and the required `measurement_support_note`/`independence_note`; these declarations alone prove nothing.
5. Run the existing commands:

   ```sh
   python research_pipeline.py --input private/responses.csv --manifest private/study.json --out private/analysis
   python build_report.py --input private/responses.csv --manifest private/study.json --output private/MBA_Project_Report.html
   ```

6. Review `audit.json`, `cleaned.json`, and `analysis.json` against the original export and protocol. Chapter 4 then contains computed Tables 4.1–4.2 and Figure 4.1. Distributions, missing reasons, and alpha diagnostics are in the private analysis file. Contextual/recruitment tables, intervals, sensitivity analyses, and cluster methods are not generated automatically; adopt only justified, separately validated procedures.
7. Review small cells/open text before sharing. Write the final empirical abstract, question-by-question discussion, bounded recommendations, and conclusions from actual findings. Update completed procedures and protocol deviations in Chapter 3. Apply the institution's real format and obtain the required review. The current design discussion is not an empirical conclusion.
8. Run `python -m unittest discover -s tests -v` and rebuild the report. Preserve private inputs and outputs locally; commit only reviewed non-sensitive source/code changes. Record the software versions, code revision, and input/manifest hashes in the study log for reproducibility.
