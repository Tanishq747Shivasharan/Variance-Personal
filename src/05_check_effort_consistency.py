from pathlib import Path

import numpy as np
import pandas as pd


WORKBOOK = Path(
    "The_SEERA_Dataset/The SEERA Dataset/"
    "Dataset Files/SEERA dataset original raw data.xlsx"
)

SHEET_NAME = "SEERA dataset "


def main():
    data = pd.read_excel(
        WORKBOOK,
        sheet_name=SHEET_NAME,
        header=1,
        keep_default_na=False,
        na_filter=False,
        dtype=object,
    )

    columns = [
        "Estimated  duration",
        "Actual duration",
        "Estimated effort",
        "Actual effort",
    ]

    for column in columns:
        data[column] = pd.to_numeric(
            data[column].replace("", pd.NA),
            errors="coerce",
        )

    valid = (
        data["Estimated  duration"].gt(0)
        & data["Estimated effort"].gt(0)
        & data["Actual duration"].notna()
        & data["Actual effort"].notna()
    )

    data = data.loc[valid].copy()

    data["Schedule Variance (%)"] = (
        (
            data["Actual duration"]
            - data["Estimated  duration"]
        )
        / data["Estimated  duration"]
    ) * 100

    data["Effort Variance (%)"] = (
        (
            data["Actual effort"]
            - data["Estimated effort"]
        )
        / data["Estimated effort"]
    ) * 100

    print("\n--- Percentage Variance Comparison ---")

    print(
        "Mean schedule variance (%):",
        round(data["Schedule Variance (%)"].mean(), 4),
    )

    print(
        "Mean effort variance (%):",
        round(data["Effort Variance (%)"].mean(), 4),
    )

    print(
        "Median schedule variance (%):",
        round(data["Schedule Variance (%)"].median(), 4),
    )

    print(
        "Median effort variance (%):",
        round(data["Effort Variance (%)"].median(), 4),
    )

    differences = (
        data["Schedule Variance (%)"]
        - data["Effort Variance (%)"]
    )

    print("\n--- Consistency Checks ---")

    print(
        "Projects compared:",
        len(data),
    )

    print(
        "Projects with matching percentages:",
        np.isclose(
            data["Schedule Variance (%)"],
            data["Effort Variance (%)"],
            rtol=1e-5,
            atol=1e-5,
        ).sum(),
    )

    print(
        "Maximum absolute percentage difference:",
        round(differences.abs().max(), 6),
    )

    print("\n--- Sample Records ---")

    print(
        data[
            [
                "Estimated  duration",
                "Actual duration",
                "Estimated effort",
                "Actual effort",
                "Schedule Variance (%)",
                "Effort Variance (%)",
            ]
        ].head(10).to_string(index=False)
    )


if __name__ == "__main__":
    main()
