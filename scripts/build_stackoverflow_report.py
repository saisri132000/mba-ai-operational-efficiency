"""Build the revised research report from checked regression output."""
from pathlib import Path
import argparse
import csv
import html
import json
import zipfile
import base64
from copy import deepcopy
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

TITLE = 'AI Use at Work'
SUBTITLE = 'Developer Adoption, Perceived Productivity, Trust and Challenges Using Stack Overflow Survey 2025'
PROJECT_URL = 'https://github.com/saisri132000/mba-ai-operational-efficiency'
LABELS = {'M1_adoption':'AI adoption', 'M2_productivity':'Perceived agent productivity',
          'M3_debugging':'Debugging frustration','M4_complex_tasks':'Complex-task ratings','M5_trust':'Trust in AI accuracy'}
CONTRASTS = {'M1_adoption':'20+ versus under 5 years of experience',
             'M2_productivity':'Daily versus monthly/infrequent agent use',
             'M3_debugging':'Daily versus monthly/infrequent AI-tool use',
             'M4_complex_tasks':'Daily versus monthly/infrequent AI-tool use',
             'M5_trust':'Daily versus monthly/infrequent AI-tool use'}
REFS = [
('Stack Overflow. (2025). Developer Survey 2025 methodology.', 'https://survey.stackoverflow.co/2025/methodology'),
('Stack Overflow. (2025). Developer Survey 2025 AI results and question wording.', 'https://survey.stackoverflow.co/2025/ai'),
('Stack Exchange. (2025). Survey archive results.csv schema.csv and survey.pdf. Public archive accessed 7 November 2026; local CSV obtained 2 November 2026 and verified by SHA-256.', 'https://github.com/StackExchange/Survey/tree/main/packages/archive/2025'),
('Stack Overflow. Survey data and files. The download page identifies ODbL 1.0 for data and DbCL 1.0 for contents.', 'https://survey.stackoverflow.co/'),
('Open Data Commons. Open Database License 1.0.', 'https://opendatacommons.org/licenses/odbl/1-0/'),
('statsmodels. Generalized linear models and binomial logit estimation. Version 0.15.0 used in this analysis.', 'https://www.statsmodels.org/stable/generated/statsmodels.genmod.generalized_linear_model.GLM.html'),
('statsmodels. Multiple testing correction with multipletests; Holm method.', 'https://www.statsmodels.org/stable/generated/statsmodels.stats.multitest.multipletests.html')]


def pvalue(p):
    return '<0.001' if p < .001 else f'{p:.3f}'


def build(root, template):
    out=root/'outputs/stackoverflow2025'
    analysis=json.loads((out/'analysis.json').read_text(encoding='utf-8'))
    audit=analysis['audit']; models=analysis['models']; sensitivity=analysis['sensitivity']
    source=Document(template)
    doc=Document(template)
    for node in list(doc.element.body):
        if node.tag != qn('w:sectPr'):
            doc.element.body.remove(node)
    # Reuse the supplied report's page system, Times New Roman styles and footer.
    for style_name in ['Normal','Title','Subtitle','Heading 1','Heading 2','Heading 3']:
        style=doc.styles[style_name]
        style.font.color.rgb=RGBColor(0,0,0)
        for borders in list(style.element.iter(qn('w:pBdr'))):
            borders.getparent().remove(borders)
    for section in doc.sections:
        for p in section.footer.paragraphs:
            for run in p.runs:
                if 'Workplace AI Adoption' in run.text:
                    run.text=run.text.replace('Workplace AI Adoption, Perceived Performance and Implementation Barriers','AI Use at Work')
    doc.styles['Normal'].paragraph_format.space_after=Pt(6)
    doc.styles['Normal'].paragraph_format.line_spacing=1.12
    doc.styles['Normal'].font.size=Pt(11)
    body=[]
    def para(text, style=None):
        doc.add_paragraph(text,style)
        body.append('<p>'+html.escape(text)+'</p>')
    def heading(text,level=1):
        doc.add_heading(text,level)
        anchor='section-'+str(len(body))
        body.append(f'<h{level+1} id="{anchor}">{html.escape(text)}</h{level+1}>')
    def page():
        doc.add_page_break()
    def repository_link():
        p=doc.add_paragraph('Public VIT project repository: ')
        link=OxmlElement('w:hyperlink')
        from docx.opc.constants import RELATIONSHIP_TYPE
        rel=doc.part.relate_to(PROJECT_URL,RELATIONSHIP_TYPE.HYPERLINK,is_external=True)
        link.set(qn('r:id'),rel)
        run=OxmlElement('w:r');props=OxmlElement('w:rPr')
        color=OxmlElement('w:color');color.set(qn('w:val'),'0563C1');props.append(color)
        underline=OxmlElement('w:u');underline.set(qn('w:val'),'single');props.append(underline)
        run.append(props);text=OxmlElement('w:t');text.text=PROJECT_URL;run.append(text)
        link.append(run);p._p.append(link)
        body.append('<p>Public VIT project repository: <a href="'+PROJECT_URL+'">'+PROJECT_URL+'</a></p>')
    def table(headers,rows):
        t=doc.add_table(rows=1,cols=len(headers));t.style='Table Grid'
        for c,txt in zip(t.rows[0].cells,headers):c.text=str(txt)
        pr=t.rows[0]._tr.get_or_add_trPr();repeat=OxmlElement('w:tblHeader');pr.append(repeat)
        for row in rows:
            for cell,txt in zip(t.add_row().cells,row):cell.text=str(txt)
        for i,row in enumerate(t.rows):
            # Repeating header, auto heights, subtle alternating fill, no split rows.
            trpr=row._tr.get_or_add_trPr();trpr.append(OxmlElement('w:cantSplit'))
            for cell in row.cells:
                tcpr=cell._tc.get_or_add_tcPr()
                borders=OxmlElement('w:tcBorders')
                for edge in ['top','left','bottom','right']:
                    e=OxmlElement('w:'+edge);e.set(qn('w:val'),'single');e.set(qn('w:sz'),'4');e.set(qn('w:color'),'D9D9D9');borders.append(e)
                tcpr.append(borders)
                if i==0 or i%2==0:
                    sh=OxmlElement('w:shd');sh.set(qn('w:fill'),'DDE6EF' if i==0 else 'F5F5F5');tcpr.append(sh)
                for p in cell.paragraphs:
                    p.paragraph_format.space_after=Pt(4);p.paragraph_format.space_before=Pt(4)
                    for r in p.runs:r.font.size=Pt(10);r.bold=i==0
        body.append('<div class="table"><table><thead><tr>'+''.join('<th>'+html.escape(str(h))+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+html.escape(str(v))+'</td>' for v in row)+'</tr>' for row in rows)+'</tbody></table></div>')

    doc.add_paragraph(TITLE,'Title');doc.add_paragraph(SUBTITLE,'Subtitle')
    body.append('<h1>'+TITLE+'</h1><p>'+SUBTITLE+'</p>')
    logo=root/'assets/VIT_logo.jpg'
    if logo.is_file():
        p=doc.add_paragraph()
        p.alignment=WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(str(logo),width=Inches(2.9))
        encoded=base64.b64encode(logo.read_bytes()).decode('ascii')
        body.append('<p style="text-align:center"><img alt="VIT Vellore Institute of Technology" style="width:290px;max-width:100%;height:auto" src="data:image/jpeg;base64,'+encoded+'"></p>')
    for text in ['A PROJECT REPORT','Master of Business Administration Online MBA',
                 'Submitted by Eesha Sai Sri Y','Register Number 24MBA7051',
                 'Guide named in supplied draft Suraj P G','VIT Online Learning Program',
                 'Vellore Institute of Technology','November 2026',
                 'Revised empirical draft for supervisor review']:
        p=doc.add_paragraph(text);p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    para('Candidate, registration and guide details are retained from the supplied draft for confirmation. Institutional acceptance, signatures and required formatting remain subject to review. The original OECD report is preserved separately; its findings are not pooled with these respondent records.')
    page();heading('Declaration and review status')
    para('Draft declaration for the candidate to review before signing: This report uses publicly released Stack Overflow Developer Survey 2025 responses for secondary analysis. No primary questionnaire was administered by this project. The scope, exclusions, model specifications and limitations are disclosed. The candidate must confirm the declaration and institutional requirements before submission.')
    para('Candidate signature ____________________    Date ____________________')
    heading('Supervisor review',2)
    para('The supervisor is requested to review the revised dataset, objectives, research design, interpretation and report format. This draft does not certify institutional approval or completed supervision.')
    para('Guide signature ____________________    Date ____________________')
    heading('Acknowledgements',2)
    para('The project acknowledges Stack Overflow and the survey respondents for the published data and questionnaires. The supplied draft identifies Suraj P G as guide. Naramala Kumar Teja and Keerthana P assisted with the project. Roles and acknowledgements should be confirmed by the candidate and supervisor.')
    page();heading('Abstract')
    para(f'This Operations Management project examines AI adoption and developers’ reported experiences using public Stack Overflow Developer Survey 2025 microdata. The archive contains {audit["source_rows"]:,} rows, while the publisher reports 49,009 responses in its published analysis. The reason for the 182-row difference has not been established; the present analysis documents its own cohort and does not claim exact reproduction of the published figures. The scope is employed professional developers: {audit["employed_professional_cohort"]:,} records before question-specific and covariate exclusions. Five exploratory binary logistic regressions examine adoption, agent-productivity agreement, debugging frustration, complex-task ratings and trust. Models adjust for grouped work experience, organisation size and grouped country; experience is the exposure in the adoption model. Models of user experiences additionally compare usage frequencies. Robust HC1 standard errors and 95% confidence intervals are reported, with Holm correction for five nominated primary contrasts.')
    for m in models[:2]:
        r=m['primary'];para(f'{LABELS[m["name"]]} model: n={m["n"]:,}; {CONTRASTS[m["name"]]}; adjusted odds ratio {r["odds_ratio"]:.2f}, 95% CI {r["ci_low"]:.2f}–{r["ci_high"]:.2f}.')
    para('Results describe associations within selected respondents. Voluntary recruitment, missingness, reverse causation and self-reported outcomes prevent causal, national-population or objective financial claims. Operational recommendations concern controlled pilots, human review and measurement of real task time and quality.')
    para('Keywords: AI adoption; perceived productivity; developer workflow; trust; logistic regression; Operations Management; Stack Overflow.')
    heading('Report contents',2)
    for text in ['1 Introduction and research scope','2 Evidence and conceptual framework','3 Methodology and measurement',
                 '4 Results and validation','5 Discussion recommendations and limitations','6 References','Appendices and reproducibility']:
        para(text)
    page();heading('1 Introduction and research scope')
    para('Software development is an operational process involving task allocation, cycle time, rework and quality control. AI may support this process while generating verification and debugging work. This study examines adoption and perceived benefits and frictions among employed professional developers, retaining Operations Management as the primary domain and statistical Data Analytics as the methodology.')
    para('The scope replaces the earlier OECD sector comparison for this revised report. It does not describe Chennai managers, all Indian employees or employer-level performance. OECD public aggregate analysis remains a separate earlier output. No datasets are pooled and no employer-worker linkage is inferred.')
    heading('1.1 Objectives and research questions',2)
    table(['Objective','Research question and model'],[
      ['1 Describe adoption','Among employed professional respondents, how is experience associated with current AI-tool adoption after adjustment? M1.'],
      ['2 Examine perceived productivity','Among current agent users, how is agent-use frequency associated with agreement that agents increased productivity? M2.'],
      ['3 Examine operational friction','Among current AI-tool users, how is frequency associated with selecting time-consuming debugging as a frustration? M3.'],
      ['4 Examine perceived task capability','Among current AI-tool users who provide a task-capability rating, how is frequency associated with a favourable rating? M4.'],
      ['5 Examine trust','Among current AI-tool users with a trust rating, how is frequency associated with trusting AI accuracy? M5.']])
    para('These objectives use questions actually present in this survey. Cost optimisation and managerial decision effectiveness are not measured as final outcomes in this revised study. They should not be presented as tested objectives.')
    page();heading('2 Evidence and conceptual framework')
    para('Stack Overflow’s methodology describes fieldwork from 29 May to 23 June 2025 and recruitment mainly through its own channels. Highly engaged users were more likely to encounter invitations. Its AI results page publishes question wording and descriptive findings on usage, trust, frustrations and agents. These publisher materials establish the measurement context, rather than validating causal effects.')
    para('The organising framework relates respondent work context and experience to adoption, then examines usage frequency alongside perceived benefits and frictions among users. Country and employer size are included as contextual adjustments. No causal pathway or mediation mechanism is identified. A favourable experience may encourage frequent use, frequent use may change perceptions, or both may reflect other factors.')
    para('Productivity agreement concerns perceived benefit. Debugging frustration concerns a selected problem, not measured rework minutes. Complex-task ratings concern perceived capability, not a task benchmark. Trust concerns confidence in AI output, not verified accuracy. These constructs are kept separate and are not combined into an operational-efficiency score.')
    para('The literature component in this revision is limited to the publisher’s evidence and statistical documentation. A broader peer-reviewed theoretical review and the institution’s preferred citation format remain for supervisor review. No claim of a complete systematic literature review is made.')
    page();heading('3 Methodology and measurement')
    heading('3.1 Source population and unit of analysis',2)
    para('Design: quantitative cross-sectional secondary analysis of publicly released respondent records. The unit is one survey respondent. Inclusion requires MainBranch = I am a developer by profession and Employment = Employed. Freelancers, students, hobbyists and other employment categories are outside the primary cohort. No probability weights are supplied or invented. Country means residence, not employer headquarters. Multiple respondents may share an employer; employer identifiers are unavailable.')
    table(['Cohort step','Records'],[['Public archive',f'{audit["source_rows"]:,}'],['Professional developers',f'{audit["professional_developers"]:,}'],['Employed professional cohort',f'{audit["employed_professional_cohort"]:,}'],['Current AI-tool users within cohort',f'{audit["current_tool_users_in_cohort"]:,}'],['Current AI-agent users within cohort',f'{audit["current_agent_users_in_cohort"]:,}']])
    para('The published methodology count is 49,009, which is 182 below the downloaded public archive. The archive SHA-256 is recorded in analysis.json. No rows are arbitrarily deleted to force agreement. Findings refer to the downloaded archive and our explicitly filtered cohorts. The discrepancy remains an unresolved provenance limitation.')
    heading('3.2 Outcomes and coding',2)
    table(['Model','Outcome equals 1','Outcome equals 0'],[
      ['M1','AISelect reports daily weekly or monthly/infrequent use','Either non-use response; planning is not adoption'],
      ['M2','Strongly or somewhat agree agents increased productivity','Neutral somewhat disagree or strongly disagree'],
      ['M3','Selects Debugging AI-generated code is more time-consuming','Answers frustration question without selecting this option'],
      ['M4','Very well or good but not great at complex tasks','Neutral bad or very poor rating'],
      ['M5','Highly trust or somewhat trust accuracy','Neutral somewhat distrust or highly distrust']])
    para('M2 reconstructs the productivity item from the five AIAgentImpact agreement columns using exact semicolon-delimited labels. Exactly one rating is required. This avoids treating a blank agreement cell as disagreement. M3 excludes a response selecting both no problems and another option; a missing question is never recoded zero. M4 excludes the combined no use for complex tasks / do not know option. Missing outcomes are excluded model by model. Binary coding simplifies original ordered responses and loses information; zero does not mean a measured absence of benefit. Planning, neutrality and nonresponse remain distinct in source counts.')
    page();heading('3.3 Predictors missingness and estimation',2)
    para('M1 compares work-experience categories: under 5 years (reference), 5–9, 10–19 and 20 or more. All models adjust for employer size: under 100 employees (reference), 100–999 and 1,000 or more. Country categories are United States (reference), Germany, India, United Kingdom, France and all other nonmissing countries pooled. These are the five most numerous countries in the full archive, not the OECD seven-country frame. Missing country is excluded rather than pooled. Organisation size I do not know, freelancer-only size, missing size and unavailable experience are excluded from complete-case models. Recorded experience outside 1–60 years is excluded as a covariate under a declared plausibility rule; zero cannot be inferred from blanks because the questionnaire instructed zero-experience respondents to leave it blank.')
    para('M2 uses agent frequency; M3–M5 use general AI-tool frequency. Each is categorical with monthly/infrequent as reference and weekly and daily contrasts. Restriction to current users is based on the relevant explicit usage question. No comparison of current agent users with nonusers can identify an agent-adoption effect on a user-only outcome. The primary M2 eligibility follows the agent-use answer even where another question is inconsistent; no unrecorded routing is assumed.')
    para('For each model log[p/(1−p)] = intercept + experience indicators + organisation-size indicators + country indicators + frequency indicators where applicable. Logistic maximum likelihood estimates odds ratios exp(beta). HC1 sandwich standard errors produce Wald 95% confidence intervals and p-values under independent-record assumptions. They do not correct voluntary sampling, common-method bias or unobserved employer clustering. All analyses are exploratory and chosen after inspecting survey variables, not preregistered.')
    para('Primary contrasts are 20+ versus under 5 years for M1 and daily versus monthly/infrequent use for M2–M5. Holm adjustment covers these five contrasts only. Other coefficients and the sensitivity fit remain exploratory; the confidence intervals are pointwise, not multiplicity-adjusted. No stepwise significance-based selection is performed. Complete cases assume missingness can be ignored conditional on the model, which is unverified and may bias estimates.')
    page();heading('4 Results and validation')
    heading('4.1 Model sample flow',2)
    table(['Model','Eligible','Outcome observed','Covariate exclusions','Final n','Outcome = 1'],[
      [m['name'].split('_')[0],f'{m["eligible_n"]:,}',f'{m["outcome_observed_n"]:,}',f'{m["covariate_excluded_n"]:,}',f'{m["n"]:,}',f'{m["events"]:,} ({m["event_percent"]:.1f}%)'] for m in models])
    para('Eligible denominators differ because adoption uses the employed cohort, productivity uses current agent users and the remaining models use current tool users. Outcome-observed counts precede complete-case adjustment. Event percentages above refer only to each final model sample and must not be described as population prevalence. Exclusion counts by covariate are stored in analysis.json and may overlap.')
    heading('4.2 Primary adjusted associations',2)
    table(['Model and comparison','Adjusted OR','95% CI','Holm p'],[
        [m['name'].split('_')[0]+' '+CONTRASTS[m['name']],f'{m["primary"]["odds_ratio"]:.2f}',
         f'{m["primary"]["ci_low"]:.2f} to {m["primary"]["ci_high"]:.2f}',pvalue(m['primary']['holm_p_five_primary_tests'])] for m in models])
    for m in models:
        r=m['primary'];direction='higher' if r['odds_ratio']>1 else 'lower'
        para(f'{m["name"].split("_")[0]} {LABELS[m["name"]]}: {CONTRASTS[m["name"]]} is associated with {direction} odds of the coded outcome, conditional on the included covariates (OR {r["odds_ratio"]:.2f}; 95% CI {r["ci_low"]:.2f}–{r["ci_high"]:.2f}; n={m["n"]:,}).')
    para('For M2, OR 8.00 means approximately eight times the adjusted odds of agreeing that agents increased productivity. It does not mean eight times the productivity, an eightfold probability or a causal improvement. Daily users may self-select because they already perceive benefits. M3 concerns odds of selecting one debugging complaint; it does not establish less debugging time.')
    heading('4.3 Diagnostics and sensitivity',2)
    table(['Model','Converged','Max VIF','Minority outcomes per parameter','In-sample AUC'],[
      [m['name'].split('_')[0],'Yes',f'{m["max_vif"]:.2f}',f'{m["minority_per_parameter"]:.1f}',f'{m["in_sample_auc"]:.3f}'] for m in models])
    para('All design matrices have full rank and coefficient estimates are finite. Each GLM fit agrees within 0.000001 with a separately fitted Logit likelihood implementation. No fitting warnings were accepted. Variance inflation factors are below 10 and minority outcomes exceed 10 per estimated parameter. Calibration-bin counts, observed proportions, fitted probabilities, Brier scores and McFadden pseudo-R² are saved with the results. These are in-sample diagnostics, not out-of-sample validation; adequate convergence is not evidence that omitted variables or selection bias are absent.')
    r=sensitivity['primary'];para(f'As a coding sensitivity check, M2 was refitted after excluding neutral productivity ratings. The daily versus monthly/infrequent OR was {r["odds_ratio"]:.2f} (95% CI {r["ci_low"]:.2f}–{r["ci_high"]:.2f}; n={sensitivity["n"]:,}), compared with 8.00 in the primary model. Direction is stable but magnitude depends materially on treatment of neutral responses. This sensitivity addresses coding only, not causality or missing-data bias.')
    para(f'Quality checks found no duplicate ResponseId values and {audit["contradictory_productivity_ratings"]} conflicting productivity ratings among eligible agent users. M3 excluded {audit["contradictory_no_frustration"]} contradictory no-problem selections. {audit["experience_over_60_excluded_as_covariate"]} employed professional records reported experience above 60 years and were treated as unavailable covariates. No imputation, fabricated participants or reconstructed OECD records were used.')
    page();heading('5 Discussion recommendations and limitations')
    para('The results connect frequent AI use with more favourable reported capability and trust, and frequent agent use with productivity agreement. These patterns can reflect learning, task suitability, selection and reverse causation. The experience contrast in adoption shows heterogeneity within the respondent cohort, not evidence that experienced employees resist innovation. The debugging association is specific to one reported complaint and should not be generalised to total operational cost or quality.')
    heading('5.1 Managerial implications',2)
    para('Managers can use the survey patterns to formulate local pilot questions. Begin with bounded tasks, define human-review responsibility and record actual completion time, rework, defects and acceptance quality before and during a pilot. Compare similar tasks and account for task complexity. Provide training in verification, prompt use and handling sensitive information. Assess who benefits and who incurs additional review work. These are recommendations for future evaluation, not interventions tested by this cross-sectional survey.')
    heading('5.2 Limitations',2)
    for text in [
      'Voluntary developer recruitment prevents representative inference to all developers, India, Chennai managers or firms. Country pooling masks differences and no employer-level clusters can be identified.',
      'Cross-sectional self-reports do not determine temporal direction. Frequency and positive perceptions may influence each other. Task mix, skill, employer policy and other unmeasured factors can confound associations.',
      'Question-specific nonresponse and complete-case exclusion can select respondents. Missing experience may include zero-experience respondents because of questionnaire instructions. No imputation resolves this ambiguity.',
      'Dichotomising ordered ratings changes interpretation. The sensitivity model illustrates dependence on neutral-response handling. Robust errors do not repair sample-selection bias.',
      'The public-archive count differs from the published count by 182 records. The reason remains unverified. No exact replication claim is made.',
      'The analysis does not measure objective output, monetary savings, causal effects, verified code quality or managerial decision effectiveness. Model diagnostics are internal; no predictive deployment or external validation is claimed.',
      'The revised research scope, academic literature coverage, format and unsigned front matter still require supervisor review.'
    ]:para(text)
    heading('5.3 Conclusion',2)
    para('The public survey supports a reproducible exploratory study of AI adoption and developer perceptions using genuine respondent records. Five fitted models answer five revised questions. Associations are suitable for discussion of workflow adoption, verification and perceived benefit, with explicit limits on generalisation and causality. OECD approval is not required for this independent dataset; acceptance of the revised dissertation scope remains an academic decision.')
    page();heading('6 References')
    for description,url in REFS:
        para(description+' '+url)
    page();heading('Appendices and reproducibility')
    heading('A Questionnaire and coding',2)
    para('The project reuses the publisher’s questionnaire. It does not claim a newly administered or locally validated questionnaire. questionnaire_extract.csv records the exact question wording and source variable names. Outcome coding is specified in Section 3.2; organisation and experience mappings and country categories are explicit in stackoverflow_analysis.py. Full source question files are available from the referenced public archive.')
    heading('B Output files',2)
    table(['File','Purpose'],[['analysis.json','Source hashes cohort counts missingness model diagnostics and sensitivity'],['primary_results.csv','Five primary contrasts with confidence intervals and raw and Holm p-values'],['M1 to M5 coefficients.csv','All model coefficients including adjustment variables'],['M1 to M5 model_rows.csv','Source ResponseId coded outcome and fitted probability for audit'],['M1 to M5 calibration.csv','In-sample calibration bins'],['descriptive_counts.csv','Question frequencies with explicit cohort denominators'],['questionnaire_extract.csv','Publisher question wording for the selected variables']])
    heading('C Rerunning the analysis',2)
    repository_link()
    para('Install the versions in requirements-stackoverflow.txt in an isolated Python environment. Download results.csv and schema.csv from the official archive using scripts/download_stackoverflow.py. Run python stackoverflow_analysis.py --data work/stackoverflow_2025/results.csv --schema work/stackoverflow_2025/schema.csv. Run python -m unittest discover -s tests -p test_stackoverflow_analysis.py. To regenerate this revised report run python scripts/build_stackoverflow_report.py --template outputs/stackoverflow2025/AI_Use_at_Work_Regression_Report.docx. The delivered DOCX can itself supply the page styles for a rerun, so the original private draft is not required. Output location: outputs/stackoverflow2025. The analysis rejects changed source hashes until reviewed. Word or another compatible renderer is needed to export the DOCX to PDF.')
    heading('D Validation and external inputs',2)
    table(['Component','Status'],[['Title objectives scope','Revised consistently for employed professional developers; supervisor acceptance pending'],['Variables and source questionnaire','Mapped to actual public survey fields; no primary survey claimed'],['Sampling','Voluntary survey and complete-case cohorts explicitly documented'],['Statistical methods','Five fitted logistic models robust intervals sensitivity and diagnostics complete'],['Interpretation','Associational self-report limits retained throughout'],['Institutional submission','Guide approval signatures formatting and literature expectations require confirmation']])
    para('Source archive SHA-256: '+audit['source_sha256'])
    para('Source schema SHA-256: '+audit['schema_sha256'])
    para('Database attribution: Stack Overflow Developer Survey 2025, Stack Exchange. Data licensed under ODbL 1.0; contents under DbCL 1.0 as identified by the publisher. Retain attribution and licence notices when reusing the database or adapted extracts. Public download does not remove applicable licence obligations.')
    dest=out/'AI_Use_at_Work_Regression_Report.docx';doc.save(dest)
    contents=''.join(body)
    navigation='<nav>'+''.join('<a href="#section-'+str(i)+'">'+html.escape(part.split('>',1)[1].split('</',1)[0])+'</a> ' for i,part in enumerate(body) if part.startswith('<h2 '))+'</nav>'
    (out/'AI_Use_at_Work_Regression_Report.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+TITLE+'</title><style>body{font:17px/1.6 Georgia,serif;max-width:1000px;margin:30px auto;padding:0 20px;color:#17212b}h1,h2,h3{line-height:1.25}nav{display:flex;flex-wrap:wrap;gap:12px;font:14px Arial}.table{overflow:auto}table{border-collapse:collapse;width:100%;font:14px/1.4 Arial;margin:20px 0}th,td{border:1px solid #ccd2d8;padding:10px;text-align:left}th{background:#dde6ef}tr:nth-child(even){background:#f5f5f5}p{overflow-wrap:anywhere}@media print{nav{display:none}h2{break-before:page}tr{break-inside:avoid}}</style>'+navigation+contents+'</html>',encoding='utf-8')
    (out/'README.md').write_text('''# Stack Overflow regression analysis

Public VIT project repository: https://github.com/saisri132000/mba-ai-operational-efficiency

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
''',encoding='utf-8')
    print(dest.resolve())


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--template',type=Path,required=True)
    args=parser.parse_args()
    build(Path(__file__).resolve().parents[1],args.template)
