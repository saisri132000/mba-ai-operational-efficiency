# Pre-collection analysis decisions

**Draft v0.2 — updated 5 October 2026**

This is a working protocol, not a registered study or a completed analysis. Freeze final decisions before main collection after the pilot and access audit. Any subsequent changes must be dated, justified, and distinguished from the original plan.

## Research model

Primary exposure: A02, AI-use frequency over the whole preceding six months, ordinal 0–4. Four separate outcomes are proposed: productivity, process efficiency, cost optimization, and managerial decision effectiveness. Outcome scores remain conditional on conceptual and measurement support. Coverage A03 and integration A04 are secondary adoption descriptors. No causal chain, mediation model, or grand efficiency score is specified.

## Record inclusion

Include eligible, consenting main-study unit records. Pilot and routing-test records are excluded from the main dataset. The implemented importer retains the earliest eligible valid-coded submission for an organisation/unit pair, ordered by timezone-aware timestamp and then original row order. Invalid applicable codes and other exclusions are logged before deduplication. Do not select records based on favourable answers. Preserve the original export and an exclusion/change log.

Uncertain geographic, activity, or sector eligibility must be resolved in a documented reviewed coding copy before inclusion; the importer excludes uncertain/other codes. Unknown or omitted/declined adoption information does not disqualify an otherwise eligible record from clearly labelled outcome descriptions, but excludes it from adoption-association analyses. Unknown/omitted/declined cost knowledge produces cost-domain missingness only, preserving the routing-answer reason. Routes are applied before numeric validation of skipped fields.

## Adoption coding

A02: Never=0; less than monthly=1; monthly but less than weekly=2; weekly but less than daily=3; daily/almost daily=4. Treat as ordinal; do not describe one category change as an equal increase in use.

For A01=No, zero-use descriptors may be derived only from the explicit confirmed non-use route. For A01=Unknown, adoption descriptors remain unknown. Contradictions or ambiguous tool descriptions are flagged; if not resolvable without guessing, adoption is unclassified for association analysis. A missing optional tool example alone does not establish misclassification. Changing integration is a non-scored category for A04. First-use timing and stopped use are reported separately from frequency.

## Outcome scoring

Primary scoring rule: a three-item domain mean requires all three valid 1–5 responses and defensible domain coherence. Report domain-specific sample counts. Two-of-three means may be examined in a labelled sensitivity analysis. No mean imputation across respondents, and no midpoint substitution for unknown responses. Cost results concern the cost-informed subgroup; discuss how its composition differs from the broader sample.

If a domain cannot be supported, report its items descriptively rather than choose the item with the best association. Document any reformulation before main collection where possible. A high alpha alone is not evidence of adequate construct coverage or distinctiveness. Three-item domains provide limited evidence for broader measurement claims.

## Descriptive reporting

The implemented outputs contain imported/retained counts, row-level exclusions/flags, organisation counts/concentration, A02 category counts, unknown adoption, item counts/medians, distributions, and missing reasons. Private analysis output also contains diagnostic alpha. The HTML item table displays valid N, missing N, and median, not every private distribution. Recruitment denominators, operational activity/role/tenure/headcount profiles, broader adoption categories, and interquartile ranges require researcher-prepared, reviewed analyses of genuine logs/context. Percentages require clearly stated denominators. The sample adoption proportion is not Chennai-sector prevalence.

## Primary associational analysis

Implemented estimate: Spearman correlation between A02 and each supported complete three-item domain mean, with average ranks for ties. Conditional tests are two-sided permutation tests of independence under exchangeability, not general tests of every zero-rank-correlation null. They require an explicit independence rationale and at most one retained unit per organisation. Exact enumeration is used through seven pairs; larger samples use 1,999 shuffles with seed 20261005 and a plus-one correction. Holm adjustment applies across the four prespecified outcomes. If an outcome is not estimable, report it as untested; retain the original family of four by treating untested comparisons as p=1 for adjustment only, without presenting a fabricated observed p-value. A family-level .05 threshold is proposed for protocol review; the software produces no automated hypothesis verdict.

Report effect magnitude and discuss uncertainty alongside any tests. Confidence intervals are not implemented; any final interval method requires an achieved-design justification and separately validated calculation. Organisation dependence disables p-values in the current pipeline; no ordinary individual-row bootstrap or independent-observation significance test is authorised for multiple units from the same organisation. With too few organisations for reliable dependence handling, descriptive associations may be more defensible than confirmatory significance claims.

Do not interpret a non-significant result as proof of zero association. Do not interpret a small adjusted p-value as proof of operational importance, causality, or sample representativeness.

## Secondary and sensitivity analysis

The following are possible separately reviewed extensions, not current automatic pipeline outputs. Record and justify any adopted procedure before use; do not imply that it has already run.

- A03 and A04 associations: exploratory; report their missingness and avoid selective significance reporting.
- Recent-adopter and discontinued-use patterns: describe exposure differences. Any exclusion sensitivity must be labelled and retain the original primary analysis.
- Outcome means with two valid items: compare cautiously with complete-item results if justified.
- Organisation concentration: report how much the sample depends on its largest contributors; do not treat removal of an inconvenient organisation as a new primary result.
- Adjusted models: optional only if sample and design support them. Unit size and activity are the proposed minimal contextual variables; do not choose controls by p-values.

## Decisions still open

The sample target, stopping dates, actual organisation spread, smallest useful association, interval method, measurement evaluation feasible at achieved N, confidentiality retention period, and final platform are not known. This protocol records those gaps; it does not fill them with assumptions presented as fact.

## Claims permitted by this design

Example: “In the sampled units with complete responses, reported AI-use frequency was associated with perceived process efficiency.” Add the estimate and uncertainty when real data exist.

Claims such as “AI caused savings,” “Chennai firms became more productive,” or “AI adoption is X% across the sector” are unsupported by this design. A six-month recall period does not make the study longitudinal.
