from pathlib import Path

import pandas as pd


# --------------------------------------------------
# Configuration
# --------------------------------------------------

WORKBOOK = Path(
    "The_SEERA_Dataset/The SEERA Dataset/"
    "Dataset Files/SEERA dataset original raw data.xlsx"
)

SHEET_NAME = "SEERA dataset "


# --------------------------------------------------
# Load dataset
# --------------------------------------------------

def load_dataset() -> pd.DataFrame:
    """Load the main SEERA dataset."""

    if not WORKBOOK.exists():
        raise FileNotFoundError(
            f"SEERA workbook not found: {WORKBOOK}"
        )

    data = pd.read_excel(
        WORKBOOK,
        sheet_name=SHEET_NAME,
        header=1,
        keep_default_na=False,
        na_filter=False,
        dtype=object,
    )

    return data


# --------------------------------------------------
# Prepare numeric columns
# --------------------------------------------------

def prepare_metrics(data: pd.DataFrame) -> pd.DataFrame:
    """Convert relevant columns and calculate performance metrics."""

    data = data.copy()

    numeric_columns = [
        "Estimated  duration",
        "Actual duration",
        "Estimated effort",
        "Actual effort",
    ]

    for column in numeric_columns:
        if column not in data.columns:
            raise ValueError(
                f"Required column is missing: {column}"
            )

        data[column] = pd.to_numeric(
            data[column].replace("", pd.NA),
            errors="coerce",
        )

    # Schedule variance: actual duration minus estimated duration.
    data["Schedule Variance"] = (
        data["Actual duration"] - data["Estimated  duration"]
    )

    # Calculate percentage variance only where estimated duration
    # is valid and greater than zero.
    valid_estimates = data["Estimated  duration"].gt(0)

    data["Schedule Variance (%)"] = pd.NA

    data.loc[valid_estimates, "Schedule Variance (%)"] = (
        data.loc[valid_estimates, "Schedule Variance"]
        / data.loc[valid_estimates, "Estimated  duration"]
    ) * 100

    # Classify schedule performance only when both durations exist.
    valid_durations = (
        data["Estimated  duration"].notna()
        & data["Actual duration"].notna()
    )

    data["Schedule Status"] = "Unclassified"

    data.loc[
        valid_durations & data["Schedule Variance"].gt(0),
        "Schedule Status",
    ] = "Delayed"

    data.loc[
        valid_durations & data["Schedule Variance"].eq(0),
        "Schedule Status",
    ] = "On Schedule"

    data.loc[
        valid_durations & data["Schedule Variance"].lt(0),
        "Schedule Status",
    ] = "Ahead of Schedule"

    # Effort variance: actual effort minus estimated effort.
    data["Effort Variance"] = (
        data["Actual effort"] - data["Estimated effort"]
    )

    valid_effort_estimates = data["Estimated effort"].gt(0)

    data["Effort Variance (%)"] = pd.NA

    data.loc[
        valid_effort_estimates,
        "Effort Variance (%)",
    ] = (
        data.loc[valid_effort_estimates, "Effort Variance"]
        / data.loc[valid_effort_estimates, "Estimated effort"]
    ) * 100

    return data


# --------------------------------------------------
# Report schedule performance
# --------------------------------------------------

def report_schedule_performance(data: pd.DataFrame) -> None:
    """Print descriptive statistics for schedule performance."""

    status_counts = data["Schedule Status"].value_counts()

    total_projects = len(data)
    classified_projects = data["Schedule Status"].ne(
        "Unclassified"
    ).sum()

    delayed_projects = status_counts.get("Delayed", 0)

    print("\n" + "=" * 55)
    print("IT PROJECT DELAY & PERFORMANCE ANALYTICS")
    print("=" * 55)

    print("\n--- Project Overview ---")
    print(f"Total project records: {total_projects}")
    print(f"Projects with valid durations: {classified_projects}")
    print(
        f"Projects not classified: "
        f"{total_projects - classified_projects}"
    )

    print("\n--- Schedule Status ---")

    for status in [
        "Delayed",
        "On Schedule",
        "Ahead of Schedule",
        "Unclassified",
    ]:
        count = status_counts.get(status, 0)

        print(f"{status}: {count}")

    if classified_projects:
        delay_rate = (
            delayed_projects / classified_projects
        ) * 100

        print(
            f"Delay rate among classified projects: "
            f"{delay_rate:.2f}%"
        )

    variance = data["Schedule Variance"].dropna()
    percentage_variance = (
        data["Schedule Variance (%)"].dropna()
    )

    print("\n--- Schedule Variance Statistics ---")

    if not variance.empty:
        print(f"Mean variance: {variance.mean():.2f}")
        print(f"Median variance: {variance.median():.2f}")
        print(f"Minimum variance: {variance.min():.2f}")
        print(f"Maximum variance: {variance.max():.2f}")

    if not percentage_variance.empty:
        print(
            "Mean percentage variance: "
            f"{percentage_variance.mean():.2f}%"
        )

        print(
            "Median percentage variance: "
            f"{percentage_variance.median():.2f}%"
        )


# --------------------------------------------------
# Report effort performance
# --------------------------------------------------

def report_effort_performance(data: pd.DataFrame) -> None:
    """Print descriptive statistics for effort performance."""

    effort_variance = data["Effort Variance"].dropna()
    effort_percentage = data["Effort Variance (%)"].dropna()

    print("\n--- Effort Performance ---")

    print(
        "Projects with valid estimated effort: "
        f"{data['Estimated effort'].notna().sum()}"
    )

    print(
        "Projects with valid actual effort: "
        f"{data['Actual effort'].notna().sum()}"
    )

    if not effort_variance.empty:
        print(
            f"Mean effort variance: "
            f"{effort_variance.mean():.2f}"
        )

        print(
            f"Median effort variance: "
            f"{effort_variance.median():.2f}"
        )

    if not effort_percentage.empty:
        print(
            "Mean effort variance percentage: "
            f"{effort_percentage.mean():.2f}%"
        )


# --------------------------------------------------
# Main execution
# --------------------------------------------------

def main() -> None:
    data = load_dataset()
    analyzed_data = prepare_metrics(data)

    report_schedule_performance(analyzed_data)
    report_effort_performance(analyzed_data)

    print("\nAnalysis completed.")


if __name__ == "__main__":
    main()
