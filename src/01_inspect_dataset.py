
from pathlib import Path
import pandas as pd

WORKBOOK = Path(
    "The_SEERA_Dataset/The SEERA Dataset/"
    "Dataset Files/SEERA dataset original raw data.xlsx"
)

if not WORKBOOK.exists():
    raise FileNotFoundError(f"Workbook not found: {WORKBOOK}")

excel_file = pd.ExcelFile(WORKBOOK)

print("Workbook:", WORKBOOK.name)
print("\nNumber of sheets:", len(excel_file.sheet_names))
print("\nSheet names:")


print("\n--- Preliminary Data Quality Audit ---")

for sheet in excel_file.sheet_names:
    data = pd.read_excel(
        WORKBOOK,
        sheet_name=sheet,
        header=None,
        keep_default_na=False,
        dtype=object,
    )

    question_marks = data.eq("?").sum().sum()
    not_applicable = data.eq("N/A").sum().sum()
    blank_cells = data.eq("").sum().sum()

    print(f"\nSheet: {sheet}")
    print(f"  Dimensions: {data.shape}")
    print(f"  '?' markers: {question_marks}")
    print(f"  'N/A' markers: {not_applicable}")
    print(f"  Blank cells: {blank_cells}")
