# Screenshots

This folder holds screenshots of the Forecasta dashboard for the README.

Capture instructions:

1. Run the backend (`uvicorn app.main:app --reload --port 8000`).
2. Run the frontend (`npm run dev`).
3. Open `http://127.0.0.1:3000/dashboard`.
4. Upload `backend/sample_data/retail_sales_sample.csv` with horizon `30` and
   model `prophet`.
5. Capture:
   - `dashboard-empty.png` — initial empty state.
   - `dashboard-result.png` — full dashboard after the forecast loads.

The README references `../docs/screenshots/dashboard-empty.png` and
`../docs/screenshots/dashboard-result.png`. Drop the captured PNGs into
`docs/screenshots/` (create the folder) and update the README image paths if
you prefer a different layout.
