# Forecasta API

Base URL: `http://127.0.0.1:8000`

Interactive API documentation is available at `/docs` when the FastAPI server is running.

## Health

`GET /api/health`

Returns service status.

## Generate Forecast

`POST /api/forecast`

Multipart form fields:

- `file`: CSV or XLSX dataset.
- `horizon`: one of `7`, `30`, `90`, `365`.
- `model`: one of `prophet`, `linear_regression`, `random_forest`.
- `date_column`: optional explicit date column name.
- `target_column`: optional explicit sales target column name.

Expected dataset schema:

- A date-like column named `date`, `order_date`, `sales_date`, `day`, or `ds`, unless `date_column` is provided.
- A numeric target column named `sales`, `revenue`, `units`, `quantity`, or `y`, unless `target_column` is provided.

The response includes upload summary, preprocessing report, feature engineering report, metrics, KPI cards, chart series, and natural language insights.
