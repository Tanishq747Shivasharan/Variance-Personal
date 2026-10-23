
from pathlib import Path
import pandas as pd

WORKBOOK = Path(
    "The_SEERA_Dataset/The SEERA Dataset/"
    "Dataset Files/SEERA dataset original raw data.xlsx"
)

main_data = pd.read_excel(
    WORKBOOK,
    sheet_name="SEERA dataset ",
    header=1,
    keep_default_na=False,
    na_filter=False,
    dtype=object,
)

print("--- Dataset Validation ---")

# 1. Check dataset dimensions.
print("Rows:", main_data.shape[0])
print("Columns:", main_data.shape[1])

# 2. Check required columns.
required_columns = [
    "ProjID",
    "Estimated  duration",
    "Actual duration",
]

for column in required_columns:
    print(f"{column}: {'Present' if column in main_data.columns else 'MISSING'}")

# 3. Validate project identifiers.
project_ids = pd.to_numeric(main_data["ProjID"], errors="coerce")

print("\n--- Project ID Checks ---")
print("Invalid IDs:", project_ids.isna().sum())
print("Duplicate IDs:", project_ids.duplicated().sum())
print("Unique IDs:", project_ids.nunique())

# 4. Validate duration values.
estimated = pd.to_numeric(
    main_data["Estimated  duration"].replace("", pd.NA),
    errors="coerce",
)

actual = pd.to_numeric(
    main_data["Actual duration"].replace("", pd.NA),
    errors="coerce",
)

print("\n--- Duration Checks ---")
print("Missing/invalid estimates:", estimated.isna().sum())
print("Missing/invalid actual durations:", actual.isna().sum())
print("Non-positive estimates:", (estimated <= 0).sum())
print("Non-positive actual durations:", (actual <= 0).sum())

print("\nValidation script completed.")
