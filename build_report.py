"""Build the canonical OECD report, explainer and portable submission ZIP."""
from pathlib import Path
import argparse
import importlib.util
import zipfile
from research_pipeline import build

ROOT = Path(__file__).resolve().parent

def release(root=ROOT):
    root = Path(root).resolve()
    build(root)
    spec = importlib.util.spec_from_file_location('project_explainer', root/'scripts/build_explainer.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    spec = importlib.util.spec_from_file_location('project_dashboard', root/'scripts/build_dashboard.py')
    dashboard = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(dashboard)
    dashboard.build_dashboard(root)
    return package_release(root)

def package_release(root=ROOT):
    """Package existing outputs without rerunning the analysis or PDF renderer."""
    root=Path(root).resolve()
    output = root/'outputs/MBA_Secondary_Data_Submission_Package.zip'
    folders = ('sources','results','report','figures','references','explanation','scripts','tests')
    files = ['README.md','requirements.txt','research_pipeline.py','build_report.py',
             'Databricks_OECD_Analysis.py','DATABRICKS_SETUP.md','FINAL_SUBMISSION_STATUS.md',
             'SUBMISSION_BLOCKERS.md','SUBMISSION_HANDOFF.md','outputs/Project_Complete_Explainer.html',
             'outputs/AI_Comparison_Dashboard.html']
    files += [name for name in ('stackoverflow_analysis.py','requirements-stackoverflow.txt')
              if (root/name).is_file()]
    if (root/'outputs/stackoverflow2025').is_dir():
        folders += ('outputs/stackoverflow2025',)
    if (root/'assets').is_dir():
        folders += ('assets',)
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as archive:
        for name in files:
            archive.write(root/name,name)
        for folder in folders:
            for path in sorted((root/folder).rglob('*')):
                if path.is_file() and '__pycache__' not in path.parts:
                    archive.write(path,path.relative_to(root).as_posix())
    print(f'Submission ZIP: {output}')
    return output

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--root',type=Path,default=ROOT)
    release(parser.parse_args().root)
