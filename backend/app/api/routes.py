import logging

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from app.core.config import Settings, get_settings
from app.db.database import record_run
from app.models.schemas import ForecastModel, ForecastResponse, HealthResponse
from app.services.data_loader import infer_columns, read_upload
from app.services.forecasting import forecast
from app.services.insights import build_kpis, build_visuals, generate_insights
from app.services.preprocessing import clean_sales_data

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="Forecasta API")


@router.post("/forecast", response_model=ForecastResponse)
async def create_forecast(
    file: UploadFile = File(...),
    horizon: int = Form(30),
    model: ForecastModel = Form("prophet"),
    date_column: str | None = Form(None),
    target_column: str | None = Form(None),
    settings: Settings = Depends(get_settings),
) -> ForecastResponse:
    try:
        if horizon not in {7, 30, 90, 365}:
            raise HTTPException(status_code=422, detail="Horizon must be one of 7, 30, 90, or 365 days.")

        raw_df = await read_upload(file)
        date_col, target_col = infer_columns(raw_df, date_column, target_column)
        cleaned = clean_sales_data(raw_df, date_col, target_col)

        if len(cleaned.frame) < 21:
            raise HTTPException(status_code=422, detail="At least 21 daily observations are required for forecasting.")

        result = forecast(cleaned.frame, model, int(horizon))
        forecast_df = result["forecast"]
        validation_df = result["validation"]
        metrics = result["metrics"]
        visuals = build_visuals(cleaned.frame, forecast_df, validation_df)
        kpis = build_kpis(cleaned.frame, forecast_df, metrics)
        insights = generate_insights(cleaned.frame, forecast_df, metrics, kpis)

        run_id = record_run(
            settings.database_path,
            filename=file.filename or "upload",
            model=str(result["model"]),
            horizon=int(horizon),
            rows_in=len(raw_df),
            rows_clean=len(cleaned.frame),
        )

        return ForecastResponse(
            run_id=run_id,
            model=result["model"],
            horizon=int(horizon),
            upload_summary={
                "filename": file.filename or "upload",
                "rows_received": len(raw_df),
                "rows_after_cleaning": len(cleaned.frame),
                "date_column": date_col,
                "target_column": target_col,
                "start_date": cleaned.frame["date"].min().strftime("%Y-%m-%d"),
                "end_date": cleaned.frame["date"].max().strftime("%Y-%m-%d"),
                "duplicate_rows_removed": cleaned.report["duplicate_rows_removed"],
                "missing_values_filled": cleaned.report["missing_values_filled"],
            },
            preprocessing_report=cleaned.report,
            feature_report=result["feature_report"],
            metrics=metrics,
            kpis=kpis,
            forecast_chart=visuals["forecast_chart"],
            seasonality_chart=visuals["seasonality_chart"],
            distribution_chart=visuals["distribution_chart"],
            residual_chart=visuals["residual_chart"],
            insights=insights,
        )
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Forecast generation failed")
        raise HTTPException(status_code=500, detail=f"Forecast generation failed: {exc}") from exc
