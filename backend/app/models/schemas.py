from typing import Literal

from pydantic import BaseModel, Field


ForecastModel = Literal["prophet", "linear_regression", "random_forest"]
ForecastHorizon = Literal[7, 30, 90, 365]


class UploadSummary(BaseModel):
    filename: str
    rows_received: int
    rows_after_cleaning: int
    date_column: str
    target_column: str
    start_date: str
    end_date: str
    duplicate_rows_removed: int
    missing_values_filled: int


class PreprocessingReport(BaseModel):
    missing_values_before: int
    missing_values_after: int
    duplicate_rows_removed: int
    invalid_dates_removed: int
    negative_targets_clipped: int
    inferred_frequency: str


class MetricSet(BaseModel):
    mae: float = Field(ge=0)
    rmse: float = Field(ge=0)
    mape: float = Field(ge=0)
    r2: float


class KpiMetrics(BaseModel):
    latest_sales: float
    forecast_total: float
    forecast_average: float
    growth_rate: float
    confidence: str


class ChartPoint(BaseModel):
    date: str
    actual: float | None = None
    forecast: float | None = None
    residual: float | None = None


class SeasonalityPoint(BaseModel):
    month: str
    sales: float


class DistributionPoint(BaseModel):
    bucket: str
    count: int


class ForecastResponse(BaseModel):
    run_id: int
    model: ForecastModel
    horizon: int
    upload_summary: UploadSummary
    preprocessing_report: PreprocessingReport
    feature_report: list[str]
    metrics: MetricSet
    kpis: KpiMetrics
    forecast_chart: list[ChartPoint]
    seasonality_chart: list[SeasonalityPoint]
    distribution_chart: list[DistributionPoint]
    residual_chart: list[ChartPoint]
    insights: list[str]


class HealthResponse(BaseModel):
    status: str
    service: str
