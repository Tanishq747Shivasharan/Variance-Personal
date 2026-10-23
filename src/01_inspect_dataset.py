
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


main_data = pd.read_excel(
    WORKBOOK,
    sheet_name="SEERA dataset ",
    header=1,
    keep_default_na=False,
    na_filter=False,
    dtype=object,
)

print("\n--- Main Dataset Audit ---")
print("Dimensions:", main_data.shape)
print("Number of attributes:", len(main_data.columns))

# Validate project identifiers.
project_ids = main_data["ProjID"]

print("Missing project IDs:", project_ids.eq("").sum())
print("Duplicate project IDs:", project_ids.duplicated().sum())
print("Unique project IDs:", project_ids.nunique())

# Count original data markers separately.
question_marks = main_data.eq("?").sum().sum()
not_applicable = main_data.eq("N/A").sum().sum()
blank_cells = main_data.eq("").sum().sum()
pandas_missing = main_data.isna().sum().sum()

total_cells = main_data.shape[0] * main_data.shape[1]
missing_percentage = (question_marks / total_cells) * 100

print("\n--- Missing-Value Audit ---")
print("Question-mark markers:", question_marks)
print("N/A markers:", not_applicable)
print("Blank cells:", blank_cells)
print("Pandas missing values:", pandas_missing)
print("Total project-data cells:", total_cells)
print(f"Question-mark marker percentage: {missing_percentage:.2f}%")

print("\n--- Sample Records ---")
print(main_data.iloc[:5, :10].to_string(index=False))
