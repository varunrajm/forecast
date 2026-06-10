from io import BytesIO

import pandas as pd
from fastapi import HTTPException, UploadFile


SUPPORTED_EXTENSIONS = {".csv", ".xlsx"}


async def read_upload(file: UploadFile) -> pd.DataFrame:
    filename = file.filename or ""
    extension = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""
    contents = await file.read()

    if not contents:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    if f".{extension}" not in SUPPORTED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only CSV and XLSX files are supported.")

    try:
        if extension == "csv":
            return pd.read_csv(BytesIO(contents))
        return pd.read_excel(BytesIO(contents))
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Could not parse uploaded file: {exc}") from exc


def infer_columns(df: pd.DataFrame, date_column: str | None, target_column: str | None) -> tuple[str, str]:
    normalized = {str(col).strip().lower(): col for col in df.columns}

    if date_column:
        if date_column not in df.columns:
            raise HTTPException(status_code=422, detail=f"Date column '{date_column}' was not found.")
        date_col = date_column
    else:
        date_candidates = ["date", "order_date", "sales_date", "day", "ds"]
        date_col = next((normalized[name] for name in date_candidates if name in normalized), None)
        if date_col is None:
            raise HTTPException(status_code=422, detail="Could not infer a date column. Use a column named date or pass date_column.")

    if target_column:
        if target_column not in df.columns:
            raise HTTPException(status_code=422, detail=f"Target column '{target_column}' was not found.")
        target_col = target_column
    else:
        target_candidates = ["sales", "revenue", "units", "quantity", "y"]
        target_col = next((normalized[name] for name in target_candidates if name in normalized), None)
        if target_col is None:
            numeric_cols = df.select_dtypes(include="number").columns.tolist()
            if not numeric_cols:
                raise HTTPException(status_code=422, detail="Could not infer a numeric sales target column.")
            target_col = numeric_cols[0]

    return str(date_col), str(target_col)
