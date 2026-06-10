export type ForecastModel = "prophet" | "linear_regression" | "random_forest";
export type ForecastHorizon = 7 | 30 | 90 | 365;

export type UploadSummary = {
  filename: string;
  rows_received: number;
  rows_after_cleaning: number;
  date_column: string;
  target_column: string;
  start_date: string;
  end_date: string;
  duplicate_rows_removed: number;
  missing_values_filled: number;
};

export type ForecastResponse = {
  run_id: number;
  model: ForecastModel;
  horizon: number;
  upload_summary: UploadSummary;
  preprocessing_report: {
    missing_values_before: number;
    missing_values_after: number;
    duplicate_rows_removed: number;
    invalid_dates_removed: number;
    negative_targets_clipped: number;
    inferred_frequency: string;
  };
  feature_report: string[];
  metrics: {
    mae: number;
    rmse: number;
    mape: number;
    r2: number;
  };
  kpis: {
    latest_sales: number;
    forecast_total: number;
    forecast_average: number;
    growth_rate: number;
    confidence: string;
  };
  forecast_chart: Array<{ date: string; actual: number | null; forecast: number | null }>;
  seasonality_chart: Array<{ month: string; sales: number }>;
  distribution_chart: Array<{ bucket: string; count: number }>;
  residual_chart: Array<{ date: string; actual: number; forecast: number; residual: number }>;
  insights: string[];
};
