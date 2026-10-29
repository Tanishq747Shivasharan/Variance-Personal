# IT Project Delay & Performance Analytics

## 1. Project overview

**Dataset:** SEERA software-project dataset  
**Current analysis scope:** 120 projects  
**Project type:** Exploratory data analytics and decision-support prototype

This project investigates schedule performance in software projects. It uses Python to calculate schedule variance, summarize delay status, inspect data quality, and compare observed delay rates across selected project attributes. Current deliverables include analysis scripts, CSV summaries, a data-quality report, and static charts.

> **Current status:** This is an initial analytical prototype, not a production forecasting system. Findings are descriptive associations and must not be presented as proof that a factor causes delays.

## 2. Problem statement

Raw project records do not automatically make schedule-performance patterns easy to understand. This project turns the SEERA dataset into interpretable summaries to investigate:
- How many projects were delayed, on schedule, or ahead of schedule?
- How large were schedule variances in the observed sample?
- How do observed delay rates differ across recorded project characteristics?
- Which fields, category codes, or missing values need data-dictionary verification?

## 3. Objectives

1. Inspect the dataset structure and columns.
2. Validate key fields and identify missing, invalid, or inconsistent values.
3. Explore the data using descriptive statistics.
4. Calculate schedule performance and summarize delay status.
5. Check effort-related consistency where supported by available fields.
6. Compare observed delay rates across selected factors.
7. Export analysis tables and charts that can be reviewed and reproduced.
8. Document limitations and outline a path toward an interactive dashboard and more rigorous analysis.

## 4. Repository workflow

| Script | Purpose |
|---|---|
| `src/01_inspect_dataset.py` | Inspect workbook structure and columns |
| `src/02_validate_dataset.py` | Validate dataset fields and data quality |
| `src/03_explore_dataset.py` | Initial exploratory analysis |
| `src/04_analyze_delays.py` | Analyze schedule delay/performance |
| `src/05_check_effort_consistency.py` | Check effort-related consistency |
| `src/06_analyze_delay_factors.py` | Compare delay rates across factors and export CSV summaries |
| `src/07_create_review_charts.py` | Generate review charts |

Current outputs:
- `outputs/analysis/delay_factor_summary.csv`
- `outputs/analysis/delay_factor_data_quality.csv`
- `outputs/figures/schedule_performance.png`
- `outputs/figures/delay_rates_by_factor.png`

Expected raw workbook path:

`The_SEERA_Dataset/The SEERA Dataset/Dataset Files/SEERA dataset original raw data.xlsx`

The worksheet name currently used by the analysis is `SEERA dataset ` (with a trailing space), and scripts may rely on that exact name and header row. If the workbook is not supplied in the repository, obtain it from the project owner or an authorized source and preserve the expected path.

## 5. Preliminary findings

The current analysis reports the following for 120 projects:

| Schedule status | Projects | Share |
|---|---:|---:|
| Delayed | 97 | 80.8% |
| On schedule | 17 | 14.2% |
| Ahead of schedule | 6 | 5.0% |
| **Total** | **120** | **100%** |

Previously calculated descriptive statistics:
- Mean schedule variance: 4.70
- Median schedule variance: 2.25
- Minimum schedule variance: -3.00
- Maximum schedule variance: 36.00
- Mean percentage variance: 90.64%
- Median percentage variance: 58.57%

**Schedule variance = actual duration − estimated duration.**

A positive result indicates that the project took longer than estimated; zero indicates equal duration; a negative result indicates that it took less time. Do not state a time unit until the dataset documentation confirms it.

Percentage variance can be disproportionately influenced by projects with small estimated durations. Interpret the mean alongside the median and raw duration variance.

## 6. How this differs from Power BI and general-purpose analytics tools

This is not a claim that Power BI or similar tools cannot perform these analyses. They can. The distinction is the project's current scope and implementation.

| Dimension | This project (current prototype) | General-purpose BI tools such as Power BI |
|---|---|---|
| Primary purpose | Focused analysis of software-project schedule performance in the SEERA dataset | Broad business intelligence, reporting, data modelling, and dashboarding |
| Analysis logic | Explicit Python scripts define validation, calculations, grouping, and exports | Often built through visual interfaces, data models, formulas, queries, and optional code |
| Reproducibility | Source code can be version-controlled and rerun in a consistent Python environment | Reports can be refreshed and shared; reproducibility depends on the report, model, sources, and configuration |
| Data-quality transparency | Can export explicit findings for missing values and unverified mappings | Data profiling and transformation features exist, but the relevant checks must still be designed |
| Domain focus | Specifically examines schedule variance and observed delay rates | General-purpose across many domains |
| Current interface | Static PNG charts and CSV outputs | Interactive filtering, drill-through, and sharing are common strengths |
| Current maturity | Small academic prototype that needs more tests and documentation | Mature products with broader reporting, governance, collaboration, and deployment capabilities |

### What makes this project valuable

- The schedule-variance formula is visible in code.
- Data-quality findings can be exported as files.
- Results can be regenerated by rerunning scripts.
- Unverified category codes can be disclosed rather than silently assigned meanings.
- The analysis scripts could later become the analytical layer behind an interactive dashboard.

### What it does not do yet

Do not describe the current version as an AI prediction engine, causal inference system, real-time monitoring platform, or replacement for Power BI. No validated predictive model or production dashboard is established by the current deliverables.

## 7. Methodology

1. Load the original SEERA workbook.
2. Inspect dimensions, field names, types, and identifiers.
3. Validate missing/invalid values and investigate inconsistent records.
4. Interpret category codes using the codebook; preserve unknown values until verified.
5. Calculate schedule variance from actual and estimated duration.
6. Summarize schedule status and descriptive statistics.
7. Compare observed delay rates across selected factors.
8. Export analysis tables and charts.
9. Interpret results cautiously, considering sample sizes, missing data, codebook uncertainty, and possible confounding.

## 8. Limitations

- The dataset contains 120 projects; findings should not automatically be generalized to all software projects.
- Group sizes vary, and rates based on small groups can be unstable.
- Some categorical codes still need verification against the codebook.
- Missing values must be handled explicitly.
- An association between a factor and delay does not establish causation.
- Predictive performance has not been established.
- Results depend on the quality and interpretation of the source data.

## 9. Reproducibility and cross-platform support

The project is intended to run on Windows, macOS, and Linux. Use a supported Python 3 version and a virtual environment. Commands differ slightly by operating system; see `TEAM_CLONE_PULL_AND_SETUP_GUIDE.md` for copy-paste instructions for Windows PowerShell, Windows Command Prompt, macOS, and Linux.

The current known Python packages are `pandas`, `matplotlib`, and `openpyxl`. A reviewed `requirements.txt` should be committed after the team verifies the imports and tested versions across the scripts.

## 10. Suggested two-minute demonstration

1. Introduce the problem: understanding schedule performance in software projects.
2. Show the SEERA dataset and explain the validation step.
3. Explain the formula: actual duration minus estimated duration.
4. Open `outputs/figures/schedule_performance.png` and state the current status counts.
5. Open `outputs/figures/delay_rates_by_factor.png`; explain that rates are descriptive and group sizes matter.
6. Show the data-quality CSV and point out that unknown category codes are flagged for verification.
7. Close with next steps: verified mappings, reproducible setup, tests, and an interactive dashboard.

## 11. Team contribution record

Record only work actually completed. Do not claim work that was not performed.

| Team member | Actual contribution | Evidence |
|---|---|---|
| Tanishq Shivasharan | Completed the whole audit of the dataset | Scripting and main commits |
| Ankita Karke | [Specific work completed] | [Script, commit, chart, test, or documentation] |
| Ankita Salpekar | [Specific work completed] | [Script, commit, chart, test, or documentation] |
| Kranit Ingle | [Specific work completed] | [Script, commit, chart, test, or documentation] |
| Ayush Bage | [Specific work completed] | [Script, commit, chart, test, or documentation] |