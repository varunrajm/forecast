from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class CleaningResult:
    frame: pd.DataFrame
    report: dict[str, int | str]


def clean_sales_data(df: pd.DataFrame, date_column: str, target_column: str) -> CleaningResult:
    rows_before = len(df)
    missing_before = int(df[[date_column, target_column]].isna().sum().sum())

    working = df[[date_column, target_column]].copy()
    working.columns = ["date", "sales"]
    working["date"] = pd.to_datetime(working["date"], errors="coerce", utc=False)
    invalid_dates = int(working["date"].isna().sum())
    working = working.dropna(subset=["date"])

    working["sales"] = pd.to_numeric(working["sales"], errors="coerce")
    median_sales = float(working["sales"].median()) if not working["sales"].dropna().empty else 0.0
    missing_targets = int(working["sales"].isna().sum())
    working["sales"] = working["sales"].fillna(median_sales)

    negative_targets = int((working["sales"] < 0).sum())
    working["sales"] = working["sales"].clip(lower=0)

    working = working.sort_values("date")
    duplicates_before = len(working)
    working = working.groupby("date", as_index=False)["sales"].sum()
    duplicate_rows_removed = duplicates_before - len(working)

    working = working.set_index("date").asfreq("D")
    missing_after_resample = int(working["sales"].isna().sum())
    working["sales"] = working["sales"].interpolate(method="time").ffill().bfill()
    working = working.reset_index()

    missing_after = int(working.isna().sum().sum())
    frequency = "daily" if len(working) > rows_before else "daily-resampled"

    return CleaningResult(
        frame=working,
        report={
            "missing_values_before": missing_before,
            "missing_values_after": missing_after,
            "duplicate_rows_removed": int(duplicate_rows_removed),
            "invalid_dates_removed": invalid_dates,
            "negative_targets_clipped": negative_targets,
            "missing_values_filled": missing_targets + missing_after_resample,
            "inferred_frequency": frequency,
        },
    )


def build_feature_frame(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    featured = df.copy()
    featured["year"] = featured["date"].dt.year
    featured["month"] = featured["date"].dt.month
    featured["quarter"] = featured["date"].dt.quarter
    featured["weekday"] = featured["date"].dt.weekday
    featured["day_of_year"] = featured["date"].dt.dayofyear
    featured["lag_1"] = featured["sales"].shift(1)
    featured["lag_7"] = featured["sales"].shift(7)
    featured["rolling_7"] = featured["sales"].rolling(7).mean()
    featured["rolling_30"] = featured["sales"].rolling(30).mean()
    featured = featured.bfill().ffill().fillna(0)

    monthly_strength = float(featured.groupby("month")["sales"].mean().std() / max(featured["sales"].mean(), 1))
    weekly_strength = float(featured.groupby("weekday")["sales"].mean().std() / max(featured["sales"].mean(), 1))
    report = [
        "Extracted year, month, quarter, weekday, and day-of-year features.",
        "Generated 1-day and 7-day lag features.",
        "Generated 7-day and 30-day rolling averages.",
        f"Detected {'meaningful' if monthly_strength > 0.08 else 'modest'} monthly seasonality.",
        f"Detected {'meaningful' if weekly_strength > 0.06 else 'modest'} weekday seasonality.",
    ]
    return featured, report


def create_future_features(history: pd.DataFrame, horizon: int) -> pd.DataFrame:
    future_dates = pd.date_range(history["date"].max() + pd.Timedelta(days=1), periods=horizon, freq="D")
    rows: list[dict[str, float | int | pd.Timestamp]] = []
    sales_history = history["sales"].tolist()

    for date in future_dates:
        lag_1 = sales_history[-1]
        lag_7 = sales_history[-7] if len(sales_history) >= 7 else lag_1
        rolling_7 = float(np.mean(sales_history[-7:]))
        rolling_30 = float(np.mean(sales_history[-30:]))
        rows.append(
            {
                "date": date,
                "year": date.year,
                "month": date.month,
                "quarter": date.quarter,
                "weekday": date.weekday(),
                "day_of_year": date.dayofyear,
                "lag_1": lag_1,
                "lag_7": lag_7,
                "rolling_7": rolling_7,
                "rolling_30": rolling_30,
            }
        )
        sales_history.append(rolling_7)

    return pd.DataFrame(rows)
