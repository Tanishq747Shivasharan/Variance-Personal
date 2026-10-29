# Team Clone, Pull, and Setup Guide (Windows, macOS, and Linux)

This guide helps team members clone the project, set up Python, run the analysis, and pull updates.

> **Important:** If `git status --short` shows files with `??`, those files are untracked. Other members cannot pull them until the project owner adds, commits, and pushes them.

Replace `<REPOSITORY_URL>` with the clone URL from GitHub and `<REPOSITORY_DIRECTORY>` with the folder created by cloning.

## 1. Project owner: publish the latest changes

Run from the project root. Git commands below work in PowerShell, Command Prompt, macOS Terminal, and Linux terminal.

```bash
git branch --show-current
git status --short

git add src/04_analyze_delays.py src/05_check_effort_consistency.py src/06_analyze_delay_factors.py src/07_create_review_charts.py outputs/analysis/delay_factor_data_quality.csv outputs/analysis/delay_factor_summary.csv outputs/figures/schedule_performance.png outputs/figures/delay_rates_by_factor.png

git diff --cached --stat
git diff --cached
git commit -m "Add schedule delay analysis and review charts"
git push -u origin feature/seera-audit
```

Review the staged changes before committing. Do not commit `.venv/`, `__pycache__/`, secrets, or unrelated files. Do not force-push if the remote rejects your push.

The dataset may not be tracked by Git. To check:

**PowerShell**
```powershell
git ls-files | Select-String -Pattern 'SEERA.*xlsx'
```

**macOS/Linux**
```bash
git ls-files | grep -i 'SEERA.*xlsx'
```

If it is not tracked, provide teammates with an authorized copy or source. Do not assume the workbook is in the repository.

## 2. Install Git and Python

### Windows

Install Git for Windows and Python 3:
- Git: https://git-scm.com/downloads
- Python: https://www.python.org/downloads/windows/

Open PowerShell and verify:

```powershell
git --version
py --version
```

### macOS

Install Git and Python 3 from https://www.python.org/downloads/macos/ or, if Homebrew is already installed:

```bash
brew install git python
git --version
python3 --version
```

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install -y git python3 python3-venv python3-pip
git --version
python3 --version
```

Other Linux distributions may use a different package manager.

## 3. Clone the repository for the first time

These commands work in PowerShell, Command Prompt, macOS Terminal, and Linux terminal:

```bash
git clone <REPOSITORY_URL>
cd <REPOSITORY_DIRECTORY>
git fetch origin
git switch --track origin/feature/seera-audit
```

If the local branch already exists:

```bash
git switch feature/seera-audit
git pull --ff-only origin feature/seera-audit
```

For a private repository, teammates need access and authentication. If the branch does not exist remotely, ask the project owner to push it or confirm the branch name.

## 4. Create a virtual environment and install packages

Run the commands for your operating system from the repository root.

### Windows PowerShell

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install pandas matplotlib openpyxl
```

If PowerShell blocks environment activation, use the environment's Python directly without changing the execution policy:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install pandas matplotlib openpyxl
```

### Windows Command Prompt (cmd.exe)

```bat
py -3 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install pandas matplotlib openpyxl
```

### macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install pandas matplotlib openpyxl
```

### Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install pandas matplotlib openpyxl
```

These are the currently known dependencies. Once the team verifies all imports and versions, add a reviewed `requirements.txt`. Then teammates can install with `python -m pip install -r requirements.txt`.

## 5. Put the SEERA workbook in the expected location

The expected path is:

`The_SEERA_Dataset/The SEERA Dataset/Dataset Files/SEERA dataset original raw data.xlsx`

If it is not in the clone, obtain it from the project owner or an authorized source. Preserve the path, file name, and worksheet name. The current worksheet name is `SEERA dataset `, including a trailing space.

**Windows PowerShell**
```powershell
Test-Path "The_SEERA_Dataset\The SEERA Dataset\Dataset Files\SEERA dataset original raw data.xlsx"
```

**Windows Command Prompt**
```bat
if exist "The_SEERA_Dataset\The SEERA Dataset\Dataset Files\SEERA dataset original raw data.xlsx" (echo Dataset found) else (echo Dataset missing)
```

**macOS/Linux**
```bash
test -f "The_SEERA_Dataset/The SEERA Dataset/Dataset Files/SEERA dataset original raw data.xlsx" && echo "Dataset found" || echo "Dataset missing"
```

## 6. Run the analysis scripts

Activate `.venv` using the relevant command above. From the repository root, run scripts sequentially:

```bash
python src/01_inspect_dataset.py
python src/02_validate_dataset.py
python src/03_explore_dataset.py
python src/04_analyze_delays.py
python src/05_check_effort_consistency.py
python src/06_analyze_delay_factors.py
python src/07_create_review_charts.py
```

Expected outputs:

- `outputs/analysis/delay_factor_data_quality.csv`
- `outputs/analysis/delay_factor_summary.csv`
- `outputs/figures/schedule_performance.png`
- `outputs/figures/delay_rates_by_factor.png`

If a script fails, stop and share the full traceback with the project owner.

## 7. Open the generated charts

**Windows PowerShell**
```powershell
Start-Process "outputs/figures/schedule_performance.png"
Start-Process "outputs/figures/delay_rates_by_factor.png"
```

**Windows Command Prompt**
```bat
start "" "outputs\figures\schedule_performance.png"
start "" "outputs\figures\delay_rates_by_factor.png"
```

**macOS**
```bash
open outputs/figures/schedule_performance.png
open outputs/figures/delay_rates_by_factor.png
```

**Linux**
```bash
xdg-open outputs/figures/schedule_performance.png
xdg-open outputs/figures/delay_rates_by_factor.png
```

## 8. Pull later changes (remote → local)

Save, commit, or safely stash local work first. Then run from the repository root:

```bash
git status
git switch feature/seera-audit
git fetch origin
git pull --ff-only origin feature/seera-audit
```

If the pull is blocked by local changes or diverged history, stop and resolve the situation. Do not use `git reset --hard` unless you intentionally want to discard local work.

If `requirements.txt` is updated in the repository, activate the virtual environment and run:

```bash
python -m pip install -r requirements.txt
```

## 9. Troubleshooting

- **`ModuleNotFoundError`:** activate `.venv` and install the missing package with `python -m pip`.
- **Python command not found:** Windows can try `py --version`; macOS/Linux can try `python3 --version`.
- **Workbook not found:** check the working directory and exact path, including spaces and capitalization.
- **PowerShell activation blocked:** use `.\\.venv\\Scripts\\python.exe` directly as shown above.
- **Local changes block pull:** inspect `git status`; commit or safely stash the work.
- **Branch not found:** run `git branch -a` and ask the project owner to verify the branch name.

## 10. Review-readiness checklist

- [ ] Project owner committed and pushed the required scripts and outputs.
- [ ] Teammates can access the repository and branch.
- [ ] Each teammate has an authorized copy of the source workbook.
- [ ] Python environment and dependencies are installed.
- [ ] All scripts run sequentially from a clean checkout.
- [ ] Both charts and both CSV files are generated.
- [ ] Team members understand their real contributions, the schedule-variance formula, and the limitations.
- [ ] Dataset provenance, permissions, and attribution are documented.
