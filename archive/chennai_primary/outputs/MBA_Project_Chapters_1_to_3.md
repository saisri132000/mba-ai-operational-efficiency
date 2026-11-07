# Artificial Intelligence Adoption and Operational Efficiency
## An Empirical Study of Productivity, Cost Optimization and Managerial Decision-Making

**MBA research project — Main report, research-design edition v1.3**

**Updated: 5 October 2026**

Primary domain: Operations Management. Analytical methodology: Data Analytics.

Study setting: selected IT/IT-enabled service operations in Chennai city, India.

## Document status

This edition completes the research-design narrative and documents an implemented, reproducible analysis procedure. No genuine respondent dataset, external instrument review, pilot evidence, or institutional requirements have been supplied. Empirical findings, final discussion, and institutional acceptance remain pending. The words “An Empirical Study” in the working title describe the intended study; they do not certify completed data collection. Statements about recruitment and participant review describe proposed procedures.

## Abstract — research-design edition

This project develops a cross-sectional survey design to examine reported artificial intelligence adoption alongside perceived operational efficiency in selected IT-enabled service units in Chennai city. Operations Management provides the substantive focus and Data Analytics the analytical methodology. The unit of analysis is an operational team engaged in customer support, transaction processing, or back-office service delivery; one eligible manager, supervisor, or team lead reports on its preceding six months. AI-use frequency is the primary adoption indicator. Productivity, process efficiency, cost optimization, and managerial decision-making effectiveness are separate proposed outcome domains. Purposive recruitment with controlled referrals is planned, including AI users and non-users. A researcher-developed questionnaire awaits external review and feasibility piloting. The implemented procedure imports coded records, checks eligibility and duplicates, preserves missing-value reasons, and generates item summaries and an adoption-frequency chart. Domain associations and permutation tests are conditional on measurement support and defensible independence assumptions. No genuine respondent data are available in this edition, so it reports no empirical estimates or findings. The present contribution is a defined research protocol and reproducible analysis framework. Any future results will describe associations in the achieved sample rather than causal effects, verified financial savings, or Chennai-sector prevalence.

Keywords: artificial intelligence adoption; service operations; operational efficiency; managerial perceptions; Chennai; cross-sectional survey.

## Report organisation

Chapter 1 defines the problem, scope, and questions. Chapter 2 evaluates the relevance and limits of the nine-source literature base. Chapter 3 specifies participant eligibility, collection, processing, and analysis. Without supplied data, Chapter 4 records the unavailable evidence and the required outputs; a supplied-data edition replaces it with computed aggregates. Chapter 5 presents design conclusions and the procedure for evidence-based discussion. Appendix A contains the draft instrument; Appendix B supplies the executable import dictionary. Tables are numbered by chapter or appendix. No empirical figure is displayed in the no-data edition; Figure 4.1 is generated only from supplied records.

# Chapter 1: Introduction

## 1.1 Background

Operations Management concerns how organisations organise work and use resources to deliver products and services. Within service operations, relevant outcomes include output relative to effort, turnaround time, rework, resource costs, and the quality of operational decisions. AI is relevant where it is used for classification, prediction, document processing, content generation, or decision support. These applications may change how work is performed, but their usefulness must be assessed in the context of the workflow in which they operate.

For example, a support assistant may help a team prepare responses while also creating a need for human checking. Document classification may reduce initial processing effort while introducing new exception-handling tasks. These are illustrative mechanisms, not claims about the organisations to be surveyed. They motivate examining multiple operational dimensions instead of equating tool use with successful implementation.

The selected location is Chennai city. The geographic choice follows the researcher's intended recruitment setting, rather than an assertion that Chennai represents India's service sector. No local adoption rate or population count is assumed. Software-development teams, sales teams, and HR departments are outside the current operational boundary unless they directly perform one of the included service activities.

## 1.2 Research problem

The practical problem is distinguishing the extent of actual AI use from the operational outcomes that managers perceive in their units. A unit may have access to an AI product but use it rarely, use it for only a small part of its work, or use it without integrating it into the service process. Similarly, perceived time savings may coexist with additional checking costs or unchanged financial expenditure.

The study will therefore ask whether differing levels of reported adoption are associated with differing assessments of productivity, process efficiency, resource-cost efficiency, and decision effectiveness. It will not ask respondents to establish company-wide financial returns that they cannot observe. It will include units with no AI use so that the sample does not consist solely of AI enthusiasts or successful implementations.

## 1.3 Aim and objectives

**Aim:** To examine associations between reported AI adoption and perceived operational efficiency in selected IT-enabled service units in Chennai.

Objectives:

1. Describe AI adoption frequency, workflow coverage, integration, and applications in the sampled units.
2. Assess the association between adoption and perceived productivity.
3. Assess the association between adoption and perceived process efficiency.
4. Assess the association between adoption and perceived cost optimization.
5. Assess the association between adoption and perceived managerial decision-making effectiveness.

Descriptions of barriers and additional implementation effort will provide context rather than introduce a separate causal model.

## 1.4 Research questions

RQ1. What is the extent and pattern of AI adoption in the sampled operational units?

RQ2. What association exists between AI adoption and perceived productivity?

RQ3. What association exists between AI adoption and perceived process efficiency?

RQ4. What association exists between AI adoption and perceived cost optimization?

RQ5. What association exists between AI adoption and perceived managerial decision-making effectiveness?

## 1.5 Working hypotheses

RQ1 is descriptive. For RQ2–RQ5, two-sided tests will be used if the data and design support inferential analysis:

**Table 1.1. Working associational hypotheses**

| Hypothesis | Null proposition | Alternative proposition |
|---|---|---|
| H1 | Adoption has no association with perceived productivity | Adoption is associated with perceived productivity |
| H2 | Adoption has no association with perceived process efficiency | Adoption is associated with perceived process efficiency |
| H3 | Adoption has no association with perceived cost optimization | Adoption is associated with perceived cost optimization |
| H4 | Adoption has no association with perceived decision effectiveness | Adoption is associated with perceived decision effectiveness |

Table 1.1 gives research propositions rather than findings. Spearman's rank correlation between A02 and each supported three-item domain mean is the specified association estimate. Conditional permutation tests use the stronger null of independence of the paired variables under exchangeability; they are not a distribution-free test of every situation with zero rank correlation. Negative associations are possible. A non-significant result will not prove independence or the absence of a relationship. Test eligibility and unresolved interval estimation are detailed in Section 3.11.

**Table 1.2. Objective, question, measurement, and analysis alignment**

| Objective / question | Questionnaire fields | Analysis and reporting boundary |
|---|---|---|
| Objective 1 / RQ1: describe adoption | A01–A08, including A07b | A02 category counts and unknown count are generated automatically; coverage, integration, applications, duration, and stopped use require researcher-prepared contextual summaries |
| Objective 2 / RQ2 / H1: productivity association | A02 and P01–P03 | Item summaries; complete three-item mean and Spearman estimate only with measurement support |
| Objective 3 / RQ3 / H2: process-efficiency association | A02 and E01–E03 | Same conditional rule for the process domain |
| Objective 4 / RQ4 / H3: cost-optimization association | B06, A02, and K01–K03 | Cost-informed subgroup only; insufficient knowledge produces missing-by-design cost answers |
| Objective 5 / RQ5 / H4: decision-effectiveness association | A02 and D01–D03 | Same conditional rule for the decision domain |

Table 1.2 connects each substantive question to an available measurement and identifies where researcher review is needed. No question is answered by a software test.

## 1.6 Scope

The target population comprises operational teams or service-delivery units performing customer support, transaction processing, or back-office operations in IT/IT-enabled services organisations within Chennai city. Eligible managers, supervisors, and team leads form the informant population. A unit must have operated throughout the preceding six months, and the respondent must have spent at least six months in that unit with direct operational responsibility.

The unit of analysis is the operational team or service-delivery unit; one knowledgeable person provides an informant report. Respondents will select their primary supervised unit and use it consistently. Where responsibilities cover several units, they will use the unit receiving the largest share of their supervisory time. If this does not yield a clear unit, eligibility will be reviewed before inclusion.

The accessible population will depend on organisations and contacts willing to participate. It is currently unknown. The study is bounded to Chennai city and does not automatically include the wider metropolitan region. An organisation's Chennai office location alone is insufficient if the reported unit operates outside the geographic boundary.

## 1.7 Significance

The study may help participating managers distinguish adoption intensity from operational performance perceptions and identify dimensions needing further investigation. For an MBA project, it connects workflow and resource decisions to survey design and quantitative analysis. Its value will depend on the quality and scope of the evidence collected, rather than whether associations are positive or statistically significant.

## 1.8 Operational definitions

**Table 1.3. Operational definitions**

| Concept | Definition for this project |
|---|---|
| AI adoption | Actual operational use of systems producing machine-learning or generative-AI outputs, described through frequency, workflow coverage, and integration |
| Productivity | Perceived amount of completed service work relative to work time or staffing effort |
| Process efficiency | Perceived timeliness and smoothness of workflow, including errors and rework |
| Cost optimization | Perceived control of total resource costs relative to service delivered; not independently verified savings or ROI |
| Decision effectiveness | Perceived timeliness, adequacy of information, and usefulness of operational managerial decisions |
| Operational efficiency | Umbrella term for the four outcomes, not an automatically validated single score |

Table 1.3 defines the terms used throughout this report. Fixed rules, basic spreadsheets, and ordinary workflow automation are not counted as AI merely because they automate work. Ambiguous technologies will be coded as uncertain rather than confidently classified. The NIST taxonomy provides context for differentiating how AI contributes to a task (Theofanos et al., 2024); the questionnaire's operational definition is a study-specific choice, not a validated NIST scale.

## 1.9 Limitations anticipated

The survey will be cross-sectional and perception-based. Purposive participation limits generalisation. Common-source reporting, recall, social desirability, unknown cost information, and differential willingness to participate may influence findings. Units within the same organisation may share technologies and policies. Adoption may vary too little to support useful association estimates. These limitations will be reported alongside results rather than treated as problems solved by regression.

# Chapter 2: Literature Review and Conceptual Framework

## 2.1 Review approach

This focused review uses nine scholarly publications and primary institutional sources relevant to AI use, operational outcomes, and survey methodology. Bibliographic details and attribution were reviewed for this edition. It is not a systematic review: no exhaustive database search, screening count, or formal evidence-quality appraisal is claimed. Publication metadata and access to a source do not establish that its findings transfer to this population. Older sources are retained where they address measurement or sample planning; publication recency alone does not determine suitability. Additional literature may be required by the actual institutional rubric, which has not been supplied.

## 2.2 Workplace productivity evidence

Brynjolfsson et al. (2025) study an AI assistant introduced in customer-support work using operational data. This supports the relevance of service workflows to AI research. Their outcome measurement and deployment-based design differ from the present cross-sectional informant survey; their estimates will not be used as expected Chennai survey effects.

## 2.3 Adoption and organisational capability

Mikalef and Gupta (2021) examine AI capability and organisational outcomes. Their work distinguishes a broader organisational capability from simply owning technology. In this project, capability is background context; it is not substituted for adoption or measured using their firm-level scale. The unit-level instrument below is researcher-developed, not a reproduction of a validated capability instrument.

## 2.4 Enterprise and worker surveys

The OECD/BCG/INSEAD (2025) report provides enterprise-level context for studying implementation. Its countries, sampling, and respondent scope differ from this project. Its findings will not establish adoption prevalence in Chennai. The OECD workplace survey programme also distinguishes employer reports from workers' experiences, reinforcing the need to identify whose evidence is being collected (OECD, n.d.).

## 2.5 Survey-method considerations

Podsakoff et al. (2024) review common-method bias and its complexity. Because the same informant supplies adoption and outcome information here, procedural safeguards include neutral wording, separate adoption and outcome sections, and explicit unknown responses. The study will not use a single-factor test to certify the absence of common-method bias. These safeguards reduce avoidable sources of bias but cannot establish that the reports are unbiased.

Lakens (2022) explains that sample-size justification should reflect inferential goals and information value. The project will establish an access-based recruitment plan and then assess what that sample can support, instead of citing a universal minimum response count.

## 2.6 Evidence map

**Table 2.1. Evidence map of the nine cited sources**

| Source | Evidence/context | Use in this project | Transfer limitation |
|---|---|---|---|
| Brynjolfsson et al., 2025 | AI deployment in customer-support work | Operational relevance and contrast with perception measures | Does not supply an effect estimate for this survey |
| Mikalef & Gupta, 2021 | AI capability and organisational outcomes | Clarify adoption versus capability | Firm-level constructs do not automatically validate team-level items |
| OECD/BCG/INSEAD, 2025 | Enterprise AI adoption evidence | Implementation context | Not a Chennai population estimate |
| OECD workplace survey programme | Employer and worker perspectives | Match respondent role to claims | Different populations and sectors |
| Podsakoff et al., 2024 | Common-method bias review | Neutral wording and reporting safeguards | No simple diagnostic eliminates all bias |
| Lakens, 2022 | Sample planning methodology | Explicit power/precision/resource rationale | Planning does not repair selection bias |
| Theofanos et al., 2024 (NIST) | AI-use taxonomy | Clarify operational use cases | Not an adoption psychometric scale |
| Noy & Zhang, 2023 | Experiment on professional writing tasks | Distinguish task productivity evidence from survey perceptions | Task experiment does not establish service-unit or Chennai effects |
| Vaccaro et al., 2024 | Meta-analysis of human–AI combinations | Avoid assuming that assistance is uniformly beneficial | Experimental comparisons and tasks differ from the proposed survey |

Table 2.1 includes every bibliography entry; none is used as evidence that the present questionnaire is validated.

## 2.7 Bounded research contribution

### Contrasting evidence on productivity and human–AI collaboration

Noy and Zhang (2023) examine generative AI in professional writing tasks using an experiment. Their study supports investigating task-level productivity, but controlled writing tasks differ from recurring service delivery. An experiment that assigns access can support stronger causal interpretation within its setting than this project's single-time survey. Neither the outcome measures nor its effect estimates will be borrowed as if they describe Chennai operational units.

Vaccaro et al. (2024) synthesise experimental evidence on human–AI combinations. Their findings caution against assuming that combining human judgment with AI necessarily outperforms the better standalone performer. The comparison group matters: outperforming humans alone is different from outperforming both humans and AI alone. This distinction supports neutral research questions and separate decision-effectiveness measurement here. Their synthesis concerns varied experimental settings rather than this project's population.

Taken together with the customer-support evidence, these sources suggest that task characteristics and the form of assistance matter. The present project will therefore allow negative, positive, and absent associations. It will not frame AI adoption as intrinsically efficient or treat checking effort as negligible. The literature justifies investigation, not a predetermined conclusion.

### Operational interpretation of the four domains

Productivity concerns output relative to inputs. A team completing more tasks without increasing staff-hours may have higher labour productivity; a team completing more tasks by adding staff-hours may not. Task complexity also matters, so perceived productivity comparisons across support and transaction-processing units require caution. The questionnaire does not obtain a verified common output/input ratio.

Process efficiency concerns how work moves through an operation. A fast individual task can coexist with a slow end-to-end process if handoffs or exception queues create delays. Turnaround and rework are therefore examined separately from perceptions of output relative to effort. However, the domains may still overlap empirically; their distinction requires measurement assessment.

Cost optimization concerns the resources used to deliver service. Faster work may create spare capacity rather than lower expenditure. Technology charges, training, supervision, and correction work can offset apparent savings. A manager's favourable rating is not evidence of a measured reduction in operating expense. Cost results will consequently be confined to informed respondents and described as perceptions.

Decision effectiveness concerns timely and useful operational choices informed by relevant evidence. A quicker decision can still be poor if information is incomplete or unsuitable. Conversely, a slower decision may be appropriate for a complex exception. The survey will assess reported timeliness, information basis, and problem resolution without claiming to measure all aspects of decision quality.

### Explanatory perspective and competing explanations

The project uses a restrained sociotechnical perspective: tools operate within workflows involving people, information, and organisational practices. This perspective motivates attention to implementation context; it is not a separately tested theoretical construct or a claim of a comprehensive theory test.

Several explanations can generate an adoption–performance association. AI may assist work; already effective units may have greater capacity to adopt tools; stronger management or better data may support both; or respondents favourable toward technology may rate both adoption and outcomes positively. Cross-sectional adjustment cannot reliably distinguish all these explanations. They will be considered in the discussion rather than removed rhetorically by calling adoption an independent variable.

### Literature-to-design synthesis

**Table 2.2. Literature-to-design synthesis**

| Evidence or conceptual concern | Design response |
|---|---|
| Task-level evidence does not automatically establish organisation-wide gains | Consistent operational-unit boundary; no firm-wide performance claims |
| Human–AI combinations need not yield uniform benefits | Neutral outcomes and two-sided hypotheses |
| Adoption is different from broader organisational capability | Separate use descriptors; no capability-scale claim |
| Faster work does not establish cash savings | Cost-knowledge screening and no ROI estimate |
| Perceptions and objective performance differ | Explicit informant-report interpretation |
| Common-source responses can inflate apparent relationships | Neutral wording, separated sections, cautious interpretation |
| Purposive access restricts population inference | Sample-specific reporting and no sector prevalence claim |

Table 2.2 summarises the design implications of the review. The literature supports the plausibility and practical relevance of the research questions. It does not validate the original questionnaire wording. Full validation remains dependent on review and collected evidence.

The research problem remains unresolved for the intended accessible units: the reviewed task experiments, deployment study, and broader surveys do not establish whether reported adoption covaries with the four performance perceptions in this particular sample. This is a bounded application question, not proof that Chennai has been neglected by all prior research. An exhaustive review has not demonstrated a unique geographic gap; the project will not claim to be the first study of its kind. Its potential contribution is a locally defined, operationally specific assessment with transparent measurement and sampling limits. Its empirical contribution can be stated only after recruitment and collection establish what evidence is available.

## 2.8 Conceptual framework

Reported AI adoption will be examined alongside four separate perceived outcomes: productivity, process efficiency, cost optimization, and decision effectiveness. Frequency is the proposed primary adoption indicator. Coverage and integration are secondary indicators. Contextual variables include unit size and operational activity. Their inclusion will be justified before analysis; a large collection of controls will not be fitted to a small sample.

The conceptual link represents association, not a causal chain. Productivity is not modelled as necessarily causing cost optimization, and decision effectiveness is not assumed to be a mediator. No mediation, moderation, or structural-equation model is planned in this first protocol. An overall operational-efficiency score would require an explicit measurement rationale and sufficient evidence beyond internal consistency.

# Chapter 3: Research Methodology

## 3.1 Design

The study will use a cross-sectional quantitative survey with descriptive and associational objectives. One informant report represents one operational unit. Optional open comments may aid researcher interpretation but will not constitute a separately validated qualitative study or an automatic text analysis. The six-month period anchors respondents' reports; it does not create longitudinal observations or a before-and-after design. Exposure and outcomes are reported by the same person at a single collection point. Consequently, temporal ordering, selection into adoption, and unmeasured organisational conditions cannot be resolved by this design.

## 3.2 Eligibility

Eligible respondents must be adults, currently supervise an included Chennai operational unit, have at least six months in that unit, understand its operational work, and provide voluntary consent. Non-users are eligible if they can report absence of AI use. Respondents unable to establish adoption status may contribute only to clearly labelled descriptive outcome summaries if otherwise eligible; they will be excluded from adoption-association analyses.

Exclude out-of-scope locations or activities, later duplicate unit reports, respondents without direct responsibility, and units not operating for the full reference period. No response will be excluded for reporting poor performance, dissatisfaction, no benefit, or a negative association. Declared analytical omissions are evaluated per analysis; unconfirmed eligibility cannot establish inclusion. Table 3.1 specifies the import boundary.

**Table 3.1. Eligibility and record-routing rules**

| Criterion / field | Required condition | Handling when unconfirmed |
|---|---|---|
| Voluntary participation / C01 | Affirmative consent | Exclude; a code is not independent proof of consent |
| Adult respondent / S01 | At least 18 years | Exclude |
| Unit location / S02 | Within Chennai city | Exclude until a documented geographic review resolves uncertainty |
| Activity / S03 | Customer support, transaction processing, or back-office service delivery | Other activity is excluded by the importer; any legitimate classification requires a reviewed coding copy |
| Sector / S03b | IT/IT-enabled business service | No or unsure is excluded |
| Responsibility / S04 | Directly supervises the selected unit | Exclude |
| Tenure / S05 and unit continuity / S06 | Both cover at least the preceding six months | Exclude when not affirmed |
| Operational knowledge / S07 | Can report operations, with AI status known or explicitly unknown | No operational knowledge is excluded; unknown AI status permits outcome descriptions only |
| Study phase and version | Main study; questionnaire v0.3 | Pilot/test and other unmapped versions are excluded |
| Unique unit | Earliest eligible, valid-coded submission for the organisation/unit pair | Later submissions excluded with a recorded reason |

Eligibility uncertainty is resolved through documented source review before import, never by guessing affirmative answers. The original export and a dated correction log are retained. Questionnaire revisions after review require an explicit version/coding decision; the current importer accepts v0.3 only.

## 3.3 Recruitment and sampling

Purposive recruitment through professional contacts, alumni networks, and participating organisations is proposed, with controlled referrals. Recruitment will seek several organisations, different operational activities, and non-use as well as different use levels. These intentions do not create probability sampling or known population proportions.

The researcher will maintain an access log covering reachable eligible units, organisation concentration, invitation numbers, and permission requirements. Where a complete eligible roster is available, the feasibility of inviting all units or random selection will be reviewed before launch. Organisation and unit codes will help detect duplicate reports and clustering. Any linkage to contact details will be kept separately with restricted access.

## 3.4 Sample justification and stopping rule

No final sample size has been justified. The recruitment count will be set using an access audit and a documented analysis-specific power or precision assessment, following the information-based approach discussed by Lakens (2022). Assumptions will include the smallest practically meaningful association, the planned multiplicity adjustment, missingness, and organisational clustering. A small pilot will not be used to obtain a supposedly reliable expected effect size. No historical aspirational response range is adopted as a requirement.

For illustration only, the Fisher-z approximation for a two-sided correlation test is N ≈ 3 + [(z_(1−alpha/2) + z_(power))/atanh(r)]². At power .80, an assumed correlation .30, and conservative alpha .0125 for four tests, this gives approximately 120 independent complete observations. This is not an actual power calculation for the planned ordinal frequency measure or clustered data. The .30 assumption has not been established as the smallest useful effect. The illustration cannot establish a recruitment target.

The final recruitment window, invitation ceiling, and stopping rule will be recorded before outcome analysis. Recruitment will not stop when significance appears. If access falls short, the study will report a resource-constrained exploratory scope and uncertainty instead of manufacturing responses or expanding eligibility after examining results.

## 3.5 Questionnaire construction

The accompanying questionnaire is researcher-developed. Adoption questions concern reported operational use. Outcome questions concern performance over the preceding six months without attributing it to AI. All items refer to the same selected unit and period. The instrument contains consent and screening questions, unit context, separate adoption descriptors, three items for each of four proposed outcome domains, and optional contextual observations. Outcome answers use a five-category agreement scale with separate Not known and Not applicable options; omissions and declines are also preserved as missing. The wording and response structure are internally reviewed, not formally validated scales.

Productivity and process questions will be checked carefully for overlap. Cost questions will be reviewed by someone familiar with service budgets; respondents without cost knowledge will skip those items. Decision items concern operational management, not broad corporate strategy. Outcomes may be revised during validation if respondents cannot distinguish them.

## 3.6 Instrument validation procedure

First, two or three reviewers with research-methods and service-operations knowledge will assess relevance, clarity, coverage, and bias. At least one reviewer should understand operational cost reporting. Reviewers will record item-level reasons for revisions.

Second, approximately five to eight eligible people will take part in cognitive interviews. They will explain which unit they selected, what terms mean, how they retrieved answers, and when they chose 'not known.' This is a planned range, not a completed activity.

Third, a small feasibility pilot, provisionally 15–25 eligible responses if accessible, will test branching, completion time, item distributions, unknown-response rates, and duplicate handling. Such a pilot cannot establish full construct validity. Substantial revisions will trigger another usability check. Pilot responses will remain separate from main-study responses.

The survey version, item changes, response options, coding rules, and analysis protocol will be frozen before main collection. Full empirical measurement evaluation requires the main data and an adequate sample.

The current questionnaire is v0.3 following an internal document review. It clarifies whole-period frequency, task coverage, changing integration, and stopped use. This review is not an expert assessment or participant pilot. The accompanying expert-review and pilot kit supplies review prompts and routing checks. Recent or discontinued use will be reported explicitly; time since first use will not be equated with continuous exposure.

## 3.7 Ethics and confidentiality

Institutional and organisational requirements will be confirmed before launch. The participant-facing form will identify the researcher, institution, supervisor/contact route, purpose, data handling, and retention period using actual details. No invented approval number or permission will be inserted. Participation will be voluntary, and respondents may skip questions or leave before submitting. Withdrawal after submission will depend on whether a record can be identified; the consent form will describe the actual arrangement.

Personal names, client names, customer records, passwords, and confidential financial figures are unnecessary. The study will use coded records and report aggregates. Before sharing, the researcher must inspect small cells and open text and combine or omit information that could reveal an organisation or unit. The pipeline does not perform automatic disclosure suppression; even aggregate counts can be identifying in a small sample. Recruitment contact details will be separated from research data. Confidentiality will not be described as absolute anonymity when the researcher holds a code linkage. Retention and deletion dates remain pending institutional requirements.

## 3.8 Data collection and coding procedure

This section specifies collection procedures rather than claiming that they have occurred. Before launch, the researcher will confirm institutional requirements and organisation access, complete actual participant information, obtain instrument review, and test the chosen survey platform and export. The repository contains an instrument specification and importer; it is not an online survey collector. Cognitive interviews and feasibility-pilot responses will be labelled and stored separately from main-study records. Recruitment dates, invitation denominators where known, exclusions, protocol changes, and stopping decisions will be logged without using significance results to decide when to stop.

After collection, the original export will be preserved unchanged under restricted local storage. A reviewed coding copy will map platform headings and labels to Appendix B explicitly. CSV must be UTF-8; JSON must be an array of records. Excel exports must first be saved as UTF-8 CSV. Administrative metadata comprise a unique record code, organisation code, unit code, submission timestamp with timezone, phase, and questionnaire version. Metadata are non-empty text; identifier whitespace is trimmed before duplicate checks. Organisational code assignment requires researcher review because the importer cannot detect two different codes assigned to the same organisation.

A01 is imported as the text categories yes, no, or not known, not as numeric 1/0. A02–A04 use their specified ordinal codes. Optional context and free-text fields remain private and are not automatically summarised. Missing required columns, empty datasets, malformed rows, invalid metadata, or non-unique record identifiers stop the import for correction. This is distinct from row-level exclusions for invalid eligible substantive answers. Any corrections are dated and justified in the coding log; source values are not overwritten.

## 3.9 Cleaning, duplicates, and missing values

Records are ordered by submission timestamp, with original row order breaking an exact tie. Eligibility and valid coding are checked before unit deduplication. For a repeated organisation/unit pair, the earliest eligible, valid-coded record is retained; later submissions receive a duplicate exclusion reason. An earlier invalid record does not silently replace a valid one: its exclusion is visible in the audit. Records are never selected because their outcomes are more favourable. Uniform ratings alone do not establish invalidity. The importer does not use completion time or optional tool examples to discard records.

Documented omissions, unknown values, not-applicable values, and declined answers remain distinct missing reasons. Numeric answers are checked for finite integer values within their specified ranges. An invalid answer in an applicable analytical field excludes the record and is logged; a documented missing value does not. The researcher reviews coding errors against the original export before rerunning. The audit reports source row numbers without publishing personal identifiers.

Unknown AI status at S07, or an unknown/omitted/declined A01 answer, leaves adoption descriptors unclassified while retaining otherwise eligible outcome information. Confirmed non-use requires explicit zero codes in A02–A04; zeros are not silently imputed. If claimed use conflicts with zero-use codes, or claimed non-use is not confirmed by all three zero codes, the adoption descriptors become unclassified and the contradiction is logged. A changing A04 level remains a distinct non-scored category while valid frequency and coverage are retained.

When B06 does not establish sufficient cost knowledge, cost items are masked before analytical validation and marked missing by design. Omitted or declined B06 answers retain their own missing reason. Values in a skipped cost route do not invalidate usable non-cost outcomes; route corrections are logged. The same principle applies to numerical adoption values entered despite an unknown-adoption route. This does not legitimise invalid values in questions the respondent was eligible to answer.

No midpoint substitution, across-respondent mean imputation, or artificial numeric missing code is used. A supported domain mean requires all three valid 1–5 answers. Different domains may consequently have different usable counts. Unknown adoption excludes a record from adoption associations but not item descriptions. Cost results concern the cost-informed subgroup. No overall operational-efficiency mean or summed adoption scale is computed.

## 3.10 Descriptive analysis and measurement assessment

The automatic analysis reports imported and retained unit counts, distinct organisations, largest-organisation contribution, classified A02 category counts, and the unknown/unclassified adoption count. Each of the twelve outcome items has a valid-answer count, missing count, median, response-category distribution, and missing-reason breakdown. Distributions and missing reasons are stored in the private analysis output; the generated report's item table shows valid N, missing N, and median. Unknown responses are not added to the neutral agreement category. Any percentage added by the researcher must state its denominator. The sample adoption distribution is not a Chennai population prevalence estimate.

For each three-item domain, complete responses permit a diagnostic Cronbach's alpha calculation when at least three records and non-zero total-score variance are available. This minimum is a computational condition, not an adequate validation sample. Alpha may be unavailable or unstable and is stored in the private analysis output. It is not a pass/fail criterion or proof of construct validity, unidimensionality, or separation from other domains. Conceptual coverage, observability, item relationships, and achieved sample adequacy need genuine assessment. Domain scoring is disabled unless the researcher lists a supported domain and supplies a measurement-support account; entering that account does not itself validate a scale.

## 3.11 Statistical estimates and test decision rules

For a supported domain, the estimate is Spearman's rank correlation between A02 and its complete three-item mean. Tied values receive average ranks. Association estimates use only pairs with known A02 and a complete supported domain. With fewer than three pairs or a constant variable, the estimate is not calculated; the computational minimum does not establish sufficient statistical information. Table 3.2 states the decision rules.

**Table 3.2. Implemented analysis decisions and limits**

| Decision | Implemented procedure | Interpretation limit |
|---|---|---|
| No measurement support | Item descriptions only; domain association withheld | Do not select an item or domain because it gives a favourable result |
| Supported complete domain | Three-item mean; pair-specific Spearman estimate | Equal spacing of adoption categories is not assumed; outcome mean is a justified scoring choice |
| Inferential testing | Requires a researcher independence/exchangeability rationale and no repeated contributing organisation | One unit per organisation is necessary under this implementation, not sufficient proof of independence |
| Two-sided permutation calculation | Compare absolute rank correlations; all permutations at paired N ≤ 7; otherwise 1,999 shuffles with seed 20261005 and plus-one correction | Tests the independence null under exchangeability; numerical p-values do not create representative sampling |
| Four primary comparisons | Holm adjustment; unavailable tests count as p=1 internally for adjustment only | Untested comparisons are still shown as not estimated, never as observed p=1 |
| Multiple units in an organisation | Disable all inferential p-values in this conservative implementation | Descriptive association may remain; no automatic cluster correction is provided |
| Low variation or insufficient pairs | Not estimated | Neither no effect nor evidence against the research question |
| Uncertainty intervals | Not implemented | Final interval method requires a design-appropriate decision and separately validated analysis |

The primary family comprises the four associations in Table 1.2. Where testing is defensible, raw and Holm-adjusted p-values are reported with paired counts and effect estimates. A family-level .05 decision threshold is proposed for protocol review before collection; the software reports p-values and does not issue hypothesis verdicts. P-values are secondary to magnitude, measurement quality, sampling limits, and uncertainty. Non-significance is not proof of zero association, and statistical significance is not proof of practical importance or causality.

## 3.12 Visualization and reporting outputs

The implemented figure is a horizontal bar chart of A02 categories from Never to Daily/almost daily. Bars show counts of retained units with classified frequency; unknown/unclassified frequency is reported separately in text. The chart has category labels and counts, with no invented baseline, trend, or causal comparison. It is generated only from supplied records and embedded in the combined report as Figure 4.1. No figure is rendered as a finding in the no-data edition. Synthetic checks carry an explicit test-only label.

The private cleaned-record file retains coded values and missing reasons. A separate audit records inclusion, exclusions, and route flags. The analysis file contains item distributions, missingness, diagnostic alpha, adoption counts, and conditional association outputs. The results document displays computed counts, item summaries, and the association table; the chart is a separate SVG and is embedded in the combined HTML report. Neither document generates an interpretation of the study's findings or institutional approval. Disclosure review remains necessary before any private aggregate is released.

## 3.13 Reproducibility and data integrity

The supplied manifest identifies the input as genuine or synthetic, records a truthful provenance account, and binds the analysis to the exact file through a SHA-256 checksum. The results also record input and manifest checksums. These digests detect a changed file; they do not authenticate respondents, certify informed consent, or establish institutional approval. Real inputs and research outputs must remain under ignored private storage. Synthetic software checks remain under ignored scratch storage and are rejected by the ordinary research-report command.

The analysis uses Python's standard library; the report uses the repository's pinned rendering dependency. The same coded input and manifest, code revision, Python/dependency environment, and fixed random seed permit rerunning the calculation. Record the actual software versions and commit identifier in the study log when data are analysed. The procedure preserves inputs and produces a new auditable output set. Reproduction of a calculation is distinct from replication of empirical findings in another sample.

To rebuild this edition, run `python build_report.py`. To process genuine responses, follow Appendix B and supply `private/responses.csv` and `private/study.json`, then run:

```sh
python research_pipeline.py --input private/responses.csv --manifest private/study.json --out private/analysis
python build_report.py --input private/responses.csv --manifest private/study.json --output private/MBA_Project_Report.html
```

Automated tests use explicitly synthetic fixtures to check eligibility, routes, missingness, deduplication, statistics, output isolation, and report presentation. They provide evidence about implementation, not participants or questionnaire validity. The no-input edition contains no empirical estimates. A supplied-data edition includes only the declared input analysis; synthetic checks are explicitly labelled and isolated from research findings.

## 3.14 Analyses requiring separate review

Invitation-based response rates, role/tenure/headcount profiles, coverage/integration/application summaries, recent or stopped-use comparisons, and interpretation of optional comments require real contextual records and researcher-prepared tables. The current importer retains extra export columns privately but does not automatically analyse them. Known recruitment denominators come from the recruitment log, not the response file alone.

Interquartile ranges, secondary A03/A04 associations, two-of-three sensitivity scores, confidence intervals, adjusted models, and organisation-dependent inference are not implemented. They are conditional extensions, not promised automatic outputs or completed analyses. If required, their methods must be justified using the achieved design, recorded as protocol amendments, implemented separately, and validated before use. No factor-analysis method, mediation model, ROI calculation, or causal effect is promised. If defensible scoring or inference is unavailable, a transparent descriptive report is preferable to unsupported significance claims.

# Chapter 4: Results Framework — Pending Empirical Data

## 4.1 Data availability

No genuine participant dataset has been supplied. The repository therefore provides no evidence of completed recruitment, an achieved sample, organisation composition, adoption distributions, or outcome scores. The absence of data is not a finding of zero adoption or no association. This chapter is a results framework, not an empirical-results chapter. No numerical entries or simulated findings are inserted.

## 4.2 Analysis status

The implemented methods in Chapter 3 have been checked with isolated synthetic software fixtures, not participant observations. No empirical reliability coefficient, correlation, uncertainty interval, hypothesis-test result, or financial saving is reported. A successful test of a calculation does not validate the questionnaire or answer a research question. Table 4.1 specifies how each result component can be produced after genuine input is available.

**Table 4.1. Results readiness and source requirements — no empirical values**

| Result component | Genuine input required | Output / review after input |
|---|---|---|
| Eligibility and retained-unit flow | Coded responses, metadata, and collection log | Import/retained counts and row-level exclusions; invitation-based rates require the real recruitment log |
| Organisation contribution | Consistent organisation/unit codes | Organisation count and largest contributor; review dependence and disclosure risk |
| Adoption-frequency description | Valid A02 or documented unknown route | A02 counts and unknown count; adoption chart generated from supplied values only |
| Outcome-item descriptions | P01–P03, E01–E03, K01–K03, D01–D03 and B06 | Valid/missing counts and medians in the report; distributions and missing reasons in private analysis output |
| Measurement diagnostics | Complete domain answers plus actual review/pilot evidence | Alpha diagnostic in private output; researcher assesses domain suitability |
| Primary associations | Known A02, complete domain answers, and supported-domain decision | Pair-specific Spearman estimate; not estimated when unsupported or non-estimable |
| Inferential tests | Independent/exchangeable design, documented rationale, and adequate data | Conditional permutation p-values and Holm adjustment; withheld when assumptions cannot be supported |
| Context, uncertainty, and final discussion | Real contextual/recruitment records and methodological review | Researcher-completed tables, justified interval analysis if needed, and evidence-based interpretation |

Table 4.1 is an output specification. It contains no participant counts, effect estimates, or expected direction. In a supplied-data edition, the builder replaces this chapter with computed Tables 4.1–4.2 and Figure 4.1. Unsupported results remain labelled not estimated; they do not become zero or a neutral finding.

## 4.3 Evidence needed for empirical completion

Empirical completion requires external questionnaire review, feasibility piloting, a justified recruitment plan, actual collection under appropriate consent arrangements, and an analysis suited to the achieved sample. Appendix B specifies the required coded fields; the genuine file and truthful provenance manifest are placed under private storage and processed using Section 3.13. Organisation clustering, unknown cost information, and measurement adequacy must be assessed before final statistical reporting. Invitations, permissions, reviews, and pilot activity are not inferred from a data-file checksum.

## 4.4 Reporting sequence after genuine data arrive

The researcher first reconciles the coded copy with the original export and collection log, reviews the exclusion/route audit, and checks the achieved sample against the protocol. Item summaries precede any domain scoring decision. Each supported association is assessed with its own usable count, variation, and assumptions. Untested domains remain visible. The computed tables and figure are then checked against the private analysis file and reviewed for disclosure risk. Contextual results and any separately validated uncertainty estimates are added with their actual methods and denominators. Only then can a completed results abstract and discussion be written.

# Chapter 5: Discussion Framework, Limitations, and Design Conclusions

## 5.1 What this project establishes

The project establishes a bounded, operationally focused research design for examining reported AI use alongside perceived productivity, process efficiency, cost optimization, and decision effectiveness in selected Chennai IT-enabled service units. It specifies a consistent unit of analysis, eligible respondents, a six-month reporting period, non-user inclusion, and separate adoption indicators. These are design conclusions, not empirical answers to the research questions.

## 5.2 What remains unestablished

The design has no empirical conclusion about the direction or magnitude of adoption–performance relationships. In the no-data edition, the questions in Table 1.2 remain empirically unanswered. Supplying records permits estimates, but their interpretation requires actual methodological assessment and a completed discussion. The project does not establish that AI increases productivity, improves decisions, or reduces expenses. No tool-adoption recommendation is justified merely by a planned survey or automatically generated table. The instrument's external review and measurement evidence must be documented separately. Completing the report's design sections does not complete the empirical study.

## 5.3 Contribution and limitations

The contribution at this stage is a research-design report connecting service-operations concepts to a transparent survey method. Its boundaries protect against treating favourable perceptions as causal evidence or task-level time savings as verified financial returns. Table 5.1 summarises the limitations that must remain visible in the final interpretation.

**Table 5.1. Study limitations and interpretation consequences**

| Limitation | Consequence for a future finding |
|---|---|
| Purposive access and voluntary response | Cannot establish Chennai-sector prevalence or population-representative associations |
| Cross-sectional self-report | Temporal order, reverse association, and causal effects remain unresolved |
| Common informant for exposure and outcomes | Favourable reporting tendencies may contribute to apparent relationships |
| Six-month recall and changing adoption | Exposure can be averaged imperfectly; recent or stopped use needs contextual reporting |
| Different task complexity and unit scale | Perceived performance is not a comparable verified output/input measure across all units |
| Cost-knowledge filter | Cost findings apply to the cost-informed subgroup and are not verified savings or ROI |
| New three-item domains | Coverage, overlap, and scoring support need real review; alpha alone is insufficient |
| Missingness and complete-item scoring | Usable counts differ; available cases may differ systematically from missing cases |
| Organisation dependence | Multiple units can share policies and technology; independent-row p-values are disabled |
| Small or low-variation achieved sample | Estimates may be unavailable or imprecise; non-significance cannot establish no association |
| Limited nine-source review | No exhaustive research-gap or comprehensive evidence-quality claim |
| Design prepared without genuine data or an institutional rubric | Data analysis alone cannot establish reviewed findings, approved formatting, or institutional acceptance |

The software's present limits also matter: it does not collect responses, certify provenance, automatically suppress revealing cells, or supply confidence intervals and cluster inference. These are disclosed procedural limits, not negative empirical findings.

## 5.4 Evidence-based discussion procedure — pending data

After actual analysis, discussion will proceed question by question using the estimates and usable counts rather than the sign of a p-value alone. The researcher will consider magnitude, uncertainty where defensibly estimated, measurement adequacy, missingness, and organisation concentration. Comparison with Brynjolfsson et al. (2025), Noy and Zhang (2023), and Vaccaro et al. (2024) must retain their different tasks, measures, designs, and comparison groups. Agreement in direction would not replicate their causal evidence; disagreement would not automatically refute it.

Alternative explanations include more capable units adopting AI, better management or data supporting both adoption and perceived performance, and common-source reporting tendencies. A negative or non-estimable association must be discussed as openly as a positive one. Claims are limited to reported use and perceived outcomes within the achieved sample. No discussion of hypothetical favourable results is presented as a completed finding.

## 5.5 Recommendations that can be made at this stage

The present recommendations concern research conduct: complete participant information and relevant permissions; review and pilot the instrument; include eligible non-users; preserve the original export and coding log; justify recruitment and stopping rules before main analysis; and report every planned domain, including unsupported or non-estimable analyses. These recommendations follow the design's needs, not observed operational improvements.

Operational recommendations must await genuine findings and managerial context. Even then, a perception-based association can motivate further investigation rather than certify an AI investment or financial return. Decisions about specific tools would require evidence of feasibility, implementation effort, objective performance, and costs beyond this survey.

## 5.6 Conclusion and future research

This edition establishes an implementable, bounded study of reported AI adoption and four operational-performance perceptions in selected Chennai service units. The research question is justified, the measurements are specified, and data-processing and conditional analysis procedures are reproducible. This is a design conclusion, not an empirical answer. The final conclusion must be rewritten after genuine evidence and supervisory review, while preserving the distinction between association and causation.

Future research using operational records, repeated observations, and credible deployment comparisons could address stronger performance or causal questions. Such extensions require a different design and are not completed features of the present project.

# References

All nine entries below are cited in Chapters 1–2 and mapped in Table 2.1. The bibliography uses a consistent author–date format; the actual institution's required style remains unknown.

Brynjolfsson, E., Li, D., & Raymond, L. (2025). Generative AI at work. *The Quarterly Journal of Economics, 140*(2), 889–942. https://doi.org/10.1093/qje/qjae044

Lakens, D. (2022). Sample size justification. *Collabra: Psychology, 8*(1), 33267. https://doi.org/10.1525/collabra.33267

Mikalef, P., & Gupta, M. (2021). Artificial intelligence capability: Conceptualization, measurement calibration, and empirical study on its impact on organizational creativity and firm performance. *Information & Management, 58*(3), 103434. https://doi.org/10.1016/j.im.2021.103434

Noy, S., & Zhang, W. (2023). Experimental evidence on the productivity effects of generative artificial intelligence. *Science, 381*(6654), 187–192. https://doi.org/10.1126/science.adh2586

OECD. (n.d.). *OECD AI surveys of employers and workers*. Retrieved 5 October 2026, from https://www.oecd.org/en/about/projects/aisurveysofemployersandworkers.html

OECD/BCG/INSEAD. (2025). *The adoption of artificial intelligence in firms: New evidence for policymaking*. OECD Publishing. https://doi.org/10.1787/f9ef33c3-en

Podsakoff, P. M., Podsakoff, N. P., Williams, L. J., Huang, C., & Yang, J. (2024). Common method bias: It's bad, it's complex, it's widespread, and it's not easy to fix. *Annual Review of Organizational Psychology and Organizational Behavior, 11*, 17–61. https://doi.org/10.1146/annurev-orgpsych-110721-040030

Theofanos, M. F., Choong, Y.-Y., & Jensen, T. (2024). *AI use taxonomy: A human-centered approach* (NIST AI 200-1). National Institute of Standards and Technology. https://doi.org/10.6028/NIST.AI.200-1

Vaccaro, M., Almaatouq, A., & Malone, T. (2024). When combinations of humans and AI are useful: A systematic review and meta-analysis. *Nature Human Behaviour, 8*, 2293–2303. https://doi.org/10.1038/s41562-024-02024-1

# Project validation status

**Table S.1. Research validation and completion status**

| Element | Present status |
|---|---|
| Title | Non-causal working title checked; institutional acceptance unknown |
| Variables | Defined; empirical measurement support pending |
| Scope | Chennai and IT-enabled service boundary specified |
| Questionnaire | v0.3 internally reviewed; external review and pilot pending |
| Sampling | Purposive strategy specified; access and justified target unknown |
| Statistical methods | Implemented core specified; real-data assumptions, intervals, and any extensions require review |
| Interpretation | Guardrails specified; actual findings pending |

Table S.1 distinguishes internal document/software checks from external and empirical validation. Completion is tracked by deliverables rather than an institution-assessed percentage. The abstract, literature synthesis, design, questionnaire, collection specification, and analysis/reporting framework are developed. External review, genuine data, real-data analysis, and final empirical conclusions remain pending. The repository is delivered privately; participant records and contact-code linkages are excluded from publication.

# Appendix A: Draft Survey Instrument

The accompanying questionnaire is the authoritative instrument for this edition. Its current version is v0.3, internally reviewed and awaiting external review and pilot testing. It is included in full in the generated report. Appendix B documents the import codes used by the implemented analysis.
