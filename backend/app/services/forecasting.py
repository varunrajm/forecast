import logging
from math import sqrt

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from app.models.schemas import ForecastModel
from app.services.preprocessing import build_feature_frame, create_future_features

logger = logging.getLogger(__name__)

FEATURE_COLUMNS = [
    "year",
    "month",
    "quarter",
    "weekday",
    "day_of_year",
    "lag_1",
    "lag_7",
    "rolling_7",
    "rolling_30",
]


def _mape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    denominator = np.where(y_true == 0, 1, y_true)
    return float(np.mean(np.abs((y_true - y_pred) / denominator)) * 100)


def _metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    return {
        "mae": round(float(mean_absolute_error(y_true, y_pred)), 2),
        "rmse": round(float(sqrt(mean_squared_error(y_true, y_pred))), 2),
        "mape": round(_mape(y_true, y_pred), 2),
        "r2": round(float(r2_score(y_true, y_pred)), 3) if len(y_true) > 1 else 0.0,
    }


def forecast(history: pd.DataFrame, model_name: ForecastModel, horizon: int) -> dict[str, object]:
    featured, feature_report = build_feature_frame(history)
    validation_size = min(max(7, len(featured) // 5), 60)
    train = featured.iloc[:-validation_size] if len(featured) > validation_size + 10 else featured
    valid = featured.iloc[-validation_size:] if len(featured) > validation_size + 10 else featured

    if model_name == "prophet":
        try:
            return _forecast_with_prophet(history, valid, horizon, feature_report)
        except Exception as exc:
            logger.warning("Prophet failed; falling back to random forest. Error: %s", exc)
            model_name = "random_forest"

    estimator = RandomForestRegressor(n_estimators=160, random_state=42) if model_name == "random_forest" else LinearRegression()
    estimator.fit(train[FEATURE_COLUMNS], train["sales"])
    validation_predictions = np.clip(estimator.predict(valid[FEATURE_COLUMNS]), 0, None)
    future_features = create_future_features(featured[["date", "sales"]], horizon)
    future_predictions = np.clip(estimator.predict(future_features[FEATURE_COLUMNS]), 0, None)

    return {
        "model": model_name,
        "feature_report": feature_report,
        "metrics": _metrics(valid["sales"].to_numpy(), validation_predictions),
        "validation": _validation_frame(valid, validation_predictions),
        "forecast": _forecast_frame(future_features["date"], future_predictions),
    }


def _forecast_with_prophet(
    history: pd.DataFrame,
    validation: pd.DataFrame,
    horizon: int,
    feature_report: list[str],
) -> dict[str, object]:
    from prophet import Prophet

    prophet_df = history.rename(columns={"date": "ds", "sales": "y"})[["ds", "y"]]
    has_yearly_history = len(history) >= 365
    model = Prophet(
        yearly_seasonality=has_yearly_history,
        weekly_seasonality=True,
        daily_seasonality=False,
        interval_width=0.8,
    )
    model.fit(prophet_df)

    future = model.make_future_dataframe(periods=horizon, freq="D")
    prediction = model.predict(future)
    merged = prediction[["ds", "yhat"]].merge(prophet_df, on="ds", how="inner")
    valid_dates = validation["date"]
    valid_pred = merged[merged["ds"].isin(valid_dates)]["yhat"].to_numpy()
    valid_true = validation["sales"].to_numpy()
    if len(valid_pred) != len(valid_true):
        valid_pred = merged.tail(len(valid_true))["yhat"].to_numpy()

    forecast_only = prediction.tail(horizon)
    return {
        "model": "prophet",
        "feature_report": feature_report
        + [f"Applied Prophet with weekly seasonality{' and yearly seasonality' if has_yearly_history else ''}."],
        "metrics": _metrics(valid_true, np.clip(valid_pred, 0, None)),
        "validation": _validation_frame(validation, np.clip(valid_pred, 0, None)),
        "forecast": _forecast_frame(forecast_only["ds"], np.clip(forecast_only["yhat"], 0, None)),
    }


def _validation_frame(valid: pd.DataFrame, predictions: np.ndarray) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": valid["date"].dt.strftime("%Y-%m-%d"),
            "actual": valid["sales"].round(2),
            "forecast": np.round(predictions, 2),
            "residual": np.round(valid["sales"].to_numpy() - predictions, 2),
        }
    )


def _forecast_frame(dates: pd.Series, predictions: np.ndarray) -> pd.DataFrame:
    date_series = pd.to_datetime(dates)
    return pd.DataFrame(
        {
            "date": date_series.dt.strftime("%Y-%m-%d"),
            "actual": None,
            "forecast": np.round(predictions, 2),
        }
    )
