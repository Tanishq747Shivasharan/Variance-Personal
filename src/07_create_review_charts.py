from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS_DIR = ROOT / "outputs" / "analysis"
FIGURES_DIR = ROOT / "outputs" / "figures"

FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# Preliminary overall project results
status = pd.Series(
    {
        "Delayed": 97,
        "On schedule": 17,
        "Ahead of schedule": 6,
    }
)

fig, ax = plt.subplots(figsize=(9, 5))

bars = ax.bar(status.index, status.values)

ax.set_title("SEERA Project Schedule Performance", fontsize=16)
ax.set_ylabel("Number of projects")
ax.set_ylim(0, max(status.values) * 1.2)
ax.grid(axis="y", alpha=0.25)

for bar, value in zip(bars, status.values):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 1,
        f"{value} ({value / status.sum():.1%})",
        ha="center",
        va="bottom",
    )

fig.tight_layout()
fig.savefig(
    FIGURES_DIR / "schedule_performance.png",
    dpi=180,
    bbox_inches="tight",
)
plt.close(fig)

# Factor-wise delay-rate comparison
csv_path = ANALYSIS_DIR / "delay_factor_summary.csv"
df = pd.read_csv(csv_path)

required = {"Factor", "Category", "Total_projects", "Delay_rate_pct"}
missing = required - set(df.columns)

if missing:
    raise ValueError(f"Missing expected CSV columns: {sorted(missing)}")

# Exclude very small groups from the main comparison.
# Their results remain in the CSV for inspection.
df = df[df["Total_projects"] >= 5].copy()

if not df.empty:
    df = df.sort_values("Delay_rate_pct", ascending=True)

    labels = df["Factor"] + " — " + df["Category"]

    fig, ax = plt.subplots(figsize=(12, max(7, len(df) * 0.32)))

    bars = ax.barh(labels, df["Delay_rate_pct"])

    ax.set_title(
        "Project Delay Rates by Factor and Category",
        fontsize=15,
    )
    ax.set_xlabel("Projects delayed (%)")
    ax.set_xlim(0, 110)
    ax.grid(axis="x", alpha=0.25)

    for bar, value in zip(bars, df["Delay_rate_pct"]):
        ax.text(
            value + 1,
            bar.get_y() + bar.get_height() / 2,
            f"{value:.1f}%",
            va="center",
            fontsize=8,
        )

    fig.tight_layout()
    fig.savefig(
        FIGURES_DIR / "delay_rates_by_factor.png",
        dpi=180,
        bbox_inches="tight",
    )
    plt.close(fig)

print("Charts saved to:", FIGURES_DIR)
