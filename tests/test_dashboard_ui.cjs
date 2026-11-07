// Dependency-free interaction checks; this does not claim a real browser run.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const path=process.argv[2]||'outputs/AI_Comparison_Dashboard.html';
const html=fs.readFileSync(path,'utf8');
const data=JSON.parse(html.match(/id="dashboard-data">([\s\S]*?)<\/script>/)[1]);
const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
class Element {
 constructor(tag='div'){this.tag=tag;this.value='';this.children=[];this.textContent='';this.style={};this.attributes={};this.events={};}
 append(child){this.children.push(child);if(this.tag==='select'&&this.children.length===1)this.value=child.value;}
 replaceChildren(){this.children=[];if(this.tag==='select')this.value='';}
 setAttribute(k,v){this.attributes[k]=v;}
 addEventListener(k,f){this.events[k]=f;}
 scrollIntoView(){}
}
const ids={};for(const match of html.matchAll(/id="([^"]+)"/g))ids[match[1]]=new Element();
ids.topic.tag='select';ids.topic.value='all';ids.topic.children.push(new Element('option'));
ids.indicator.tag='select';ids['dashboard-data'].textContent=JSON.stringify(data);
const document={getElementById:id=>{assert(ids[id],'Unknown element '+id);return ids[id];},createElement:tag=>new Element(tag)};
vm.runInNewContext(script,{document});
assert.equal(ids.indicator.children.length,20);assert.equal(ids['comparison-table'].children.length,20);
assert.equal(ids['finance-value'].textContent,'41.70%');assert.match(ids['finance-n'].textContent,/653/);
function choose(metric){ids.indicator.value=data.find(row=>row.metric===metric).id;ids.indicator.events.change();}
choose('Employer perceived productivity: positive');assert.equal(ids['difference-value'].textContent,'+5.90 pp');assert.match(ids.population.textContent,/AI-adopting employers/);assert.match(ids['finance-n'].textContent,/291/);assert.equal(ids['finance-bar'].style.width,'56.7%');assert.equal(ids.evidence.children.length,8);
choose('Worker perceived performance: improved');assert.match(ids.formula.textContent,/30.30% \+ 49.00% = 79.30%/);assert.match(ids['finance-n'].textContent,/1,231/);
choose('Decision quality: agreement');assert.equal(ids['difference-value'].textContent,'0.00 pp');assert.match(ids.comparison.textContent,/equal/);assert.match(ids.population.textContent,/receiving AI decision assistance/);
ids.topic.value='Adoption barriers';ids.topic.events.change();assert.equal(ids.indicator.children.length,4);assert.match(ids.caveat.textContent,/higher percentage is not a better outcome/);
ids['comparison-table'].children[1].children[0].children[0].events.click();assert.equal(ids['metric-title'].textContent,'Skills barrier');
ids.topic.value='Adoption by firm size';ids.topic.events.change();assert.equal(ids.indicator.children.length,4);assert.match(ids['finance-n'].textContent,/247/);assert.match(ids['manufacturing-n'].textContent,/529/);
ids.topic.value='all';ids.topic.events.change();assert.equal(ids.indicator.children.length,20);
console.log('PASS: initial view, all 20 indicators, source subgroups, combined categories, equal values, topic filtering, row selection, firm-size subgroups, and reset.');
