"""Build the existing MBA research documents into an offline, printable report."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPORT = ROOT / "outputs" / "MBA_Project_Chapters_1_to_3.md"
QUESTIONNAIRE = ROOT / "outputs" / "MBA_Draft_Questionnaire.md"

CSS = """
:root{color-scheme:light;--ink:#1b2938;--muted:#526578;--accent:#125e69;--line:#d7e1e5}
*{box-sizing:border-box}body{margin:0;background:#f0f4f5;color:var(--ink);font:17px/1.7 Georgia,serif}
.shell{display:grid;grid-template-columns:270px minmax(0,920px);gap:36px;max-width:1260px;margin:auto;padding:32px}
nav{font:14px/1.5 system-ui,sans-serif;position:sticky;top:24px;align-self:start;max-height:90vh;overflow:auto}
nav a{display:block;padding:8px 0;color:var(--accent);text-decoration:none;border-bottom:1px solid var(--line)}
nav a:hover,nav a:focus{text-decoration:underline}main{background:white;padding:48px;border-radius:8px;min-width:0}
h1,h2,h3{font-family:system-ui,sans-serif;line-height:1.3;scroll-margin-top:24px}h1{font-size:1.8rem;margin-top:48px}
h1:first-child{margin-top:0}h2{font-size:1.3rem;margin-top:36px}h3{font-size:1.1rem;margin-top:28px}
a{color:var(--accent);overflow-wrap:anywhere}p,li{overflow-wrap:anywhere}img{max-width:100%;height:auto}.table-wrap{overflow-x:auto;margin:24px 0}
table{border-collapse:collapse;width:100%;font:14px/1.5 system-ui,sans-serif}th,td{padding:12px;text-align:left;border:1px solid var(--line);vertical-align:top}
th{background:#eaf1f3}code{font-size:.9em;background:#f0f4f5;padding:2px 4px}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f0f4f5;padding:16px;font:13px/1.6 monospace}.badge{padding:16px;border-left:4px solid var(--accent);background:#eaf1f3;font:14px/1.6 system-ui,sans-serif;margin-bottom:32px}
button{background:var(--accent);color:white;border:0;border-radius:4px;padding:12px 18px;cursor:pointer;font:inherit;margin:16px 0}
button:focus-visible,a:focus-visible{outline:3px solid #d98218;outline-offset:3px}footer{font:13px/1.5 system-ui,sans-serif;color:var(--muted);border-top:1px solid var(--line);padding-top:20px;margin-top:40px}
@media(max-width:800px){.shell{display:block;padding:16px}nav{position:static;max-height:none;margin-bottom:24px}main{padding:24px}h1{font-size:1.5rem}}
@media print{@page{size:A4;margin:18mm}body{background:white;font-size:11pt}.shell{display:block;padding:0}nav,button{display:none}main{padding:0;border-radius:0}h1{break-before:page}h1:first-child{break-before:auto}h1,h2,h3{break-after:avoid}.table-wrap{overflow:visible}table{font-size:9pt}tr{break-inside:avoid}a{color:inherit}.badge{font-size:9pt}footer{font-size:9pt}}
"""


def load_sources(report: Path = REPORT, questionnaire: Path = QUESTIONNAIRE) -> str:
    """Use the standalone questionnaire as the single appendix source."""
    for path in (report, questionnaire):
        if not path.is_file():
            raise ValueError(f"Required source is missing: {path.name}")
    source = report.read_text(encoding="utf-8-sig")
    source = source.split("# Appendix A: Draft Survey Instrument", 1)[0].rstrip()
    survey = questionnaire.read_text(encoding="utf-8-sig").strip()
    if not source or not survey:
        raise ValueError("Report and questionnaire sources must not be empty.")
    survey = re.sub(r'^# ', '## ', survey, count=1)
    return source + "\n\n# Appendix A: Draft Survey Instrument\n\n" + survey + "\n"


def validate_source(source: str) -> None:
    for number in range(1, 6):
        if len(re.findall(rf"^# Chapter {number}:", source, flags=re.M)) != 1:
            raise ValueError(f"Expected exactly one Chapter {number}.")
    if source.count("# Appendix A: Draft Survey Instrument") != 1:
        raise ValueError("Expected one survey appendix.")
    for field in ("A02", "A07b", "P01", "E01", "K01", "D01"):
        if not re.search(rf"^{field}\.", source, flags=re.M):
            raise ValueError(f"Required questionnaire item missing: {field}")
    if "no empirical conclusion" not in source.lower():
        raise ValueError("The report must disclose its lack of empirical conclusions.")
    if re.search(r"(?:C:[/\\]Users[/\\]|file://)", source, flags=re.I):
        raise ValueError("Machine-specific paths must not appear in the report.")


def render(source: str, imported_evidence: bool = False, synthetic: bool = False) -> str:
    try:
        import markdown
    except ImportError as exc:
        raise ValueError("Install the dependency with: python -m pip install -r requirements.txt") from exc
    import html

    # Source files contain research prose, not executable HTML. Escape raw tags.
    safe_source = source.replace("<", "&lt;").replace(">", "&gt;")
    md = markdown.Markdown(extensions=["tables", "toc", "sane_lists", "fenced_code"],
                           extension_configs={"toc": {"toc_depth": "1-1"}})
    body = md.convert(safe_source)
    # Turn bare bibliographic URLs into clickable links without nesting links.
    parts = re.split(r"(<[^>]+>)", body)
    inside_link = False
    for i, part in enumerate(parts):
        if part.startswith("<a "):
            inside_link = True
        elif part == "</a>":
            inside_link = False
        elif not part.startswith("<") and not inside_link:
            parts[i] = re.sub(r"https://[^\s<]+", lambda m: '<a href="' + html.escape(m[0], quote=True) + '">' + m[0] + '</a>', part)
    body = "".join(parts).replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
    title = html.escape("AI Adoption and Operational Efficiency — MBA Research Project")
    status = ('Aggregate analysis from researcher-declared genuine input is included. Authenticity and institutional acceptance are not independently established.'
              if imported_evidence else 'The research-design narrative and draft instrument are developed. No survey data have been collected; empirical results and final interpretation remain pending.')
    if synthetic:
        status = 'SYNTHETIC SOFTWARE TEST ONLY — NOT RESEARCH FINDINGS. This isolated report tests rendering; no respondents are represented.'
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title><style>{CSS}</style></head><body>
<div class="shell"><nav aria-label="Report sections"><strong>MBA research project</strong>
<button type="button" onclick="window.print()">Print / Save as PDF</button>{md.toc}</nav>
<main><div class="badge"><strong>Research design report · Chennai IT-enabled services</strong><br>
{status}</div>
{body}<footer>Generated reproducibly from the report and questionnaire sources. Offline document with no analytics, uploads, or automatic network requests; external reference links open their cited sources.</footer></main></div></body></html>"""


def build(output: Path, input_path: Path | None = None, manifest_path: Path | None = None,
          synthetic_check: bool = False) -> Path:
    from research_pipeline import dictionary_markdown, run, results_markdown, chart
    output = Path(output)
    if output.suffix.lower() != '.html':
        raise ValueError('Report destination must be an .html file; source files are never overwritten.')
    if output.resolve() in (REPORT.resolve(), QUESTIONNAIRE.resolve()):
        raise ValueError('Report destination must not overwrite research sources.')
    source = load_sources()
    validate_source(source)
    if bool(input_path) != bool(manifest_path):
        raise ValueError('Supply both --input and --manifest to include actual analysis.')
    imported = input_path is not None
    if synthetic_check and not imported:
        raise ValueError('Synthetic check needs explicitly labelled input and a manifest.')
    if imported:
        import base64
        import json
        manifest = json.loads(manifest_path.read_text(encoding='utf-8-sig'))
        kind = manifest.get('evidence_kind') if isinstance(manifest, dict) else None
        if kind != ('synthetic' if synthetic_check else 'real'):
            raise ValueError('Synthetic/test analysis is prohibited in the research report.')
        target = ROOT / ('work' if synthetic_check else 'private')
        if not output.resolve().is_relative_to(target.resolve()):
            raise ValueError('Research reports require private/; synthetic checks require work/.')
        if output.resolve() in (input_path.resolve(), manifest_path.resolve()):
            raise ValueError('Report destination must not overwrite input or provenance files.')
        result = run(input_path, manifest_path, output.parent/'analysis')
        first = source.index('# Chapter 4:')
        last = source.index('# Chapter 5:')
        diagram = base64.b64encode(chart(result).encode()).decode()
        source = source[:first] + '# Chapter 4: Supplied Evidence Analysis\n\n' + results_markdown(result) + f'\n### 4.3 Adoption-frequency figure\n\nFigure 4.1 displays classified frequency counts; unknown/unclassified frequency is reported separately above.\n\n![Adoption frequency in supplied sample](data:image/svg+xml;base64,{diagram})\n\n**Figure 4.1. Reported AI-use frequency in retained supplied records**\n\n' + source[last:]
        first = source.index('## Document status')
        last = source.index('## Abstract — research-design edition')
        source = source[:first] + '## Document status\n\nThis edition includes aggregate analysis of researcher-declared genuine input. Source provenance is declared, not independently verified. Chapter 3 remains the planned methodology; the analysis protocol must be reviewed against actual collection. Institutional acceptance and empirical interpretation remain external requirements.\n\n' + source[last:]
        if synthetic_check:
            source = source.replace('This edition includes aggregate analysis of researcher-declared genuine input.',
                                    'SYNTHETIC SOFTWARE TEST ONLY: all imported records are generated software fixtures, not respondents.')
        source = source.replace('No genuine respondent data are available in this edition, so it reports no empirical estimates or findings.',
                                'Supplied-record aggregates are presented in Chapter 4; this design abstract does not interpret them as completed research findings.')
        source = source.replace('The design has no empirical conclusion about the direction or magnitude of adoption–performance relationships.',
                                'The software generates descriptive estimates and, where enabled, conditional tests, but no empirical conclusion is inferred automatically.')
        source = source.replace('No participant review, pilot, main survey dataset, or empirical results exist.',
                                'Participant review and pilot evidence must be established separately from supplied main records.')
        source = source.replace('Participant review, empirical data, actual analysis, and final conclusions are outstanding.',
                                'Supplied data are processed in this edition; external validation, methodological review, and final empirical conclusions remain researcher responsibilities.')
        source = source.replace('External review, genuine data, real-data analysis, and final empirical conclusions remain pending.',
                                'Supplied records have been processed; external validation, methodological review, and final empirical conclusions remain pending.')
        source = source.replace('## 5.4 Evidence-based discussion procedure — pending data',
                                '## 5.4 Evidence-based discussion procedure — pending interpretation')
    source += '\n\n' + dictionary_markdown()
    page = render(source, imported, synthetic_check)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(page, encoding="utf-8")
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "outputs" / "MBA_Project_Report.html")
    parser.add_argument('--input', type=Path, help='Coded genuine responses under private/.')
    parser.add_argument('--manifest', type=Path, help='Provenance and analysis decisions for this file.')
    parser.add_argument('--synthetic-check', action='store_true', help='Isolated software test report under work/; never research findings.')
    args = parser.parse_args()
    try:
        path = build(args.output, args.input, args.manifest, args.synthetic_check)
    except (ValueError, OSError, TypeError) as exc:
        print(f"Build failed: {exc}", file=sys.stderr)
        return 1
    print(f"Report built: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
