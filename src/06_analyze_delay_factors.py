"""
SEERA Project Analytics
----------------------
Analyze project characteristics associated with schedule delays.

Outputs:
    outputs/analysis/delay_factor_summary.csv
    outputs/analysis/delay_factor_data_quality.csv

Schedule variance = Actual duration - Estimated duration

Positive variance: Delayed
Zero variance: On schedule
Negative variance: Ahead of schedule
"""

from pathlib import Path

import pandas as pd


# ============================================================
# 1. CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

WORKBOOK_PATH = (
    PROJECT_ROOT
    / "The_SEERA_Dataset"
    / "The SEERA Dataset"
    / "Dataset Files"
    / "SEERA dataset original raw data.xlsx"
)

WORKSHEET_NAME = "SEERA dataset "

OUTPUT_DIR = PROJECT_ROOT / "outputs" / "analysis"

SUMMARY_FILE = OUTPUT_DIR / "delay_factor_summary.csv"
QUALITY_FILE = OUTPUT_DIR / "delay_factor_data_quality.csv"

PROJECT_ID = "ProjID"
ESTIMATED_DURATION = "Estimated duration"
ACTUAL_DURATION = "Actual duration"

MISSING_MARKERS = {
    "", "?", "N/A", "NA", "NAN", "NONE", "NULL"
}

SMALL_GROUP_THRESHOLD = 10


# ============================================================
# 2. VERIFIED CATEGORY MAPPINGS
# ============================================================

CATEGORY_MAPPINGS = {
    "Organization type": {
        1: "Public Software company",
        2: "University",
        3: "Federal Ministry",
        4: "Federal directorates",
        5: "Private Software company",
        6: "Corporate IT department",
        7: "Freelancer",
        8: "Telecommunication company",
    },

    "Size of organization": {
        1: "1–5 employees",
        2: "6–10 employees",
        3: "11–20 employees",
        4: "21–30 employees",
        5: "31–40 employees",
        6: "41–50 employees",
        7: "51–100 employees",
        8: "101–150 employees",
        9: "151–200 employees",
        10: "201–250 employees",
        11: "251–300 employees",
        12: "301–350 employees",
        13: "351–400 employees",
        14: "401–450 employees",
        15: "451–500 employees",
        16: "More than 500 employees",
    },

    "Size of IT department": {
        1: "1–5 employees",
        2: "6–10 employees",
        3: "11–15 employees",
        4: "16–20 employees",
        5: "21–25 employees",
        6: "26–30 employees",
        7: "31–35 employees",
        8: "36–40 employees",
        9: "41–45 employees",
        10: "46–50 employees",
    },

    "Development type": {
        1: "New software development",
        2: "Upgrading existing software",
        3: "Modifying existing software",
        4: "Customization of imported software",
    },

    "Application domain": {
        1: "Banking systems",
        2: "ERP",
        5: "Financial and managerial",
        6: "Web applications",
        7: "Bespoke applications",
    },

    "Project manager experience": {
        1: "Previous experience in similar software systems",
        2: "Previous experience in non-similar software systems",
        3: "No previous experience",
    },

    "Product complexity": {
        1: "Clear and simple",
        2: "Clear with some complexity",
        3: "Complex",
        4: "Very complex algorithms and difficult to understand",
    },
}


# These mappings have not been verified against the codebook.
UNVERIFIED_CODE_COLUMNS = {
    "Development environment adequacy",
    "Degree of risk management",
}


FACTORS_TO_ANALYZE = [
    "Organization type",
    "Size of organization",
    "Size of IT department",
    "Development type",
    "Application domain",
    "Project manager experience",
    "Product complexity",
    "Development environment adequacy",
    "Degree of risk management",
]


# ============================================================
# 3. LOAD AND CLEAN DATA
# ============================================================

def load_dataset():
    """Load the Excel worksheet and normalize column names."""

    if not WORKBOOK_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found:\n{WORKBOOK_PATH}\n"
            "Check the workbook path."
        )

    print("=" * 70)
    print("SEERA: IT PROJECT DELAY ANALYSIS")
    print("=" * 70)

    df = pd.read_excel(
        WORKBOOK_PATH,
        sheet_name=WORKSHEET_NAME,
        header=1,
    )

    # Strip outer whitespace and normalize repeated spaces.
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )

    duplicates = df.columns[df.columns.duplicated()].tolist()

    if duplicates:
        raise ValueError(
            f"Duplicate columns after normalization: {duplicates}"
        )

    required = [
        PROJECT_ID,
        ESTIMATED_DURATION,
        ACTUAL_DURATION,
    ]

    missing = [column for column in required if column not in df.columns]

    if missing:
        raise ValueError(
            f"Required columns are missing: {missing}\n"
            f"Available columns: {df.columns.tolist()}"
        )

    # Remove completely empty rows.
    df = df.dropna(how="all").copy()

    # Normalize common textual missing-value markers.
    for column in df.select_dtypes(
        include=["object", "string"]
    ).columns:
        values = df[column].astype("string").str.strip()

        missing_mask = values.str.upper().isin(MISSING_MARKERS)

        df[column] = values.mask(missing_mask, pd.NA)

    print(f"Workbook: {WORKBOOK_PATH.name}")
    print(f"Worksheet: {WORKSHEET_NAME!r}")
    print(f"Records loaded: {len(df)}")
    print(f"Columns loaded: {len(df.columns)}")

    return df


# ============================================================
# 4. CALCULATE SCHEDULE PERFORMANCE
# ============================================================

def prepare_schedule_data(df):
    """Calculate schedule variance and classify project outcomes."""

    df = df.copy()

    df[ESTIMATED_DURATION] = pd.to_numeric(
        df[ESTIMATED_DURATION],
        errors="coerce",
    )

    df[ACTUAL_DURATION] = pd.to_numeric(
        df[ACTUAL_DURATION],
        errors="coerce",
    )

    invalid_duration = (
        df[ESTIMATED_DURATION].isna()
        | df[ACTUAL_DURATION].isna()
    )

    zero_estimate = df[ESTIMATED_DURATION].eq(0)

    valid_duration = (
        df[ESTIMATED_DURATION].gt(0)
        & df[ACTUAL_DURATION].notna()
    )

    analysis_df = df.loc[valid_duration].copy()

    analysis_df["Schedule variance"] = (
        analysis_df[ACTUAL_DURATION]
        - analysis_df[ESTIMATED_DURATION]
    )

    analysis_df["Schedule variance (%)"] = (
        analysis_df["Schedule variance"]
        / analysis_df[ESTIMATED_DURATION]
        * 100
    )

    analysis_df["Schedule status"] = "On schedule"

    analysis_df.loc[
        analysis_df["Schedule variance"] > 0,
        "Schedule status",
    ] = "Delayed"

    analysis_df.loc[
        analysis_df["Schedule variance"] < 0,
        "Schedule status",
    ] = "Ahead of schedule"

    analysis_df["Delayed"] = (
        analysis_df["Schedule variance"] > 0
    )

    print("\n" + "-" * 70)
    print("SCHEDULE DATA QUALITY")
    print("-" * 70)
    print(f"Original records: {len(df)}")
    print(f"Missing/invalid duration records: {int(invalid_duration.sum())}")
    print(f"Zero estimated-duration records: {int(zero_estimate.sum())}")
    print(f"Records included in analysis: {len(analysis_df)}")

    return analysis_df


# ============================================================
# 5. OVERALL SCHEDULE SUMMARY
# ============================================================

def print_overall_summary(analysis_df):
    """Display the overall schedule performance."""

    if analysis_df.empty:
        raise ValueError(
            "No projects have valid durations and positive "
            "estimated durations."
        )

    total = len(analysis_df)

    delayed = int(analysis_df["Delayed"].sum())

    on_schedule = int(
        (analysis_df["Schedule status"] == "On schedule").sum()
    )

    ahead = int(
        (analysis_df["Schedule status"] == "Ahead of schedule").sum()
    )

    print("\n" + "-" * 70)
    print("OVERALL SCHEDULE PERFORMANCE")
    print("-" * 70)

    print(f"Projects analyzed: {total}")
    print(f"Delayed: {delayed}")
    print(f"On schedule: {on_schedule}")
    print(f"Ahead of schedule: {ahead}")
    print(f"Delay rate: {delayed / total * 100:.2f}%")

    print(
        f"Mean schedule variance: "
        f"{analysis_df['Schedule variance'].mean():.2f}"
    )

    print(
        f"Median schedule variance: "
        f"{analysis_df['Schedule variance'].median():.2f}"
    )

    print(
        f"Minimum schedule variance: "
        f"{analysis_df['Schedule variance'].min():.2f}"
    )

    print(
        f"Maximum schedule variance: "
        f"{analysis_df['Schedule variance'].max():.2f}"
    )

    print(
        f"Mean percentage variance: "
        f"{analysis_df['Schedule variance (%)'].mean():.2f}%"
    )

    print(
        f"Median percentage variance: "
        f"{analysis_df['Schedule variance (%)'].median():.2f}%"
    )


# ============================================================
# 6. CONVERT CODES INTO READABLE LABELS
# ============================================================

def category_label(value, factor):
    """Return a readable category label without inventing mappings."""

    if pd.isna(value):
        return pd.NA

    numeric_value = pd.to_numeric(
        pd.Series([value]),
        errors="coerce",
    ).iloc[0]

    if pd.isna(numeric_value):
        return f"Unrecognized value: {value}"

    code = (
        int(numeric_value)
        if float(numeric_value).is_integer()
        else float(numeric_value)
    )

    if factor in UNVERIFIED_CODE_COLUMNS:
        return f"Code {code} (mapping unverified)"

    mappings = CATEGORY_MAPPINGS.get(factor, {})

    if mappings:
        return mappings.get(code, f"Unmapped code: {code}")

    return f"Code {code}"


# ============================================================
# 7. ANALYZE INDIVIDUAL FACTORS
# ============================================================

def analyze_factor(analysis_df, factor):
    """Summarize delay outcomes for each category of a factor."""

    if factor not in analysis_df.columns:
        print(f"\nWARNING: Factor column not found: {factor}")

        quality = pd.DataFrame([{
            "Factor": factor,
            "Total_projects_analyzed": len(analysis_df),
            "Projects_with_factor_value": 0,
            "Missing_factor_values": len(analysis_df),
            "Mapping_status": "Column missing",
        }])

        return pd.DataFrame(), quality

    columns = [
        PROJECT_ID,
        factor,
        "Delayed",
        "Schedule status",
        "Schedule variance",
        "Schedule variance (%)",
    ]

    factor_df = analysis_df[columns].copy()

    factor_df["Category"] = factor_df[factor].map(
        lambda value: category_label(value, factor)
    )

    missing_mask = factor_df["Category"].isna()

    missing_count = int(missing_mask.sum())

    factor_df = factor_df.loc[~missing_mask].copy()

    mapping_status = (
        "Unverified"
        if factor in UNVERIFIED_CODE_COLUMNS
        else "Partially mapped; unmapped codes checked"
    )

    quality_rows = [{
        "Factor": factor,
        "Total_projects_analyzed": len(analysis_df),
        "Projects_with_factor_value": len(factor_df),
        "Missing_factor_values": missing_count,
        "Mapping_status": mapping_status,
    }]

    if factor_df.empty:
        print(f"\nNo usable values for factor: {factor}")

        return pd.DataFrame(), pd.DataFrame(quality_rows)

    grouped = factor_df.groupby("Category", sort=True)

    summary = grouped.agg(
        Total_projects=(PROJECT_ID, "count"),
        Delayed_projects=("Delayed", "sum"),
        Mean_schedule_variance=("Schedule variance", "mean"),
        Median_schedule_variance=("Schedule variance", "median"),
        Mean_schedule_variance_pct=("Schedule variance (%)", "mean"),
        Median_schedule_variance_pct=("Schedule variance (%)", "median"),
        Ahead_of_schedule_projects=(
            "Schedule status",
            lambda values: (values == "Ahead of schedule").sum(),
        ),
        On_schedule_projects=(
            "Schedule status",
            lambda values: (values == "On schedule").sum(),
        ),
    ).reset_index()

    summary["Delay_rate_pct"] = (
        summary["Delayed_projects"]
        / summary["Total_projects"]
        * 100
    )

    summary["Small_group_warning"] = (
        summary["Total_projects"] < SMALL_GROUP_THRESHOLD
    )

    summary.insert(0, "Factor", factor)

    summary = summary.sort_values(
        ["Delay_rate_pct", "Total_projects"],
        ascending=[False, False],
    ).reset_index(drop=True)

    # Record codes that are present but not in a verified mapping.
    mappings = CATEGORY_MAPPINGS.get(factor, {})

    if mappings:
        observed_codes = pd.to_numeric(
            factor_df[factor],
            errors="coerce",
        ).dropna()

        observed_codes = {
            int(value) if float(value).is_integer() else float(value)
            for value in observed_codes
        }

        for code in sorted(observed_codes - set(mappings)):
            quality_rows.append({
                "Factor": factor,
                "Total_projects_analyzed": len(analysis_df),
                "Projects_with_factor_value": len(factor_df),
                "Missing_factor_values": missing_count,
                "Mapping_status": f"Unmapped code detected: {code}",
            })

    print("\n" + "=" * 70)
    print(f"FACTOR: {factor}")
    print("=" * 70)

    display_columns = [
        "Category",
        "Total_projects",
        "Delayed_projects",
        "Delay_rate_pct",
        "Mean_schedule_variance",
        "Median_schedule_variance",
        "Small_group_warning",
    ]

    print(
        summary[display_columns].to_string(
            index=False,
            formatters={
                "Delay_rate_pct": lambda value: f"{value:.2f}%",
                "Mean_schedule_variance": lambda value: f"{value:.2f}",
                "Median_schedule_variance": lambda value: f"{value:.2f}",
            },
        )
    )

    if missing_count:
        print(f"Missing values for this factor: {missing_count}")

    if factor in UNVERIFIED_CODE_COLUMNS:
        print(
            "NOTE: Category meanings are unverified; "
            "results are grouped by raw code."
        )

    print(
        f"NOTE: Groups with fewer than {SMALL_GROUP_THRESHOLD} "
        "projects require cautious interpretation."
    )

    return summary, pd.DataFrame(quality_rows)


# ============================================================
# 8. RUN THE ANALYSIS AND SAVE REPORTS
# ============================================================

def main():
    """Run the complete factor analysis."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = load_dataset()

    analysis_df = prepare_schedule_data(df)

    print_overall_summary(analysis_df)

    summaries = []
    quality_reports = []

    for factor in FACTORS_TO_ANALYZE:
        summary, quality = analyze_factor(
            analysis_df,
            factor,
        )

        if not summary.empty:
            summaries.append(summary)

        if not quality.empty:
            quality_reports.append(quality)

    if summaries:
        final_summary = pd.concat(
            summaries,
            ignore_index=True,
        )

        final_summary.to_csv(
            SUMMARY_FILE,
            index=False,
        )

        print("\n" + "-" * 70)
        print("FACTOR SUMMARY SAVED")
        print("-" * 70)
        print(SUMMARY_FILE)
        print(f"Rows written: {len(final_summary)}")

    if quality_reports:
        final_quality = pd.concat(
            quality_reports,
            ignore_index=True,
        )

        final_quality.to_csv(
            QUALITY_FILE,
            index=False,
        )

        print("\n" + "-" * 70)
        print("DATA QUALITY REPORT SAVED")
        print("-" * 70)
        print(QUALITY_FILE)
        print(f"Rows written: {len(final_quality)}")

    print("\nAnalysis completed.")
    print(
        "Reminder: associations do not prove causation. "
        "Review category mappings and group sizes before "
        "drawing conclusions."
    )


if __name__ == "__main__":
    main()
