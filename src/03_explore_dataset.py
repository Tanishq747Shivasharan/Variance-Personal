from pathlib import Path
import pandas as pd

WORKBOOK = Path("The_SEERA_Dataset/The SEERA Dataset/"
    "Dataset Files/SEERA dataset original raw data.xlsx")

main_data = pd.read_excel(
    WORKBOOK,
    sheet_name="SEERA dataset ",
    header=1,
    keep_default_na=False,
    na_filter=False,
    dtype=object,
)

# Check dataset dimensions.
print(f"Rows: {main_data.shape[0]}")
print(f"Columns: {main_data.shape[1]}")

# List of column names
print("\n--- Column Names ---")
print(main_data.columns.tolist())