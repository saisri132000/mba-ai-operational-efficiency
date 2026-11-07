"""Rebuild the secondary-data submission package from unchanged OECD sources."""
from pathlib import Path
import argparse, csv, hashlib, html, json, re
import openpyxl
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.graphics.shapes import Drawing, Rect, String

TITLE = 'Workplace AI Adoption, Perceived Performance and Implementation Barriers'
SUBTITLE = 'A Comparative Secondary Analysis of OECD Employer and Worker Surveys'
DOI = 'https://doi.org/10.1787/ea0a0fe1-en'
REFERENCES = f'''# References

Lane, M., Williams, M., & Broecke, S. (2023). *The impact of AI on the workplace: Main findings from the OECD AI surveys of employers and workers*. OECD Social, Employment and Migration Working Papers, No. 288. OECD Publishing. {DOI}

OECD. (2023). *AI report main findings: Employers and workers surveys graphs* [Supplementary Excel tables accompanying Lane, Williams, and Broecke (2023)]. Supplied public workbook; the original file is retained in sources/. Individual worksheets and cell addresses are recorded in results/observations.csv. The fieldwork took place in 2022; publication occurred in 2023.

The report and supplementary workbook are the evidence sources for this secondary analysis. No additional literature is represented as having been reviewed. Consult the original report's bibliography for wider literature; those entries are not automatically citations of this project.
'''

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def verify_sources(root):
    manifest_path = root/'sources/source_manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    required = {'OECD_2023_report.pdf', 'OECD_published_tables.xlsx'}
    if set(manifest) != required:
        raise ValueError('Source manifest must list exactly the two approved OECD inputs')
    for name, expected in manifest.items():
        if sha(root/'sources'/name) != expected:
            raise ValueError(f'Source checksum mismatch: {name}; do not rewrite the manifest to bypass review')
    return manifest


def build(root):
    root = Path(root).resolve()
    verify_sources(root)
    for folder in ('report','results','figures','references','explanation'):
        (root/folder).mkdir(parents=True, exist_ok=True)
    wb = openpyxl.load_workbook(root/'sources/OECD_published_tables.xlsx', data_only=True)
    records, checks, summaries = [], [], []
    def group(metric, sector, sheet, cells, labels, n, distribution=True):
        values = []
        for cell,label in zip(cells,labels):
            v = wb[sheet][cell].value
            if not isinstance(v,(int,float)) or not 0 <= v <= 1:
                raise ValueError(f'Invalid proportion: {sheet}!{cell}: {v}')
            values.append(v)
            records.append(dict(metric=metric,sector=sector,response=label,raw_proportion=v,
                                percentage=round(v*100,4),source_sheet=sheet,source_cell=cell,
                                unweighted_source_subgroup_n=n))
        if distribution:
            total = sum(values)
            checks.append(dict(metric=metric,sector=sector,total=round(total,6),
                               status='PASS' if abs(total-1)<=.002 else 'EXCLUDED: inconsistent source total'))
            if abs(total-1)>.002 and metric!='Staff-cost motivation':
                raise ValueError(f'Unexpected source inconsistency: {metric} {sector}')
        return values
    def pair(metric, sheet, fin, man, labels, nf, nm, positive):
        fv=group(metric,'Finance and insurance',sheet,fin,labels,nf)
        mv=group(metric,'Manufacturing',sheet,man,labels,nm)
        f=sum(fv[i] for i in positive)*100; m=sum(mv[i] for i in positive)*100
        difference=round(m-f,2)
        if difference==0:
            difference=0.0
        summaries.append(dict(metric=metric,finance_percent=round(f,2),manufacturing_percent=round(m,2),
                              manufacturing_minus_finance_pp=difference,source_sheet=sheet))
    pair('Employer AI adoption','Figure 2_1',['F31','F32','F33'],['F39','F40','F41'],['Yes','No','Do not know'],653,1400,[0])
    pair('Employer perceived productivity: positive','Figure 3_2',['B33','B34','B35','B36'],['B42','B43','B44','B45'],['Positive','No effect','Negative','Do not know'],291,452,[0])
    pair('Worker perceived performance: improved','Figure 3_3',[f'B{r}' for r in range(32,38)],[f'B{r}' for r in range(43,49)],['Improved a lot','Improved a little','No effect','Worsened a little','Worsened a lot','Do not know'],1231,912,[0,1])
    pair('Worker task pace: increased','Figure 5_6',[f'C{r}' for r in range(40,46)],[f'B{r}' for r in range(40,46)],['Decreased a lot','Decreased a little','No effect','Increased a little','Increased a lot','Do not know'],1231,912,[3,4])
    pair('Worker task control: increased','Figure 5_6',[f'G{r}' for r in range(40,46)],[f'F{r}' for r in range(40,46)],['Decreased a lot','Decreased a little','No effect','Increased a little','Increased a lot','Do not know'],1231,912,[3,4])
    pair('Workers receiving decision assistance','Figure 5_8',['C33','C34','C35'],['B33','B34','B35'],['Yes','No','Do not know'],1231,912,[0])
    for metric,col in [('Decision quality: agreement','B'),('Decision enjoyment: agreement','C'),('Decision speed: agreement','D')]:
        pair(metric,'Figure 5_9',[f'{col}{r}' for r in range(43,49)],[f'{col}{r}' for r in range(55,61)],['Strongly agree','Somewhat agree','Somewhat disagree','Strongly disagree','Neither','Do not know'],883,558,[0,1])
    for metric,col in [('High-cost barrier','F'),('Skills barrier','E'),('Not convinced of benefits','D'),('Government-regulation barrier','C')]:
        pair(metric,'Figure 8_7',[f'{col}{r}' for r in (40,41,42)],[f'{col}{r}' for r in (48,49,50)],['Yes','No','Do not know'],653,1400,[0])
    for sector,row,n in [('Finance and insurance',32,291),('Manufacturing',40,452)]:
        group('Staff-cost motivation',sector,'Figure 3_1',[f'C{r}' for r in (row,row+1,row+2)],['Yes','No','Do not know'],n)
    tasks=[]
    for metric,fin,man in [('Task automation','A24','D24'),('Task creation','B24','E24'),('Both automation and creation','C24','F24')]:
        f=group(metric,'Finance and insurance','Figure 5_1',[fin],['Reported'],291,False)[0]*100
        m=group(metric,'Manufacturing','Figure 5_1',[man],['Reported'],452,False)[0]*100
        row=dict(metric=metric,finance_percent=round(f,2),manufacturing_percent=round(m,2),manufacturing_minus_finance_pp=round(m-f,2),source_sheet='Figure 5_1')
        tasks.append(row); summaries.append(row)
    sizes=[]
    for col,size in zip('BCDE',['20-49 employees','50-249 employees','250-499 employees','500+ employees']):
        f=group('AI adoption: '+size,'Finance and insurance','Figure 2_1',[f'{col}{r}' for r in (31,32,33)],['Yes','No','Do not know'],wb['Figure 2_1'][f'{col}35'].value)[0]*100
        m=group('AI adoption: '+size,'Manufacturing','Figure 2_1',[f'{col}{r}' for r in (39,40,41)],['Yes','No','Do not know'],wb['Figure 2_1'][f'{col}43'].value)[0]*100
        sizes.append(dict(metric=size,finance_percent=round(f,2),manufacturing_percent=round(m,2),manufacturing_minus_finance_pp=round(m-f,2),source_sheet='Figure 2_1'))
    wb.close()
    def write_csv(name,rows):
        with (root/'results'/name).open('w',encoding='utf-8',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    write_csv('observations.csv',records);write_csv('sector_comparisons.csv',summaries);write_csv('adoption_by_firm_size.csv',sizes)
    quality={'checks':checks,'rounding_tolerance_proportion':.002,'known_issue':'Figure 3_1 finance staff-cost motivation answers sum to 0.94; excluded from comparative conclusions. Source retained unchanged. No renormalization or inferred missing respondents.',
             'scope':'Published weighted aggregates, not individual respondent records. No new causal or inferential estimates.'}
    (root/'results/data_quality.json').write_text(json.dumps(quality,indent=2),encoding='utf-8')
    (root/'results/analysis.json').write_text(json.dumps({'sector_comparisons':summaries,'firm_sizes':sizes},indent=2),encoding='utf-8')
    def mdtable(rows):
        out=['| Indicator | Finance (%) | Manufacturing (%) | Difference (pp) |','|---|---:|---:|---:|']
        out += [f"| {r['metric']} | {r['finance_percent']:.2f} | {r['manufacturing_percent']:.2f} | {r['manufacturing_minus_finance_pp']:+.2f} |" for r in rows]
        return '\n'.join(out)
    chart_specs=[('adoption', 'AI adoption by firm size',sizes),('performance','Perceived performance',summaries[1:3]),('tasks','Task changes reported by AI-adopting employers',tasks),('decisions','Agreement among workers receiving AI decision assistance',summaries[6:9])]
    drawings={}
    for name,title,rows in chart_specs:
        height=65+len(rows)*70;d=Drawing(480,height)
        svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="780" height="{height}" viewBox="0 0 780 {height}">','<rect width="100%" height="100%" fill="white"/>',f'<text x="10" y="20" font-family="Arial" font-size="14">{html.escape(title)}</text>']
        d.add(String(0,height-15,title,fontName='Helvetica-Bold',fontSize=10))
        for i,r in enumerate(rows):
            y=45+i*70; label=r['metric']
            svg.append(f'<text x="10" y="{y}" font-family="Arial" font-size="12">{html.escape(label)}</text>')
            d.add(String(0,height-y,label,fontSize=8))
            for j,(field,color,sector) in enumerate([('finance_percent','#14577a','Finance'),('manufacturing_percent','#c56822','Manufacturing')]):
                v=r[field];yy=y+8+j*18
                svg += [f'<rect x="120" y="{yy}" width="{v*5}" height="12" fill="{color}"/>',f'<text x="10" y="{yy+10}" font-family="Arial" font-size="11">{sector}</text>',f'<text x="{126+v*5}" y="{yy+10}" font-family="Arial" font-size="11">{v:.2f}%</text>']
                d.add(String(0,height-yy-10,sector,fontSize=7));d.add(Rect(85,height-yy-12,v*3,10,fillColor=colors.HexColor(color),strokeColor=None));d.add(String(90+v*3,height-yy-10,f'{v:.2f}%',fontSize=7))
        svg.append(f'<text x="120" y="{height-5}" font-family="Arial" font-size="10">Bar length: 0 to 100 percent; OECD weighted estimates.</text></svg>')
        (root/f'figures/{name}.svg').write_text('\n'.join(svg),encoding='utf-8');drawings[name]=d
    report=f'''# {TITLE}
## {SUBTITLE}

MBA research project | Primary domain: Operations Management | Methodology: descriptive secondary-data analysis

Evidence: OECD survey fieldwork in 2022, report and supplementary tables published in 2023. This package contains completed descriptive analysis of published aggregates. It does not claim institutional approval, primary questionnaire collection, or a Chennai sample.

## Abstract

This project examines artificial intelligence adoption and perceived workplace performance using published OECD employer and worker survey tables. It considers adoption, productivity perceptions, task changes, decision assistance, and implementation barriers in finance and insurance and manufacturing across seven OECD countries. The method extracts weighted proportions from specified spreadsheet cells, checks response distributions, computes percentages and percentage-point differences, and produces reproducible tables and figures. Employer AI adoption is 41.7% in finance and insurance and 29.0% in manufacturing. Among AI-adopting employers, 56.7% and 62.6%, respectively, report positive productivity effects. Among AI-using workers, 79.3% and 79.8% report improved own performance. Workers receiving decision assistance generally report better and faster decisions. These are reported perceptions and descriptive comparisons; they do not demonstrate causation or measured financial returns. A source inconsistency in a finance staff-cost motivation item is disclosed and excluded from comparison. Recommendations emphasize bounded pilots, worker training, human oversight, and measurement of actual operational outcomes. The completed secondary analysis cannot establish findings about Chennai IT/IT-enabled services.

## Chapter 1. Introduction and research scope

### 1.1 Operational problem

AI can change how organizations allocate work, automate tasks, and support decisions. Operations managers need to judge whether these changes improve output quality and timeliness, create new work, or introduce additional costs and risks. Adoption alone is insufficient evidence of success. This study examines what surveyed employers and workers report, while separating these perceptions from independently measured efficiency.

### 1.2 Scope and design change

The original project proposed a primary questionnaire among managers or team leads in Chennai IT/IT-enabled services. Genuine responses and reviewed recruitment arrangements were unavailable. This completed report therefore adopts an explicit secondary-data design, using the OECD sources supplied for this project. It changes the population and measurement framework; it does not retrofit OECD percentages into the Chennai questionnaire. The original primary-survey software remains a separate possible future study.

The source study covers Austria, Canada, France, Germany, Ireland, the United Kingdom, and the United States, in finance and insurance and manufacturing. Employer firms have at least 20 employees. The source reports 2,053 firms and 5,334 workers overall. The present analysis selects published estimates, not individual records. Employer and worker observations are different populations and are not paired.

### 1.3 Objectives and research questions

O1 / RQ1: Describe how published AI adoption estimates differ by sector and firm size.

O2 / RQ2: Describe employers' productivity perceptions and workers' own performance perceptions among the relevant AI-adopting/using subgroups.

O3 / RQ3: Describe reported task automation, task creation, pace, and control associated with workplace AI use.

O4 / RQ4: Describe the prevalence of decision assistance and perceived decision quality, enjoyment, and speed among workers receiving it.

O5 / RQ5: Describe published adoption barriers, particularly cost and skills, without interpreting them as realized cost savings.

These questions are descriptive. No causal hypothesis or respondent-level association is tested with the aggregate workbook.

## Chapter 2. Evidence and conceptual framework

### 2.1 Evidence base

Lane, Williams, and Broecke (2023) report employer and worker surveys about AI adoption, workplace effects, and attitudes. Their supplementary OECD workbook supplies the quantitative inputs used here. The original report contains the survey methodology, question wording, figures, and wider bibliography. This project relies on those two supplied sources rather than claiming a new comprehensive systematic literature review.

### 2.2 Operational framework

The framework connects AI adoption with reported productivity, changes to tasks, and decision support, with cost and skill constraints affecting implementation. This is a conceptual organizing framework, not an estimated causal model. Productivity, own performance, task pace, task control, and decision speed are distinct measures. They are not combined into an invented operational-efficiency score. Employer perceptions and worker perceptions are presented separately.

Realized cost optimization would require actual expense, output, and rework measurements with an appropriate comparison. The workbook's cost-barrier and motivation items do not supply those measurements. Faster task pace can also indicate work intensification and should not automatically be treated as a benefit.

## Chapter 3. Methodology

### 3.1 Research design, population, and unit

This is a quantitative descriptive secondary analysis of published cross-sectional survey aggregates. The original OECD researchers performed recruitment and weighting. This project did not recruit participants, administer a questionnaire, or determine the original sample. The analytical unit is a published sector or firm-size estimate with its documented source question and subgroup, rather than a new individual respondent.

### 3.2 Inclusion and exclusion

Included estimates have a numeric proportion in [0,1], identifiable sector and response category, clear figure provenance, and a relevant operational research question. Selected sources are Figures 2.1, 3.2, 3.3, 5.1, 5.6, 5.8, 5.9, and 8.7. Figure 3.1 is inspected for a cost-item quality check. Detailed application subcategories and other unselected figures are outside this analysis.

The finance staff-cost motivation distribution in Figure 3.1 sums to 94%, despite its displayed total of 100%. It is retained in the audit data but excluded from comparative findings. Values are not normalized and the unexplained remainder is not assigned to an answer category. Source files remain unchanged.

### 3.3 Denominators and measurement

AI adoption and barriers use all surveyed employers: finance n=653 and manufacturing n=1,400. Employer productivity and task changes refer to AI-adopting employers: n=291 and n=452. Worker performance, pace, control, and decision-assistance prevalence refer to AI-using workers: finance n=1,231 and manufacturing n=912. Decision-quality, enjoyment, and speed agreement refer to assisted workers: n=883 and n=558. These are source unweighted subgroup sizes, not reconstructed response counts. Percentages use the source's weighted estimates.

### 3.4 Extraction, cleaning, and analysis

The reproducible script reads the supplied workbook without editing it. Each extracted category records the sheet, cell, source proportion, transformed percentage, and subgroup size. Complete response distributions are checked against 100%, permitting a 0.2 percentage-point rounding tolerance. Multiple-response task indicators are kept separate because automation and task creation can overlap. 'Do not know' is retained; it is not converted into missing data or a negative answer.

Percentage = source proportion multiplied by 100. Improved worker performance sums 'improved a lot' and 'improved a little'. Decision agreement sums 'strongly agree' and 'somewhat agree'. Increased pace or control sums its two increase categories. A sector difference is manufacturing percentage minus finance percentage, expressed in percentage points. It is not a percentage change and is not a significance test.

No respondent imputation, duplicate deletion, new reliability coefficient, regression, correlation, p-value, or confidence interval is produced. Such analyses would require compatible individual data and survey-design information. File hashes identify the original inputs; validation diagnostics remain available separately from conclusions.

### 3.5 Ethics and reproducibility

The package uses published aggregate tables and contains no individual respondent records. It neither claims new participant consent nor invents ethics approval. Original OECD authorship and sources are acknowledged. Institutional acceptance of the secondary-data design and local formatting requirements must be confirmed externally. The report, extraction code, charts, and audit outputs can be rebuilt from the packaged source workbook. The same Python pipeline is callable from the included Databricks notebook; platform execution does not change the evidence or analysis. Live cloud execution requires an actual workspace and is not certified by local tests.

## Chapter 4. Results

### 4.1 AI adoption

Table 1. Published adoption estimates by firm size; source Figure 2.1. Sector totals are 41.70% finance and insurance and 29.00% manufacturing.

{mdtable(sizes)}

![AI adoption by firm size](../figures/adoption.svg)

Adoption is higher in finance in every displayed size band. The manufacturing estimate increases across the size bands. Finance does not increase monotonically: its 500+ employee estimate is lower than its 250-499 estimate. These patterns are descriptive and do not establish that firm size causes adoption.

### 4.2 Perceived performance and productivity

Table 2. Positive employer productivity and improved worker performance; Figures 3.2 and 3.3. The populations differ and must not be averaged into one metric.

{mdtable(summaries[1:3])}

![Perceived performance](../figures/performance.svg)

Among AI-adopting employers, manufacturing's positive productivity estimate exceeds finance by 5.90 percentage points. Worker improvement estimates are similar, differing by 0.50 points. These are perceptions reported in separate surveys; they are not measured productivity gains or proof of comparable benefits for all firms.

### 4.3 Task changes and work organization

Table 3. AI-adopting employers reporting task changes; Figure 5.1. Categories overlap.

{mdtable(tasks)}

![Task changes](../figures/tasks.svg)

Automation and task creation coexist. 'Both' is an overlapping subgroup and must not be added to automation and creation to obtain a total. These indicators describe whether changes were reported, not how many jobs were removed or how much working time was saved.

Table 4. AI-using workers reporting increased task pace and control; Figure 5.6.

{mdtable(summaries[3:5])}

More workers report increased pace than increased control in both sectors. The measures concern different questions and may overlap at individual level, which the workbook cannot reconstruct. Increased pace can reflect faster execution or intensified work; the aggregate evidence cannot distinguish these explanations.

### 4.4 Decision assistance

Among AI-using workers, 69.70% in finance and 56.20% in manufacturing report AI assistance with decisions (Figure 5.8). Table 5 uses only workers receiving that assistance, not all workers.

{mdtable(summaries[6:9])}

![Decision assistance perceptions](../figures/decisions.svg)

Agreement that assistance improves decision quality is 81.90% in both sectors. Agreement about faster decisions is 84.60% in finance and 86.40% in manufacturing. These self-reports do not test actual decision accuracy, error rates, or completion time.

### 4.5 Implementation barriers

Table 6. Employers reporting each barrier; Figure 8.7. Responses can overlap across barrier categories.

{mdtable(summaries[9:13])}

High costs are the most frequently reported of the four selected barriers in both sectors, followed by lack of relevant skills. A cost barrier indicates a perceived implementation obstacle, not the amount spent or a realized return on investment. The inconsistent finance staff-cost motivation item is not used to claim savings.

## Chapter 5. Discussion, conclusion, and recommendations

### 5.1 Interpretation against the research questions

RQ1 finds sector and firm-size differences in reported adoption. RQ2 finds predominantly positive performance perceptions among selected AI users and adopters. RQ3 finds simultaneous automation and creation of tasks, alongside increased pace and control. RQ4 finds widespread favorable perceptions among decision-assisted workers. RQ5 identifies cost and skills as salient barriers in the selected published estimates.

Together, the findings support examining AI as an operational change involving technology, work design, and people. They do not establish that AI alone produced the reported improvements. Adopting organizations may already differ from non-adopters; users may be selected into different tasks; and reported experiences may depend on implementation quality. Aggregated sector comparisons cannot adjust for these factors.

### 5.2 Managerial recommendations

Begin with a specific operational problem and a bounded pilot. Measure baseline and subsequent cycle time, error rate, rework, cost per completed transaction, and service quality using the same definitions. Include training, integration, oversight, and maintenance in cost evaluation. These are proposed management practices, not outcomes demonstrated by this study.

Retain human review for consequential decisions and define escalation responsibilities. Track decision correctness and time separately, because speed alone does not establish quality. Review worker feedback and workload as well as output. Where increased pace occurs, check whether workers also have sufficient control, support, and time to verify AI output. Treat skill development as part of implementation rather than assuming software purchase is sufficient.

### 5.3 Limitations

The data concern 2022 workplace AI and precede much of the later generative-AI expansion. Results should not be described as a current adoption census. The seven countries and two sectors do not represent India or Chennai IT/IT-enabled services. The source design and weighting restrict generalization; this reanalysis cannot remove original survey limitations.

Published aggregates cannot support individual-level relationships, reliability analysis, or independent causal identification. Employer and worker results use different denominators. Favorable self-reports may be affected by recall, selection, and other reporting biases. No objective cost savings, long-term productivity change, or firm-level return is measured here. One source inconsistency is explicitly excluded. No new precision estimates or significance claims are made.

### 5.4 Conclusion and future research

The completed secondary analysis shows substantial favorable performance and decision-support perceptions among surveyed AI adopters/users, alongside overlapping task changes and implementation barriers. Its contribution is a transparent operational interpretation and reproducible extraction of genuine published evidence. It provides a basis for management questions and future measurement, rather than causal proof or a Chennai-specific conclusion.

A future Chennai study would need institutionally accepted scope, reviewed questionnaire and recruitment arrangements, genuine eligible responses, and an analysis plan suited to those measurements. Alternatively, approved access to compatible OECD microdata could enable a more detailed secondary analysis with appropriate survey-design methods. Neither extension is claimed as completed here.

## Appendix A. Instrument and objective alignment

| Research question | Source measurement | Output |
|---|---|---|
| RQ1 | AI adoption by sector and firm size, Figure 2.1 | Table 1 and adoption chart |
| RQ2 | Employer productivity, Figure 3.2; worker own performance, Figure 3.3 | Table 2 and performance chart |
| RQ3 | Task automation/creation, Figure 5.1; pace/control, Figure 5.6 | Tables 3-4 and task chart |
| RQ4 | Decision assistance, Figure 5.8; agreement, Figure 5.9 | Table 5 and decision chart |
| RQ5 | Adoption barriers, Figure 8.7 | Table 6 |

No new questionnaire was administered. The original OECD report packaged in sources/ contains the source survey instruments and wording in its annexes. Cell-level extraction is documented in results/observations.csv. The earlier Chennai questionnaire is not the instrument used for these results.

## Appendix B. Data dictionary and validation status

observations.csv contains metric, sector, response, raw_proportion, percentage, source_sheet, source_cell, and unweighted_source_subgroup_n. Each row is a published estimate, not a person. Values use UTF-8 CSV with a header; percentages are not response counts. sector_comparisons.csv reports selected composite percentages and manufacturing-minus-finance percentage-point differences. adoption_by_firm_size.csv contains the size comparisons. analysis.json mirrors calculated summaries; data_quality.json lists distribution checks and the excluded cost item.

Title and scope: internally aligned with the secondary design. Variables: kept distinct and linked to source measures. Questionnaire: original source instrument; no new local validation claimed. Sampling: source study's design; no new participant recruitment. Statistical methods: descriptive calculations verified against worksheet cells. Interpretation: limited to weighted published perceptions and comparisons. Institutional acceptance and formatting: external confirmation still required.

## Appendix C. Reproducibility and submission inputs

Extract the ZIP, install requirements.txt, and run python build_report.py from its root. Generated deliverables are report/PROJECT_REPORT.pdf, report/PROJECT_REPORT.html, report/PROJECT_REPORT.md, results/, and figures/. README.md gives exact commands. sources/source_manifest.json records input SHA-256 hashes. The package includes the genuine aggregate data needed for this analysis; individual microdata is not required for these descriptive outputs.

Before institutional submission, obtain confirmation that the secondary-data design is acceptable and apply required identity details, declarations, signatures, and formatting supplied by the institution. No approval, supervisor signature, or certification is fabricated. New primary data would require a separate design and cannot simply be inserted into this aggregate analysis.

{REFERENCES}
'''
    (root/'report/PROJECT_REPORT.md').write_text(report.rstrip()+'\n',encoding='utf-8')
    (root/'references/REFERENCES.md').write_text(REFERENCES,encoding='utf-8')
    # Markdown package is optional: the HTML converter below uses only the standard library.
    styles=getSampleStyleSheet();styles['Normal'].fontSize=10;styles['Normal'].leading=14;styles['Normal'].spaceAfter=7
    styles['Heading1'].fontSize=17;styles['Heading1'].leading=21;styles['Heading2'].fontSize=14;styles['Heading2'].leading=18
    def inline(text):
        text=html.escape(text)
        text=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',text)
        text=re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)',r'<i>\1</i>',text)
        return text
    def blocks(text):
        lines=text.splitlines();i=0
        while i<len(lines):
            s=lines[i].strip()
            if not s:i+=1;continue
            if s.startswith('|'):
                rows=[]
                while i<len(lines) and lines[i].strip().startswith('|'):
                    row=[c.strip() for c in lines[i].strip().strip('|').split('|')]
                    if not all(re.fullmatch(r'[-: ]+',c) for c in row):rows.append(row)
                    i+=1
                yield 'table',rows;continue
            if s.startswith('!['):
                yield 'image',re.search(r'\((.*?)\)',s).group(1);i+=1;continue
            if s.startswith('#'):
                level=len(s)-len(s.lstrip('#'));yield f'h{level}',s[level:].strip();i+=1;continue
            para=[s];i+=1
            while i<len(lines) and lines[i].strip() and not lines[i].startswith(('#','|','![')):
                para.append(lines[i].strip());i+=1
            yield 'p',' '.join(para)
    story=[];out=[];toc=[]
    for typ,value in blocks(report):
        if typ.startswith('h'):
            anchor='section-'+str(len(toc));toc.append((anchor,value,typ))
            out.append(f'<{typ} id="{anchor}">{inline(value)}</{typ}>')
            style='Title' if typ=='h1' else 'Heading1' if typ=='h2' else 'Heading2'
            story.append(Paragraph(inline(value),styles[style]))
        elif typ=='p':
            out.append('<p>'+inline(value)+'</p>');story.append(Paragraph(inline(value),styles['Normal']))
        elif typ=='table':
            out.append('<table>'+''.join('<tr>'+''.join(f'<{"th" if j==0 else "td"}>{inline(c)}</{"th" if j==0 else "td"}>' for c in row)+'</tr>' for j,row in enumerate(value))+'</table>')
            widths=[245,80,90,80] if len(value[0])==4 else [75,270,150]
            data=[[Paragraph(inline(c),styles['Normal']) for c in row] for row in value]
            tab=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT');tab.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e8f0f5')),('GRID',(0,0),(-1,-1),.4,colors.HexColor('#bdcbd2')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5)]));story += [tab,Spacer(1,12)]
        else:
            out.append(f'<img src="{html.escape(value)}" alt="OECD sector comparison chart">');story += [drawings[Path(value).stem],Spacer(1,12)]
    nav=''.join(f'<li><a href="#{a}">{html.escape(v)}</a></li>' for a,v,t in toc if t=='h2')
    page=f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{TITLE}</title><style>body{{max-width:1000px;margin:30px auto;padding:0 22px;font:16px/1.65 Arial;color:#182a35}}h1,h2,h3{{color:#14577a;line-height:1.25}}h2{{border-bottom:1px solid #b7cbd7;padding-top:25px}}table{{border-collapse:collapse;width:100%;font-size:14px;margin:18px 0}}td,th{{border:1px solid #bacbd5;padding:9px;text-align:left}}th{{background:#e8f0f5}}img{{max-width:100%;height:auto}}a{{color:#14577a}}@media print{{nav{{display:none}}body{{margin:0}}}}</style><nav><h2>Contents</h2><ul>{nav}</ul></nav>'+''.join(out)+'</html>'
    # Link the original OECD report in HTML.
    page=page.replace(DOI,f'<a href="{DOI}">{DOI}</a>')
    (root/'report/PROJECT_REPORT.html').write_text(page,encoding='utf-8')
    def footer(canvas,doc):
        canvas.setFont('Helvetica',8);canvas.setFillColor(colors.HexColor('#50616a'))
        canvas.drawString(42,25,'OECD published aggregates | Descriptive secondary analysis')
        canvas.drawRightString(A4[0]-42,25,str(doc.page))
    SimpleDocTemplate(str(root/'report/PROJECT_REPORT.pdf'),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=42,bottomMargin=42,title=TITLE,author='MBA research project').build(story,onFirstPage=footer,onLaterPages=footer)
    guide='''# Project explanation and viva guide

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
'''
    (root/'explanation/PROJECT_EXPLANATION.md').write_text(guide,encoding='utf-8')
    guide_html=[]
    for typ,value in blocks(guide):
        if typ.startswith('h'):
            guide_html.append(f'<{typ}>{inline(value)}</{typ}>')
        elif typ=='p':
            guide_html.append('<p>'+inline(value)+'</p>')
    (root/'explanation/PROJECT_EXPLANATION.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Project explanation and viva guide</title><style>body{max-width:850px;margin:30px auto;padding:0 20px;font:17px/1.65 Arial;color:#182a35}h1,h2{color:#14577a}</style>'+''.join(guide_html)+'</html>',encoding='utf-8')
    summary=guide.split('## 350-400 word explanation\n\n')[1].split('\n\n## Five-minute')[0]
    count=len(summary.split())
    if not 350<=count<=400:raise ValueError(f'Explanation word count {count}')
    manifest={p.name:sha(p) for p in (root/'sources').iterdir() if p.suffix in ('.pdf','.xlsx')}
    (root/'sources/source_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    from pypdf import PdfReader
    pdf=PdfReader(root/'report/PROJECT_REPORT.pdf')
    alltext='\n'.join(p.extract_text() for p in pdf.pages)
    assert all(s in alltext for s in ('Chapter 1','Chapter 5','79.30','References'))
    assert sum(c['status'].startswith('EXCLUDED') for c in checks)==1
    assert all((root/'report'/p).resolve().is_file() for p in re.findall(r'<img src="([^"]+)"',page))
    assert all(f'id="{p}"' in page for p in re.findall(r'href="#([^"]+)"',page))
    verification={'pdf_pages':len(pdf.pages),'explanation_word_count':count,'extracted_estimates':len(records),'distribution_checks':len(checks),'excluded_source_items':1,'internal_html_links':'PASS','chart_links':'PASS','pdf_text_checks':'PASS'}
    (root/'results/VERIFICATION.json').write_text(json.dumps(verification,indent=2),encoding='utf-8')
    print(json.dumps(verification))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parent);args=parser.parse_args();build(args.root.resolve())
