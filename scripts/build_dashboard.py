"""Build an offline comparison dashboard from the verified OECD output files."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SECTORS = ('Finance and insurance', 'Manufacturing')
TOPICS = (
    ('Adoption', ('Employer AI adoption',)),
    ('Performance', ('Employer perceived productivity: positive', 'Worker perceived performance: improved')),
    ('Work organization', ('Worker task pace: increased', 'Worker task control: increased')),
    ('Decision assistance', ('Workers receiving decision assistance', 'Decision quality: agreement',
                             'Decision enjoyment: agreement', 'Decision speed: agreement')),
    ('Adoption barriers', ('High-cost barrier', 'Skills barrier', 'Not convinced of benefits',
                           'Government-regulation barrier')),
    ('Task changes', ('Task automation', 'Task creation', 'Both automation and creation')),
)

def load_csv(path):
    with path.open(encoding='utf-8', newline='') as stream:
        return list(csv.DictReader(stream))

def describe(metric, size=False):
    if size:
        return 'Employers in this firm-size band', ['Yes'], 'Adoption prevalence, not a performance measure.'
    if metric == 'Employer AI adoption':
        return 'All surveyed employers', ['Yes'], 'Adoption prevalence, not a performance measure.'
    if metric == 'Employer perceived productivity: positive':
        return 'AI-adopting employers', ['Positive'], 'Reported positive effects, not measured productivity growth.'
    if metric == 'Worker perceived performance: improved':
        return 'AI-using workers', ['Improved a lot', 'Improved a little'], 'Reported own performance, not independently measured output.'
    if metric in ('Worker task pace: increased', 'Worker task control: increased'):
        return 'AI-using workers', ['Increased a little', 'Increased a lot'], 'A faster pace can indicate work intensification; it is not automatically a benefit.'
    if metric == 'Workers receiving decision assistance':
        return 'AI-using workers', ['Yes'], 'Prevalence of decision assistance, not its quality.'
    if metric.startswith('Decision '):
        return 'Workers receiving AI decision assistance', ['Strongly agree', 'Somewhat agree'], 'Agreement with a perception statement, not measured accuracy or decision time.'
    if metric in TOPICS[4][1]:
        return 'All surveyed employers', ['Yes'], 'Reported barrier. A higher percentage is not a better outcome; barriers can overlap.'
    if metric in TOPICS[5][1]:
        return 'AI-adopting employers', ['Reported'], 'Task indicators overlap. Do not sum automation, creation, and both.'
    raise ValueError(f'No documented population or calculation for {metric}')

def dashboard_data(root):
    observations = load_csv(root/'results/observations.csv')
    comparisons = load_csv(root/'results/sector_comparisons.csv')
    sizes = load_csv(root/'results/adoption_by_firm_size.csv')
    topic_by_metric = {metric: topic for topic, metrics in TOPICS for metric in metrics}
    if {row['metric'] for row in comparisons} != set(topic_by_metric):
        raise ValueError('Unexpected or missing sector indicators; review dashboard metadata')
    indicators = []
    for index, row in enumerate(comparisons + sizes):
        size = index >= len(comparisons)
        metric = row['metric']
        lookup = 'AI adoption: ' + metric if size else metric
        population, included, caveat = describe(metric, size)
        evidence = [dict(item, percentage=float(item['percentage']),
                         unweighted_source_subgroup_n=int(item['unweighted_source_subgroup_n']))
                    for item in observations if item['metric'] == lookup]
        values = [float(row['finance_percent']), float(row['manufacturing_percent'])]
        for sector, expected in zip(SECTORS, values):
            selected = [item for item in evidence if item['sector'] == sector]
            if not selected or len({item['unweighted_source_subgroup_n'] for item in selected}) != 1:
                raise ValueError(f'Missing or inconsistent source subgroup: {lookup}, {sector}')
            contributing = [item for item in selected if item['response'] in included]
            if {item['response'] for item in contributing} != set(included):
                raise ValueError(f'Missing calculation categories: {lookup}, {sector}')
            if abs(sum(item['percentage'] for item in contributing) - expected) > .011:
                raise ValueError(f'Dashboard summary disagrees with source estimates: {lookup}, {sector}')
        difference = float(row['manufacturing_minus_finance_pp'])
        if not all(0 <= value <= 100 for value in values) or abs(values[1]-values[0]-difference) > .011:
            raise ValueError(f'Invalid sector comparison: {lookup}')
        indicators.append(dict(id=str(index), metric=metric, topic='Adoption by firm size' if size else topic_by_metric[metric],
                               population=population, included=included, caveat=caveat,
                               finance=values[0], manufacturing=values[1], difference=difference,
                               sheet=row['source_sheet'], evidence=evidence))
    return indicators

PAGE = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Workplace AI comparison dashboard</title><style>
:root{--ink:#183142;--muted:#526a79;--blue:#125b7c;--orange:#b85a1b;--line:#cddde6;--bg:#f2f6f8}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 system-ui,Arial}header{background:#143c52;color:white;padding:36px max(22px,calc((100vw - 1120px)/2))}h1{font-size:clamp(28px,4vw,42px);line-height:1.2;margin:8px 0 16px}h2{font-size:24px;line-height:1.3}h3{margin:8px 0}.eyebrow{text-transform:uppercase;letter-spacing:.08em;font-size:12px}header p{max-width:900px;color:#d6e8f1}main{max-width:1168px;margin:auto;padding:24px}.panel{background:white;border:1px solid var(--line);border-radius:14px;padding:26px;margin-bottom:22px}.filters{display:grid;grid-template-columns:1fr 2fr;gap:20px}label{display:block;font-weight:650;margin-bottom:6px}select,button{font:inherit;padding:11px;border:1px solid #91aab9;border-radius:7px;background:white;color:var(--ink);max-width:100%}select{width:100%}button{cursor:pointer}button:hover{background:#eaf2f7}select:focus-visible,button:focus-visible,a:focus-visible,summary:focus-visible{outline:3px solid #b76c20;outline-offset:3px}.stats{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin:22px 0}.stat{border:1px solid var(--line);border-radius:10px;padding:18px;background:#f8fbfc}.value{font-size:clamp(25px,3vw,36px);font-weight:750;font-variant-numeric:tabular-nums}.small{font-size:14px;color:var(--muted)}.badge{font-size:13px;background:#eaf2f7;border-radius:5px;display:inline-block;padding:3px 8px}.chart-row{display:grid;grid-template-columns:155px 1fr 82px;gap:14px;align-items:center;margin:20px 0}.track{height:34px;background:#e9f0f4;border-radius:5px;overflow:hidden}.bar{height:100%;background:var(--blue)}.orange{background:var(--orange)}.axis{display:flex;justify-content:space-between;margin-left:169px;margin-right:96px;font-size:12px;color:var(--muted)}.note{border-left:4px solid #c17a2d;background:#fff7ec;padding:14px 18px;margin:18px 0}.scroll{overflow:auto}table{width:100%;border-collapse:collapse;font-size:14px}th,td{padding:12px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}th{background:#edf4f8}td.num{font-variant-numeric:tabular-nums;white-space:nowrap}.included{background:#eef7f3}a{color:var(--blue)}.links{display:flex;gap:20px;flex-wrap:wrap;margin-top:18px}details{margin:18px 0}summary{cursor:pointer;font-weight:650}footer{max-width:1120px;margin:0 auto;padding:0 22px 30px;color:var(--muted);font-size:14px}.section-space{margin-top:28px}.nojs{padding:15px;background:#fff7ec}@media(max-width:650px){main{padding:14px}.panel{padding:20px 16px}.filters,.stats{grid-template-columns:1fr}.stats{gap:10px}.stat{padding:14px}.chart-row{grid-template-columns:100px 1fr 65px;gap:8px}.axis{margin-left:108px;margin-right:73px}th,td{padding:9px}}@media print{header{background:white;color:var(--ink);padding:12px}header p{color:var(--muted)}body{background:white}.filters,button,.links{display:none}.panel{border:0;padding:10px 0}main{padding:0}.stats{break-inside:avoid}h2,h3{break-after:avoid}.scroll{overflow:visible}table{font-size:10pt}}
</style></head><body><header><div class="eyebrow">Operations Management · OECD secondary analysis</div><h1>Workplace AI comparison dashboard</h1><p>Explore published AI adoption, performance perceptions, task changes, decision assistance, and barriers across finance and insurance and manufacturing.</p><p>2022 fieldwork · Seven OECD countries · Published weighted percentages</p></header><main>
<section class="panel" aria-label="Indicator controls"><div class="filters"><div><label for="topic">Research topic</label><select id="topic"><option value="all">All topics</option></select></div><div><label for="indicator">Indicator</label><select id="indicator"></select></div></div><p class="small" id="selection-count"></p></section>
<noscript><p class="nojs">Enable JavaScript to select indicators and view comparisons. The original report and CSV results remain available through the links below.</p></noscript>
<section class="panel" aria-labelledby="metric-title"><span id="topic-label" class="badge"></span><h2 id="metric-title">Select an indicator</h2><p id="population"></p><div class="stats"><div class="stat"><div>Finance and insurance</div><div id="finance-value" class="value"></div><div id="finance-n" class="small"></div></div><div class="stat"><div>Manufacturing</div><div id="manufacturing-value" class="value"></div><div id="manufacturing-n" class="small"></div></div><div class="stat"><div>Manufacturing minus finance</div><div id="difference-value" class="value"></div><div class="small">Percentage points, not percentage growth</div></div></div>
<div role="img" id="chart" aria-label="Selected sector comparison"><div class="chart-row"><span>Finance and insurance</span><div class="track"><div class="bar" id="finance-bar"></div></div><strong id="finance-label"></strong></div><div class="chart-row"><span>Manufacturing</span><div class="track"><div class="bar orange" id="manufacturing-bar"></div></div><strong id="manufacturing-label"></strong></div><div class="axis"><span>0%</span><span>50%</span><span>100%</span></div></div>
<p id="comparison" role="status" aria-live="polite"></p><div class="note" id="caveat"></div><p class="small">The bars use the same 0–100% scale for every indicator. A higher percentage is not automatically better. Differences are descriptive; no significance test or causal effect is estimated.</p>
<h3>Calculation and source</h3><p id="formula"></p><p id="source"></p><p class="small">Subgroup n is the original unweighted source count. Percentages are weighted estimates; multiplying them by n does not recover observed respondent counts.</p>
<details open><summary>Underlying published response categories</summary><p class="small">Shaded rows contribute to the displayed percentage. Other answers remain visible for context. Each row below is a published estimate, not a person.</p><div class="scroll"><table><thead><tr><th scope="col">Sector</th><th scope="col">Source response</th><th scope="col">Published %</th><th scope="col">Source cell</th><th scope="col">Used in result</th></tr></thead><tbody id="evidence"></tbody></table></div></details></section>
<section class="panel"><h2>Compare all indicators in this topic</h2><p class="small">Rows can use different respondent subgroups and questions. Do not average them into a single efficiency score. Select a row to inspect its population and source.</p><div class="scroll"><table><thead><tr><th scope="col">Indicator</th><th scope="col">Finance %</th><th scope="col">Manufacturing %</th><th scope="col">Difference pp</th></tr></thead><tbody id="comparison-table"></tbody></table></div></section>
<section class="panel"><h2>Evidence and boundaries</h2><p>The source study covers Austria, Canada, France, Germany, Ireland, the United Kingdom, and the United States, in finance and insurance and manufacturing. These are genuine published OECD survey aggregates, not responses collected by this project.</p><p>Results do not represent Chennai or India, a current adoption census, measured financial savings, or causal effects. Employer and worker populations are separate and unpaired.</p><p>A finance staff-cost motivation distribution in Figure 3.1 totals 94%. It is disclosed and excluded from comparisons; it is not selectable in this dashboard.</p><p>Source: Lane, Williams, and Broecke (2023), <em>The impact of AI on the workplace</em>, OECD Working Paper No. 288, and its supplementary workbook. <a href="https://doi.org/10.1787/ea0a0fe1-en" target="_blank" rel="noopener noreferrer">Read the original OECD report</a>.</p><div class="links"><a href="Project_Complete_Explainer.html">Project explanation and voice-over</a><a href="../report/PROJECT_REPORT.html">Research report</a><a href="../results/sector_comparisons.csv" download>Sector comparison CSV</a></div><p class="small">Offline page generated from the project results. The read-only controls select existing evidence; they do not edit the source files or create new findings.</p></section>
</main><footer>Rebuild with python scripts/build_dashboard.py after regenerating project results. Full builds include this dashboard in the submission ZIP.</footer>
<script type="application/json" id="dashboard-data">__DATA__</script><script>
'use strict';
const indicators=JSON.parse(document.getElementById('dashboard-data').textContent),get=id=>document.getElementById(id),fmt=n=>Number(n).toFixed(2),signed=n=>(n>0?'+':'')+fmt(n);
const topic=get('topic'),picker=get('indicator');
function cell(row,text,cls){const td=document.createElement('td');td.textContent=text;if(cls)td.className=cls;row.append(td);return td;}
function filtered(){return indicators.filter(row=>topic.value==='all'||row.topic===topic.value);}
function render(){
 const row=indicators.find(item=>item.id===picker.value);if(!row)return;
 get('topic-label').textContent=row.topic;get('metric-title').textContent=row.metric;get('population').textContent='Population for this indicator: '+row.population+'.';
 for(const [prefix,sector,value] of [['finance','Finance and insurance',row.finance],['manufacturing','Manufacturing',row.manufacturing]]){
  get(prefix+'-value').textContent=fmt(value)+'%';get(prefix+'-label').textContent=fmt(value)+'%';get(prefix+'-bar').style.width=value+'%';
  const records=row.evidence.filter(item=>item.sector===sector);get(prefix+'-n').textContent='Source subgroup n = '+records[0].unweighted_source_subgroup_n.toLocaleString('en-US');
 }
 get('difference-value').textContent=signed(row.difference)+' pp';get('chart').setAttribute('aria-label',row.metric+': finance '+fmt(row.finance)+' percent; manufacturing '+fmt(row.manufacturing)+' percent.');
 get('comparison').textContent=row.difference===0?'The displayed sector estimates are equal.':(row.difference>0?'Manufacturing':'Finance and insurance')+' has a '+fmt(Math.abs(row.difference))+' percentage-point higher reported share for this indicator.';
 get('caveat').textContent=row.caveat;get('source').textContent='Worksheet: '+row.sheet+'. Source cells are listed below.';
 const equations=['Finance and insurance','Manufacturing'].map(sector=>{const items=row.evidence.filter(item=>item.sector===sector&&row.included.includes(item.response));return sector+': '+items.map(item=>fmt(item.percentage)+'%').join(' + ')+' = '+fmt(sector==='Manufacturing'?row.manufacturing:row.finance)+'%';});
 get('formula').textContent='Included answers: '+row.included.join(' + ')+'. '+equations.join('; ')+'. Difference: '+fmt(row.manufacturing)+' − '+fmt(row.finance)+' = '+signed(row.difference)+' pp.';
 get('evidence').replaceChildren();for(const item of row.evidence){const tr=document.createElement('tr'),used=row.included.includes(item.response);if(used)tr.className='included';cell(tr,item.sector);cell(tr,item.response);cell(tr,fmt(item.percentage),'num');cell(tr,row.sheet+'!'+item.source_cell);cell(tr,used?'Yes':'No');get('evidence').append(tr);}
}
function filter(){const previous=picker.value,rows=filtered();picker.replaceChildren();for(const row of rows){const o=document.createElement('option');o.value=row.id;o.textContent=row.metric;picker.append(o);}picker.value=rows.some(row=>row.id===previous)?previous:rows[0].id;
 get('selection-count').textContent=rows.length+' indicators in this selection · '+indicators.length+' available overall';get('comparison-table').replaceChildren();
 for(const row of rows){const tr=document.createElement('tr'),td=document.createElement('td'),button=document.createElement('button');button.type='button';button.textContent=row.metric;button.setAttribute('aria-label','Inspect '+row.metric);button.addEventListener('click',()=>{picker.value=row.id;render();get('metric-title').scrollIntoView({block:'start',behavior:'smooth'});});td.append(button);tr.append(td);cell(tr,fmt(row.finance),'num');cell(tr,fmt(row.manufacturing),'num');cell(tr,signed(row.difference),'num');get('comparison-table').append(tr);}render();}
for(const name of [...new Set(indicators.map(row=>row.topic))]){const o=document.createElement('option');o.value=name;o.textContent=name;topic.append(o);}
topic.addEventListener('change',filter);picker.addEventListener('change',render);filter();
</script></body></html>'''

def build_dashboard(root=ROOT):
    root=Path(root).resolve()
    data=dashboard_data(root)
    page=PAGE.replace('__DATA__',json.dumps(data,ensure_ascii=False).replace('<','\\u003c'))
    path=root/'outputs/AI_Comparison_Dashboard.html'
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(page,encoding='utf-8')
    print(f'Comparison dashboard: {path}')
    return path

if __name__=='__main__':build_dashboard()
