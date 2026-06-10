import numpy as np
import pandas as pd


def build_visuals(history: pd.DataFrame, forecast_df: pd.DataFrame, validation_df: pd.DataFrame) -> dict[str, list[dict[str, object]]]:
    recent_history = history.tail(120).copy()
    historical_points = [
        {"date": row.date.strftime("%Y-%m-%d"), "actual": round(float(row.sales), 2), "forecast": None}
        for row in recent_history.itertuples(index=False)
    ]

    seasonality = (
        history.assign(month=history["date"].dt.month_name().str[:3])
        .groupby("month", sort=False)["sales"]
        .mean()
        .reset_index()
    )
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    seasonality["month"] = pd.Categorical(seasonality["month"], month_order, ordered=True)
    seasonality = seasonality.sort_values("month")

    counts, edges = np.histogram(history["sales"], bins=min(12, max(5, len(history) // 15)))
    distribution = [
        {"bucket": f"{edges[i]:.0f}-{edges[i + 1]:.0f}", "count": int(counts[i])}
        for i in range(len(counts))
    ]

    return {
        "forecast_chart": historical_points + forecast_df.to_dict(orient="records"),
        "seasonality_chart": [
            {"month": str(row.month), "sales": round(float(row.sales), 2)}
            for row in seasonality.itertuples(index=False)
        ],
        "distribution_chart": distribution,
        "residual_chart": validation_df[["date", "actual", "forecast", "residual"]].to_dict(orient="records"),
    }


def build_kpis(history: pd.DataFrame, forecast_df: pd.DataFrame, metrics: dict[str, float]) -> dict[str, float | str]:
    latest_sales = float(history["sales"].iloc[-1])
    forecast_total = float(forecast_df["forecast"].sum())
    forecast_average = float(forecast_df["forecast"].mean())
    historical_average = float(history["sales"].tail(len(forecast_df)).mean())
    growth_rate = ((forecast_average - historical_average) / max(historical_average, 1)) * 100
    confidence = "High" if metrics["mape"] < 10 else "Medium" if metrics["mape"] < 25 else "Low"

    return {
        "latest_sales": round(latest_sales, 2),
        "forecast_total": round(forecast_total, 2),
        "forecast_average": round(forecast_average, 2),
        "growth_rate": round(growth_rate, 2),
        "confidence": confidence,
    }


def generate_insights(history: pd.DataFrame, forecast_df: pd.DataFrame, metrics: dict[str, float], kpis: dict[str, float | str]) -> list[str]:
    first_period = history["sales"].head(30).mean()
    last_period = history["sales"].tail(30).mean()
    growth = ((last_period - first_period) / max(first_period, 1)) * 100

    monthly = history.assign(month=history["date"].dt.month_name()).groupby("month")["sales"].mean()
    peak_month = str(monthly.idxmax())
    low_month = str(monthly.idxmin())
    forecast_avg = float(kpis["forecast_average"])
    recent_avg = float(history["sales"].tail(30).mean())
    inventory_delta = ((forecast_avg - recent_avg) / max(recent_avg, 1)) * 100

    trend_word = "expanding" if growth > 5 else "contracting" if growth < -5 else "stable"
    stock_action = "increase" if inventory_delta > 8 else "reduce" if inventory_delta < -8 else "maintain"

    return [
        f"Demand is {trend_word}; the latest 30-day average changed by {growth:.1f}% compared with the opening 30-day period.",
        f"Seasonality peaks in {peak_month} and softens most in {low_month}, which can guide promotion and staffing windows.",
        f"Inventory planning should {stock_action} near-term stock levels; the forecast average is {inventory_delta:.1f}% versus the recent 30-day average.",
        f"Forecast confidence is {kpis['confidence']} based on a validation MAPE of {metrics['mape']:.1f}%.",
    ]
