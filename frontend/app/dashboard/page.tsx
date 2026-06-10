"use client";

import { BarChart3, Database, LineChart, Sparkles } from "lucide-react";
import { useState } from "react";

import { DistributionChart, ForecastLineChart, ResidualChart, SeasonalityChart } from "@/components/chart-card";
import { MetricCard } from "@/components/metric-card";
import { UploadPanel } from "@/components/upload-panel";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { formatCurrency, formatNumber } from "@/lib/utils";
import type { ForecastResponse } from "@/types/forecast";

const samplePath = "/sample_data/retail_sales_sample.csv";

export default function DashboardPage() {
  const [result, setResult] = useState<ForecastResponse | null>(null);

  return (
    <main className="min-h-screen bg-white">
      <header className="border-b bg-white">
        <div className="mx-auto flex max-w-7xl flex-col gap-6 px-6 py-8 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <div className="flex items-center gap-3">
              <span className="flex h-9 w-9 items-center justify-center rounded-md bg-slate-950 text-white">
                <LineChart className="h-5 w-5" />
              </span>
              <p className="text-sm font-semibold uppercase text-slate-500">Forecasta</p>
            </div>
            <h1 className="mt-6 max-w-3xl text-4xl font-semibold tracking-normal text-slate-950 md:text-5xl">
              Sales forecasting for sharper demand decisions.
            </h1>
            <p className="mt-4 max-w-2xl text-base leading-7 text-slate-600">
              Upload historical sales data, clean it, model demand, and translate predictions into operational insights.
            </p>
          </div>
          <a
            href={samplePath}
            download
            className="inline-flex h-10 items-center justify-center rounded-md border px-4 text-sm font-medium text-slate-700 hover:bg-slate-50"
          >
            Download sample CSV
          </a>
        </div>
      </header>

      <div className="mx-auto grid max-w-7xl gap-8 px-6 py-8 lg:grid-cols-[390px_1fr]">
        <aside className="space-y-6">
          <UploadPanel onResult={setResult} />
          {result ? <UploadSummary result={result} /> : <EmptySummary />}
        </aside>

        <section className="space-y-8">
          {result ? <DashboardResult result={result} /> : <EmptyDashboard />}
        </section>
      </div>
    </main>
  );
}

function DashboardResult({ result }: { result: ForecastResponse }) {
  const growthTrend = result.kpis.growth_rate > 0 ? "up" : result.kpis.growth_rate < 0 ? "down" : "flat";

  return (
    <>
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <MetricCard label="Latest sales" value={formatCurrency(result.kpis.latest_sales)} detail="Last cleaned observation" />
        <MetricCard label="Forecast total" value={formatCurrency(result.kpis.forecast_total)} detail={`${result.horizon} day horizon`} trend="up" />
        <MetricCard label="Average forecast" value={formatCurrency(result.kpis.forecast_average)} detail="Expected daily demand" />
        <MetricCard
          label="Growth outlook"
          value={`${formatNumber(result.kpis.growth_rate)}%`}
          detail={`${result.kpis.confidence} confidence`}
          trend={growthTrend}
        />
      </div>

      <ForecastLineChart data={result.forecast_chart} />

      <div className="grid gap-6 xl:grid-cols-2">
        <InsightsPanel result={result} />
        <PerformancePanel result={result} />
      </div>

      <div className="grid gap-6 xl:grid-cols-2">
        <SeasonalityChart data={result.seasonality_chart} />
        <DistributionChart data={result.distribution_chart} />
      </div>

      <ResidualChart data={result.residual_chart} />
    </>
  );
}

function InsightsPanel({ result }: { result: ForecastResponse }) {
  return (
    <Card className="shadow-none">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Sparkles className="h-4 w-4 text-blue-600" />
          Insights
        </CardTitle>
        <CardDescription>Business-readable interpretation generated from model output.</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {result.insights.map((insight) => (
            <p key={insight} className="rounded-md border bg-slate-50 px-4 py-3 text-sm leading-6 text-slate-700">
              {insight}
            </p>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

function PerformancePanel({ result }: { result: ForecastResponse }) {
  const metrics = [
    ["MAE", formatCurrency(result.metrics.mae)],
    ["RMSE", formatCurrency(result.metrics.rmse)],
    ["MAPE", `${formatNumber(result.metrics.mape)}%`],
    ["R2 Score", formatNumber(result.metrics.r2)]
  ];

  return (
    <Card className="shadow-none">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <BarChart3 className="h-4 w-4 text-blue-600" />
          Model Performance
        </CardTitle>
        <CardDescription>
          Current run #{result.run_id} using {result.model.replace("_", " ")}.
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-5">
        <div className="grid grid-cols-2 gap-3">
          {metrics.map(([label, value]) => (
            <div key={label} className="rounded-md border px-4 py-3">
              <p className="text-xs uppercase text-muted-foreground">{label}</p>
              <p className="mt-1 text-lg font-semibold">{value}</p>
            </div>
          ))}
        </div>
        <div className="space-y-2">
          {result.feature_report.map((item) => (
            <p key={item} className="text-sm text-slate-600">
              {item}
            </p>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

function UploadSummary({ result }: { result: ForecastResponse }) {
  const report = result.preprocessing_report;

  return (
    <Card className="shadow-none">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Database className="h-4 w-4 text-blue-600" />
          Upload Summary
        </CardTitle>
        <CardDescription>{result.upload_summary.filename}</CardDescription>
      </CardHeader>
      <CardContent className="space-y-3 text-sm">
        <SummaryRow label="Rows received" value={result.upload_summary.rows_received} />
        <SummaryRow label="Rows after cleaning" value={result.upload_summary.rows_after_cleaning} />
        <SummaryRow label="Date range" value={`${result.upload_summary.start_date} to ${result.upload_summary.end_date}`} />
        <SummaryRow label="Date column" value={result.upload_summary.date_column} />
        <SummaryRow label="Target column" value={result.upload_summary.target_column} />
        <SummaryRow label="Duplicates removed" value={report.duplicate_rows_removed} />
        <SummaryRow label="Missing values before" value={report.missing_values_before} />
        <SummaryRow label="Missing values after" value={report.missing_values_after} />
        <SummaryRow label="Invalid dates removed" value={report.invalid_dates_removed} />
        <SummaryRow label="Negative values clipped" value={report.negative_targets_clipped} />
      </CardContent>
    </Card>
  );
}

function SummaryRow({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="flex items-center justify-between gap-4 border-b py-2 last:border-b-0">
      <span className="text-slate-500">{label}</span>
      <span className="text-right font-medium text-slate-900">{value}</span>
    </div>
  );
}

function EmptySummary() {
  return (
    <Card className="shadow-none">
      <CardHeader>
        <CardTitle>Preprocessing Report</CardTitle>
        <CardDescription>Generated after a dataset is uploaded.</CardDescription>
      </CardHeader>
      <CardContent className="space-y-3">
        {["Schema validation", "Missing value handling", "Duplicate removal", "Date normalization"].map((item) => (
          <div key={item} className="rounded-md border bg-slate-50 px-4 py-3 text-sm text-slate-500">
            {item}
          </div>
        ))}
      </CardContent>
    </Card>
  );
}

function EmptyDashboard() {
  return (
    <div className="flex min-h-[620px] items-center justify-center rounded-lg border bg-slate-50 px-6 text-center">
      <div className="max-w-lg">
        <p className="text-sm font-semibold uppercase text-slate-500">Ready for analysis</p>
        <h2 className="mt-3 text-3xl font-semibold tracking-normal text-slate-950">Upload sales history to generate a forecast.</h2>
        <p className="mt-4 text-base leading-7 text-slate-600">
          Forecasta will validate the file, clean the data, engineer time-series features, evaluate the model, and render executive-ready insights.
        </p>
      </div>
    </div>
  );
}
