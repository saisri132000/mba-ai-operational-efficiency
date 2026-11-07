# New Databricks workspace: Buisness projects

## Create your workspace

1. Visit [Databricks Free Edition](https://www.databricks.com/learn/free-edition) and sign up. Databricks creates a workspace for personal learning. This account action requires your login; no credentials should be sent in chat or stored in Git.
2. Open **Workspace**, then your user folder. Create a folder named exactly **Buisness projects**. This is the project-organizing folder inside the new workspace; the account-level workspace may have an automatically assigned name.
3. Inside that folder, create a **Git folder**, using `https://github.com/Naramalakumarteja/mba-ai-operational-efficiency-chennai.git` and branch `main`. Connect your GitHub account through Databricks' Git integration for access to this private repository. Grant only the access you intend.
4. Open `Databricks_OECD_Analysis.py` from that Git folder and choose serverless Python, or a compatible Runtime 14.0+ environment. Keep the complete folder tree, including `sources/` and `scripts/`.
5. Run all notebook cells. The first cell installs the pinned Python packages. The next restarts Python. The remaining cells validate inputs, generate reports/ZIP, display the report and results, and print output paths.

The current notebook folder is normally the default working directory in Runtime 14.0+. If `project_root` does not locate `sources/`, set it to the complete workspace filesystem path of the cloned Git folder, then rerun from that cell. Do not set it to the parent **Buisness projects** folder unless the project files are directly there.

## Packages and data

`requirements.txt` specifies openpyxl, reportlab, and pypdf. `%pip` installs suitable packages for the Databricks environment; no Windows-specific downloads are uploaded. The genuine source PDF and workbook are versioned in `sources/` and arrive with the Git clone. This small descriptive study does not need Spark, Unity Catalog tables, or a separate database.

Outputs are written into the cloned project folder. Use Workspace's file menu to download the PDF or `outputs/MBA_Secondary_Data_Submission_Package.zip`. The notebook displays the report with embedded SVG charts. The interactive explainer should be downloaded and opened in a browser for voice-over; notebook display policies may restrict JavaScript/speech.

## Honest execution status

The shared pipeline is tested locally. This repository does not claim the notebook was run in a cloud workspace until that workspace exists and an actual execution succeeds. Free Edition has usage limits; account signup and workspace access remain external.

Official documentation:

- [Free Edition signup](https://docs.databricks.com/aws/en/getting-started/free-edition)
- [Workspace browser](https://docs.databricks.com/aws/en/workspace/workspace-browser)
- [Git folders](https://docs.databricks.com/aws/en/repos/)
- [Current working directory](https://docs.databricks.com/aws/en/files/cwd-dbr-14)
- [Notebook libraries](https://docs.databricks.com/aws/en/libraries/)
