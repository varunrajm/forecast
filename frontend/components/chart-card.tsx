"use client";

import type { ReactNode } from "react";
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import type { ForecastResponse } from "@/types/forecast";

type ChartCardProps = {
  title: string;
  description: string;
  children: ReactNode;
};

function ChartCard({ title, description, children }: ChartCardProps) {
  return (
    <Card className="shadow-none">
      <CardHeader>
        <CardTitle>{title}</CardTitle>
        <CardDescription>{description}</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="h-80 w-full">{children}</div>
      </CardContent>
    </Card>
  );
}

export function ForecastLineChart({ data }: { data: ForecastResponse["forecast_chart"] }) {
  return (
    <ChartCard title="Historical vs Forecast" description="Recent sales history with the generated forecast horizon.">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} className="chart-grid">
          <CartesianGrid stroke="#e2e8f0" strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="date" minTickGap={32} />
          <YAxis width={56} />
          <Tooltip />
          <Line type="monotone" dataKey="actual" stroke="#0f172a" strokeWidth={2} dot={false} connectNulls={false} />
          <Line type="monotone" dataKey="forecast" stroke="#2563eb" strokeWidth={2} dot={false} connectNulls={false} />
        </LineChart>
      </ResponsiveContainer>
    </ChartCard>
  );
}

export function SeasonalityChart({ data }: { data: ForecastResponse["seasonality_chart"] }) {
  return (
    <ChartCard title="Monthly Seasonality" description="Average demand by calendar month.">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} className="chart-grid">
          <CartesianGrid stroke="#e2e8f0" strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="month" />
          <YAxis width={48} />
          <Tooltip />
          <Bar dataKey="sales" fill="#2563eb" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </ChartCard>
  );
}

export function DistributionChart({ data }: { data: ForecastResponse["distribution_chart"] }) {
  return (
    <ChartCard title="Sales Distribution" description="Frequency of sales values across the cleaned dataset.">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} className="chart-grid">
          <CartesianGrid stroke="#e2e8f0" strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="bucket" hide />
          <YAxis width={48} />
          <Tooltip />
          <Bar dataKey="count" fill="#334155" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </ChartCard>
  );
}

export function ResidualChart({ data }: { data: ForecastResponse["residual_chart"] }) {
  return (
    <ChartCard title="Residual Analysis" description="Validation residuals reveal bias and large misses.">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={data} className="chart-grid">
          <CartesianGrid stroke="#e2e8f0" strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="date" minTickGap={28} />
          <YAxis width={48} />
          <Tooltip />
          <Area type="monotone" dataKey="residual" stroke="#2563eb" fill="#dbeafe" strokeWidth={2} />
        </AreaChart>
      </ResponsiveContainer>
    </ChartCard>
  );
}
