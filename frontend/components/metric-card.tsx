import { ArrowDownRight, ArrowUpRight, Minus } from "lucide-react";

import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";

type MetricCardProps = {
  label: string;
  value: string;
  detail?: string;
  trend?: "up" | "down" | "flat";
};

export function MetricCard({ label, value, detail, trend = "flat" }: MetricCardProps) {
  const Icon = trend === "up" ? ArrowUpRight : trend === "down" ? ArrowDownRight : Minus;

  return (
    <Card className="shadow-none">
      <CardContent className="p-5">
        <div className="flex items-start justify-between gap-4">
          <div className="min-w-0">
            <p className="text-sm text-muted-foreground">{label}</p>
            <p className="mt-2 truncate text-2xl font-semibold tracking-normal">{value}</p>
            {detail ? <p className="mt-2 text-sm text-muted-foreground">{detail}</p> : null}
          </div>
          <span
            className={cn(
              "flex h-8 w-8 shrink-0 items-center justify-center rounded-md border",
              trend === "up" && "border-blue-200 bg-blue-50 text-blue-700",
              trend === "down" && "border-slate-200 bg-slate-50 text-slate-700",
              trend === "flat" && "border-slate-200 bg-white text-slate-500"
            )}
          >
            <Icon className="h-4 w-4" />
          </span>
        </div>
      </CardContent>
    </Card>
  );
}
