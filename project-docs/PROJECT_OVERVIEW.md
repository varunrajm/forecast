# 📊 Forecasta — Project Documentation

> **Full-stack Sales & Demand Forecasting Platform**
> Built with FastAPI (Python) + Next.js 15 (TypeScript)

---

## 🧩 What Is Forecasta?

Forecasta is a production-ready, full-stack web application that allows users to:

1. **Upload** historical sales data (CSV or XLSX)
2. **Clean** the data automatically (missing values, duplicates, invalid dates, negative targets)
3. **Forecast** future demand using ML models (Prophet, Random Forest, Linear Regression)
4. **Visualize** results with interactive charts
5. **Get insights** in plain business language

---

## 🗂️ Project Structure

```
task-1/
├── backend/                  ← Python FastAPI backend
│   ├── app/
│   │   ├── api/routes.py     ← REST endpoints (/api/health, /api/forecast)
│   │   ├── core/
│   │   │   ├── config.py     ← Settings & environment config
│   │   │   └── logging.py    ← Logging configuration
│   │   ├── db/database.py    ← SQLite setup and run logging
│   │   ├── models/schemas.py ← Pydantic request/response models
│   │   └── services/
│   │       ├── data_loader.py    ← CSV/XLSX parsing & column inference
│   │       ├── preprocessing.py  ← Data cleaning & feature engineering
│   │       ├── forecasting.py    ← ML model training & prediction
│   │       └── insights.py       ← KPIs, charts, and NL insights
│   ├── sample_data/
│   │   └── retail_sales_sample.csv
│   ├── requirements.txt
│   └── venv/                 ← Python virtual environment
│
├── frontend/                 ← Next.js 15 frontend
│   ├── app/
│   │   ├── dashboard/page.tsx  ← Main dashboard UI
│   │   ├── layout.tsx          ← Root layout
│   │   └── page.tsx            ← Redirects to /dashboard
│   ├── components/
│   │   ├── chart-card.tsx      ← Recharts chart components
│   │   ├── metric-card.tsx     ← KPI metric cards
│   │   ├── upload-panel.tsx    ← File upload form
│   │   └── ui/                 ← shadcn/ui components (button, card, input, select)
│   ├── lib/
│   │   ├── api.ts              ← Fetch wrapper for backend API
│   │   └── utils.ts            ← cn(), formatCurrency(), formatNumber()
│   ├── types/forecast.ts       ← TypeScript types matching backend schemas
│   └── public/
│       └── sample_data/retail_sales_sample.csv
│
├── docs/API.md               ← API contract documentation
├── project-docs/             ← THIS documentation folder
└── README.md                 ← Quick-start guide
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend Framework | Next.js 15 (App Router) |
| Frontend Language | TypeScript |
| Styling | Tailwind CSS |
| UI Components | shadcn/ui style (Radix UI) |
| Charts | Recharts |
| Backend Framework | FastAPI |
| Backend Language | Python 3.x |
| ML Libraries | Prophet, scikit-learn (Random Forest, Linear Regression) |
| Data Processing | Pandas, NumPy |
| Database | SQLite (via Python sqlite3) |
| Config Management | pydantic-settings |
| Server | Uvicorn (ASGI) |

---

## 🔌 API Endpoints

### `GET /api/health`
Health check — confirms the API is running.

**Response:**
```json
{ "status": "ok", "service": "Forecasta API" }
```

### `POST /api/forecast`
Upload a CSV/XLSX file and get a full forecast result.

**Form Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `file` | File | required | CSV or XLSX file with date + sales columns |
| `horizon` | int | 30 | Days to forecast: 7, 30, 90, or 365 |
| `model` | string | prophet | `prophet`, `random_forest`, or `linear_regression` |
| `date_column` | string | auto | Optional: name of the date column |
| `target_column` | string | auto | Optional: name of the sales column |

**Response:** Full `ForecastResponse` with metrics, charts, KPIs, and insights.

---

## 🤖 Machine Learning Models

### 1. Prophet (Default)
- Meta's time-series forecasting library
- Handles seasonality, holidays, trend changes automatically
- Supports weekly and yearly seasonality
- Falls back to Random Forest if Prophet fails

### 2. Random Forest Regressor
- Ensemble of 160 decision trees
- Uses engineered time features: year, month, quarter, weekday, day_of_year, lag_1, lag_7, rolling_7, rolling_30
- Fast and reliable

### 3. Linear Regression
- Simple baseline model
- Same feature set as Random Forest
- Best for linear trend data

---

## 📊 Metrics Computed

| Metric | Meaning |
|--------|---------|
| MAE | Mean Absolute Error — average prediction error |
| RMSE | Root Mean Squared Error — penalizes large errors |
| MAPE | Mean Absolute Percentage Error — % accuracy |
| R² | Coefficient of determination — explained variance |

---

## 🧹 Data Cleaning Pipeline

1. **Column inference** — auto-detects date and sales columns by name
2. **Date parsing** — converts to datetime, removes invalid dates
3. **Numeric coercion** — fills non-numeric sales with column median
4. **Negative clipping** — clips negative values to 0
5. **Deduplication** — groups by date, sums sales for same-date rows
6. **Resampling** — fills gaps to daily frequency using time interpolation
7. **Feature engineering** — adds lags, rolling averages, calendar fields

---

## 📸 Screenshots

### Dashboard (Empty State)
The landing dashboard before any data is uploaded.

![Dashboard](dashboard_screenshot.png)

### API Documentation (FastAPI Swagger)
Auto-generated interactive API documentation at `http://127.0.0.1:8000/docs`.

![API Docs](api_docs_screenshot.png)

---

## 🐛 Bugs Fixed

| Bug | File | Fix Applied |
|-----|------|-------------|
| **Port mismatch** — Frontend pointed to port `5000`, backend runs on port `8000` | `frontend/lib/api.ts` | Changed default port to `8000` |
| **`typedRoutes` config** — Placed in `experimental` block which triggered a warning in Next.js 15.5 | `frontend/next.config.ts` | Kept at top-level (correct for Next.js 15.5+) |

---

## ▶️ How to Run the Project

### Prerequisites
- Python 3.10+ with virtual environment (`venv/`)
- Node.js 18+ with npm

### Step 1 — Start the Backend

Open a terminal and run:

```powershell
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The API will be live at: **http://127.0.0.1:8000**
Interactive API docs: **http://127.0.0.1:8000/docs**

### Step 2 — Start the Frontend

Open a **second terminal** and run:

```powershell
cd frontend
npm run dev
```

The dashboard will be live at: **http://localhost:3000/dashboard**

### Step 3 — Use the App

1. Open **http://localhost:3000/dashboard** in your browser
2. Click **"Download sample CSV"** to get a test dataset
3. Click **"Choose file"** and upload the CSV
4. Select a **Model** (Prophet recommended) and **Forecast horizon** (e.g., 30 days)
5. Click **"Generate forecast"**
6. Wait ~10–30 seconds for results to appear

---

## 🗑️ Files Cleaned Up

The following are auto-generated/build artifacts that are not needed in source control (already gitignored):
- `backend/venv/` — Python virtual environment
- `backend/__pycache__/` — Python bytecode cache
- `frontend/.next/` — Next.js build output
- `frontend/node_modules/` — Node.js dependencies
- `backend/server.log` / `backend/server.err.log` — Runtime log files

---

## 📦 Environment Variables

### Backend
| Variable | Default | Description |
|----------|---------|-------------|
| `FORECASTA_DATABASE_PATH` | OS temp dir | Path to SQLite database file |
| `FORECASTA_UPLOAD_DIR` | `uploads/` | Directory for uploaded files |
| `FORECASTA_ALLOWED_ORIGINS` | localhost:3000 | CORS allowed origins |

### Frontend
| Variable | Default | Description |
|----------|---------|-------------|
| `NEXT_PUBLIC_API_URL` | `http://127.0.0.1:8000` | Backend API base URL |

---

## 🔗 Quick Reference URLs

| Service | URL |
|---------|-----|
| Frontend Dashboard | http://localhost:3000/dashboard |
| Backend API | http://127.0.0.1:8000 |
| Swagger UI (API Docs) | http://127.0.0.1:8000/docs |
| ReDoc (API Docs) | http://127.0.0.1:8000/redoc |
