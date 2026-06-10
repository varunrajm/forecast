import type { ForecastHorizon, ForecastModel, ForecastResponse } from "@/types/forecast";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

export async function requestForecast(input: {
  file: File;
  horizon: ForecastHorizon;
  model: ForecastModel;
  dateColumn?: string;
  targetColumn?: string;
}): Promise<ForecastResponse> {
  const form = new FormData();
  form.append("file", input.file);
  form.append("horizon", String(input.horizon));
  form.append("model", input.model);

  if (input.dateColumn) form.append("date_column", input.dateColumn);
  if (input.targetColumn) form.append("target_column", input.targetColumn);

  const response = await fetch(`${API_URL}/api/forecast`, {
    method: "POST",
    body: form
  });

  if (!response.ok) {
    const payload = await response.json().catch(() => null);
    throw new Error(payload?.detail ?? "Forecast request failed.");
  }

  return response.json();
}
