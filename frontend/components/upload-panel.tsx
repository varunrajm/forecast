"use client";

import { UploadCloud } from "lucide-react";
import { FormEvent, useState } from "react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { requestForecast } from "@/lib/api";
import type { ForecastHorizon, ForecastModel, ForecastResponse } from "@/types/forecast";

type UploadPanelProps = {
  onResult: (result: ForecastResponse) => void;
};

export function UploadPanel({ onResult }: UploadPanelProps) {
  const [file, setFile] = useState<File | null>(null);
  const [model, setModel] = useState<ForecastModel>("prophet");
  const [horizon, setHorizon] = useState<ForecastHorizon>(30);
  const [dateColumn, setDateColumn] = useState("");
  const [targetColumn, setTargetColumn] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!file) {
      setError("Choose a CSV or XLSX file before generating a forecast.");
      return;
    }

    setIsLoading(true);
    setError(null);
    try {
      const result = await requestForecast({
        file,
        model,
        horizon,
        dateColumn: dateColumn || undefined,
        targetColumn: targetColumn || undefined
      });
      onResult(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <Card className="shadow-none">
      <CardHeader>
        <CardTitle>Upload Dataset</CardTitle>
        <CardDescription>CSV or XLSX with a date column and sales, revenue, units, or quantity target.</CardDescription>
      </CardHeader>
      <CardContent>
        <form className="grid gap-5" onSubmit={handleSubmit}>
          <label className="flex min-h-44 cursor-pointer flex-col items-center justify-center rounded-lg border border-dashed bg-slate-50 px-6 text-center transition-colors hover:bg-slate-100">
            <UploadCloud className="h-8 w-8 text-slate-500" />
            <span className="mt-3 text-sm font-medium">{file ? file.name : "Choose file"}</span>
            <span className="mt-1 text-xs text-muted-foreground">Supports .csv and .xlsx</span>
            <Input
              className="sr-only"
              type="file"
              accept=".csv,.xlsx"
              onChange={(event) => setFile(event.target.files?.[0] ?? null)}
            />
          </label>

          <div className="grid gap-4 md:grid-cols-2">
            <div className="space-y-2">
              <label className="text-sm font-medium">Model</label>
              <Select value={model} onValueChange={(value) => setModel(value as ForecastModel)}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="prophet">Prophet</SelectItem>
                  <SelectItem value="random_forest">Random Forest</SelectItem>
                  <SelectItem value="linear_regression">Linear Regression</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">Forecast horizon</label>
              <Select value={String(horizon)} onValueChange={(value) => setHorizon(Number(value) as ForecastHorizon)}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="7">7 days</SelectItem>
                  <SelectItem value="30">30 days</SelectItem>
                  <SelectItem value="90">90 days</SelectItem>
                  <SelectItem value="365">365 days</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="grid gap-4 md:grid-cols-2">
            <Input placeholder="Date column (optional)" value={dateColumn} onChange={(event) => setDateColumn(event.target.value)} />
            <Input placeholder="Target column (optional)" value={targetColumn} onChange={(event) => setTargetColumn(event.target.value)} />
          </div>

          {error ? <p className="rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p> : null}

          <Button type="submit" disabled={isLoading}>
            {isLoading ? "Generating forecast..." : "Generate forecast"}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
