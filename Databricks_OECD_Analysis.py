# Databricks notebook source
# MAGIC %md
# MAGIC # Workplace AI: OECD secondary analysis
# MAGIC Open this notebook inside the project Git folder under **Buisness projects**.
# MAGIC Uses genuine published weighted aggregates, not respondent microdata.
# MAGIC Run all cells on serverless Python or Databricks Runtime 14.0+.

# COMMAND ----------
# MAGIC %pip install -r ./requirements.txt

# COMMAND ----------
dbutils.library.restartPython()

# COMMAND ----------
from pathlib import Path
import sys

dbutils.widgets.text('project_root', str(Path.cwd()), 'Project folder containing sources/ and build_report.py')
project_root = Path(dbutils.widgets.get('project_root')).resolve()
if not (project_root/'sources/OECD_published_tables.xlsx').is_file():
    raise FileNotFoundError('Set project_root to the cloned project folder containing sources/.')
sys.path.insert(0, str(project_root))
from build_report import release

# COMMAND ----------
# Build the same validated outputs locally and in Databricks.
submission_zip = release(project_root)

# COMMAND ----------
# Show the complete report with its SVG charts embedded for notebook display.
import re
page = (project_root/'report/PROJECT_REPORT.html').read_text(encoding='utf-8')
def inline_chart(match):
    path = (project_root/'report'/match.group(1)).resolve()
    if project_root not in path.parents or path.suffix != '.svg':
        raise ValueError('Unexpected chart location')
    return path.read_text(encoding='utf-8')
page = re.sub(r'<img src="([^"]+)"[^>]*>', inline_chart, page)
displayHTML(page)

# COMMAND ----------
# Inspect audit outputs without pretending aggregate rows are respondents.
import csv
import json
from html import escape

with (project_root/'results/sector_comparisons.csv').open(encoding='utf-8',newline='') as stream:
    comparisons = list(csv.DictReader(stream))
table = '<table><tr><th>Indicator</th><th>Finance %</th><th>Manufacturing %</th><th>Difference pp</th></tr>'
for row in comparisons:
    table += '<tr>' + ''.join('<td>'+escape(row[key])+'</td>' for key in (
        'metric','finance_percent','manufacturing_percent','manufacturing_minus_finance_pp')) + '</tr>'
displayHTML(table+'</table>')
print((project_root/'results/VERIFICATION.json').read_text(encoding='utf-8'))
print('Download the report or ZIP from Workspace files:', submission_zip)

# COMMAND ----------
# MAGIC %md
# MAGIC ## Interpretation
# MAGIC No causal effects, actual savings, Chennai results, respondent-level correlations,
# MAGIC or significance tests are claimed. Figure 3.1 finance cost motivation totals 94%
# MAGIC and is excluded from comparisons. Employer and worker denominators differ.
# MAGIC The notebook needs no database, credentials in code, Spark cluster configuration,
# MAGIC or Windows-specific downloaded packages. It installs the pinned Python libraries.
