# Forecasta

Forecasta is a full-stack sales and demand forecasting platform. Users upload historical sales data, choose a forecasting model and horizon, then receive cleaned-data summaries, model metrics, charts, and business-friendly insights.

## Stack

- Frontend: Next.js 15, TypeScript, Tailwind CSS, shadcn/ui-style components, Recharts
- Backend: FastAPI, Pydantic, SQLite
- ML: Pandas, NumPy, Scikit-learn, Prophet

## Features

- CSV and XLSX upload with schema validation.
- Data cleaning for missing values, duplicates, invalid dates, negative targets, and date normalization.
- Feature engineering for calendar fields, lags, rolling averages, and seasonality detection.
- Forecasting with Prophet, Random Forest Regressor, and Linear Regression.
- Forecast horizons of 7, 30, 90, and 365 days.
- MAE, RMSE, MAPE, and R2 metrics.
- Historical vs forecast, monthly seasonality, sales distribution, and residual charts.
- Natural language insights for trend, seasonality, inventory planning, and confidence.

## Project Structure

```text
backend/
  app/
    api/            REST routes
    core/           config and logging
    db/             SQLite setup and run logging
    models/         Pydantic schemas
    services/       upload, cleaning, feature, model, insight logic
  sample_data/      example retail sales CSV
frontend/
  app/              Next.js app router pages
  components/       dashboard and UI components
  lib/              API client and utilities
  types/            shared frontend types
docs/
  API.md            API contract
```

## Backend Setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The SQLite database defaults to the operating system temp directory. To use a persistent project-local database, set:

```bash
set FORECASTA_DATABASE_PATH=data/forecasta.db
```

FastAPI documentation is available at:

- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`

Backend verification:

```bash
cd backend
python -m unittest discover
```

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Open `http://127.0.0.1:3000/dashboard`.

Frontend verification:

```bash
npm run lint
npm run build
```

If the API is not running on `127.0.0.1:8000`, set:

```bash
NEXT_PUBLIC_API_URL=http://your-api-host
```

## Sample Dataset

Use `backend/sample_data/retail_sales_sample.csv` or download the sample CSV from the dashboard.

## Screenshots

Drop a screenshot of the empty dashboard and one of the result view into
`frontend/public/screenshots/` (see `frontend/public/screenshots/README.md` for
capture instructions), then reference them from this README.

Expected columns:

- `date`: date-like values.
- `sales`: numeric sales, revenue, units, quantity, or demand values.

Custom column names can be entered in the dashboard before forecasting.

## Deployment

Backend:

```bash
cd backend
python -m pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Frontend:

```bash
cd frontend
npm install
npm run build
npm run start
```

Recommended production settings:

- Run the API behind a reverse proxy with HTTPS.
- Set strict CORS origins in `backend/app/core/config.py`.
- Store uploaded files in object storage if persistence is required.
- Replace SQLite with Postgres for multi-user or high-concurrency deployments.
- Pin environment variables through the target platform rather than committing secrets.
