"use client";

import { FormEvent, useMemo, useState } from "react";

type JsonValue =
  | string
  | number
  | boolean
  | null
  | JsonValue[]
  | { [key: string]: JsonValue };

type AnalysisResult = {
  company?: string;
  competitor?: string;
  overview?: Record<string, JsonValue>;
  strategies?: Record<string, JsonValue>;
  creative_clusters?: JsonValue[];
  similar_creatives?: JsonValue[];
  performance?: Record<string, JsonValue>;
  trends?: Record<string, JsonValue>;
  anomalies?: JsonValue[];
  competitor_comparison?: Record<string, JsonValue>;
  blind_spots?: JsonValue[];
  recommendations?: JsonValue[];
};

const API_URL = `${process.env.NEXT_PUBLIC_API_URL}/analyze`;

export default function Home() {
  const [company, setCompany] = useState("Swiggy");
  const [competitor, setCompetitor] = useState("Zomato");
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setResult(null);
    setIsLoading(true);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ company, competitor }),
      });

      const payload = await response.json().catch(() => null);
      if (!response.ok) {
        throw new Error(payload?.detail || "Analysis request failed.");
      }

      setResult(payload);
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Unable to run analysis."
      );
    } finally {
      setIsLoading(false);
    }
  }

  const title = result
    ? `${result.company ?? company} vs ${result.competitor ?? competitor}`
    : "Ad Intelligence";

  return (
    <main className="min-h-screen bg-[#f6f7fb] text-slate-950">
      <section className="border-b border-slate-200 bg-white">
        <div className="mx-auto grid max-w-7xl gap-8 px-5 py-8 lg:grid-cols-[1fr_420px] lg:px-8">
          <div className="flex flex-col justify-between gap-8">
            <div>
              <p className="text-sm font-semibold uppercase tracking-[0.16em] text-cyan-700">
                Meta Ad Library Intelligence
              </p>
              <h1 className="mt-3 max-w-3xl text-4xl font-semibold tracking-normal text-slate-950 md:text-6xl">
                {title}
              </h1>
              <p className="mt-4 max-w-2xl text-base leading-7 text-slate-600">
                Compare public competitor ads, creative themes, campaign gaps,
                and next best actions from one dashboard.
              </p>
            </div>

            <div className="grid gap-3 text-sm text-slate-600 sm:grid-cols-3">
              <Metric label="Source" value="Meta Ad Library" />
              <Metric label="Collector" value="TinyFish" />
              <Metric label="Backend" value="FastAPI" />
            </div>
          </div>

          <form
            onSubmit={handleSubmit}
            className="rounded-lg border border-slate-200 bg-slate-50 p-5 shadow-sm"
          >
            <div className="grid gap-4">
              <label className="grid gap-2 text-sm font-medium text-slate-700">
                Company
                <input
                  value={company}
                  onChange={(event) => setCompany(event.target.value)}
                  className="h-12 rounded-md border border-slate-300 bg-white px-3 text-base text-slate-950 outline-none transition focus:border-cyan-600 focus:ring-4 focus:ring-cyan-100"
                  placeholder="Swiggy"
                  required
                />
              </label>
              <label className="grid gap-2 text-sm font-medium text-slate-700">
                Competitor
                <input
                  value={competitor}
                  onChange={(event) => setCompetitor(event.target.value)}
                  className="h-12 rounded-md border border-slate-300 bg-white px-3 text-base text-slate-950 outline-none transition focus:border-cyan-600 focus:ring-4 focus:ring-cyan-100"
                  placeholder="Zomato"
                  required
                />
              </label>
              <button
                type="submit"
                disabled={isLoading}
                className="h-12 rounded-md bg-slate-950 px-4 text-sm font-semibold text-white transition hover:bg-cyan-800 disabled:cursor-not-allowed disabled:bg-slate-400"
              >
                {isLoading ? "Analyzing ads..." : "Run analysis"}
              </button>
            </div>
            {error ? (
              <p className="mt-4 rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
                {error}
              </p>
            ) : null}
          </form>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-5 py-6 lg:px-8">
        {isLoading ? <LoadingDashboard /> : null}
        {!isLoading && !result ? <EmptyState /> : null}
        {result ? <Dashboard result={result} /> : null}
      </section>
    </main>
  );
}

function Dashboard({ result }: { result: AnalysisResult }) {
  return (
    <div className="grid gap-5">
      <Overview data={result.overview} />

      <div className="grid gap-5 xl:grid-cols-2">
        <Panel title="Strategy Distribution">
          <StrategyView data={result.strategies} />
        </Panel>
        <Panel title="Creative Engagement Potential">
          <PerformanceView data={result.performance} />
        </Panel>
      </div>

      <div className="grid gap-5 xl:grid-cols-[1.1fr_0.9fr]">
        <Panel title="Creative Themes">
          <ListView items={result.creative_clusters} />
        </Panel>
        <Panel title="Trends">
          <GenericObject data={result.trends} />
        </Panel>
      </div>

      <div className="grid gap-5 xl:grid-cols-2">
        <Panel title="Anomalies">
          <ListView items={result.anomalies} emptyText="No anomalies detected." />
        </Panel>
        <Panel title="Competitor Comparison">
          <GenericObject data={result.competitor_comparison} />
        </Panel>
      </div>

      <div className="grid gap-5 xl:grid-cols-2">
        <Panel title="Blind Spots">
          <ListView items={result.blind_spots} />
        </Panel>
        <Panel title="Recommendations">
          <ListView items={result.recommendations} />
        </Panel>
      </div>

      <Panel title="Similar Creatives">
        <ListView items={result.similar_creatives} emptyText="No similar creatives found." />
      </Panel>
    </div>
  );
}

function Overview({ data }: { data?: Record<string, JsonValue> }) {
  const entries = Object.entries(data ?? {});

  return (
    <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
      {entries.map(([key, value]) => (
        <div
          key={key}
          className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm"
        >
          <p className="text-xs font-semibold uppercase tracking-[0.14em] text-slate-500">
            {formatLabel(key)}
          </p>
          <p className="mt-3 text-2xl font-semibold text-slate-950">
            {formatValue(value)}
          </p>
        </div>
      ))}
    </div>
  );
}

function StrategyView({ data }: { data?: Record<string, JsonValue> }) {
  if (!data || Object.keys(data).length === 0) {
    return <EmptyText text="No strategy data returned." />;
  }

  return (
    <div className="grid gap-5 md:grid-cols-2">
      {Object.entries(data).map(([group, value]) => (
        <div key={group} className="grid gap-4">
          <h3 className="text-sm font-semibold uppercase tracking-[0.14em] text-slate-500">
            {formatLabel(group)}
          </h3>
          <GenericObject data={value} />
        </div>
      ))}
    </div>
  );
}

function PerformanceView({ data }: { data?: Record<string, JsonValue> }) {
  const chartData = useMemo(() => {
    if (!data) return [];

    return Object.entries(data).map(([label, value]) => {
      const objectValue = isRecord(value) ? value : {};
      return {
        label,
        value: Number(objectValue.active_ads ?? 0),
      };
    });
  }, [data]);

  return (
    <div className="grid gap-5">
      <BarChart data={chartData} />
      <GenericObject data={data} />
    </div>
  );
}

function Panel({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
      <div className="mb-5 flex items-center justify-between gap-3 border-b border-slate-100 pb-3">
        <h2 className="text-lg font-semibold text-slate-950">{title}</h2>
      </div>
      {children}
    </section>
  );
}

function ListView({
  items,
  emptyText = "No data returned.",
}: {
  items?: JsonValue[];
  emptyText?: string;
}) {
  if (!items || items.length === 0) {
    return <EmptyText text={emptyText} />;
  }

  return (
    <div className="grid gap-3">
      {items.map((item, index) => (
        <div key={index} className="rounded-md border border-slate-200 bg-slate-50 p-4">
          {typeof item === "string" ? (
            <p className="text-sm leading-6 text-slate-700">{item}</p>
          ) : (
            <GenericValue value={item} />
          )}
        </div>
      ))}
    </div>
  );
}

function GenericObject({ data }: { data?: JsonValue }) {
  if (!data || !isRecord(data)) {
    return <GenericValue value={data ?? null} />;
  }

  const entries = Object.entries(data);
  if (entries.length === 0) {
    return <EmptyText text="No data returned." />;
  }

  return (
    <div className="grid gap-3">
      {entries.map(([key, value]) => (
        <div
          key={key}
          className="grid gap-2 rounded-md border border-slate-200 bg-slate-50 p-3"
        >
          <p className="text-xs font-semibold uppercase tracking-[0.12em] text-slate-500">
            {formatLabel(key)}
          </p>
          <GenericValue value={value} />
        </div>
      ))}
    </div>
  );
}

function GenericValue({ value }: { value: JsonValue }) {
  if (Array.isArray(value)) {
    if (value.length === 0) return <EmptyText text="None" />;

    const keywordItems = value.filter(isRecord).filter((item) => "keyword" in item);
    if (keywordItems.length === value.length) {
      return (
        <BarChart
          data={keywordItems.map((item) => ({
            label: String(item.keyword),
            value: Number(item.count ?? 1),
          }))}
        />
      );
    }

    return <ListView items={value} />;
  }

  if (isRecord(value)) {
    const simpleEntries = Object.entries(value).filter(
      ([, item]) => !Array.isArray(item) && !isRecord(item)
    );

    if (simpleEntries.length === Object.keys(value).length) {
      return (
        <div className="grid gap-2">
          {simpleEntries.map(([key, item]) => (
            <div key={key} className="flex items-center justify-between gap-4 text-sm">
              <span className="text-slate-500">{formatLabel(key)}</span>
              <span className="text-right font-medium text-slate-900">
                {formatValue(item)}
              </span>
            </div>
          ))}
        </div>
      );
    }

    return <GenericObject data={value} />;
  }

  return <p className="break-words text-sm leading-6 text-slate-700">{formatValue(value)}</p>;
}

function BarChart({ data }: { data: { label: string; value: number }[] }) {
  const max = Math.max(...data.map((item) => item.value), 1);

  if (data.length === 0) {
    return <EmptyText text="No chart data available." />;
  }

  return (
    <div className="grid gap-3">
      {data.slice(0, 8).map((item) => (
        <div key={item.label} className="grid gap-1">
          <div className="flex items-center justify-between gap-4 text-xs font-medium text-slate-600">
            <span className="truncate">{formatLabel(item.label)}</span>
            <span>{item.value}</span>
          </div>
          <div className="h-2 rounded-full bg-slate-200">
            <div
              className="h-2 rounded-full bg-cyan-600"
              style={{ width: `${Math.max((item.value / max) * 100, 6)}%` }}
            />
          </div>
        </div>
      ))}
    </div>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-md border border-slate-200 bg-slate-50 px-4 py-3">
      <p className="text-xs font-semibold uppercase tracking-[0.14em] text-slate-500">
        {label}
      </p>
      <p className="mt-1 font-semibold text-slate-950">{value}</p>
    </div>
  );
}

function LoadingDashboard() {
  return (
    <div className="grid gap-5">
      <div className="rounded-lg border border-cyan-200 bg-cyan-50 p-5 text-cyan-900">
        Collecting Meta ads with TinyFish and running the ML pipeline. This can
        take a few minutes for live competitor research.
      </div>
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {[0, 1, 2, 3].map((item) => (
          <div key={item} className="h-28 animate-pulse rounded-lg bg-white" />
        ))}
      </div>
      <div className="grid gap-5 xl:grid-cols-2">
        <div className="h-80 animate-pulse rounded-lg bg-white" />
        <div className="h-80 animate-pulse rounded-lg bg-white" />
      </div>
    </div>
  );
}

function EmptyState() {
  return (
    <div className="rounded-lg border border-dashed border-slate-300 bg-white p-8 text-center">
      <h2 className="text-xl font-semibold text-slate-950">Ready for analysis</h2>
      <p className="mx-auto mt-2 max-w-xl text-sm leading-6 text-slate-600">
        Enter a company and competitor above to collect live public ads and
        generate the dashboard.
      </p>
    </div>
  );
}

function EmptyText({ text }: { text: string }) {
  return <p className="text-sm leading-6 text-slate-500">{text}</p>;
}

function isRecord(value: JsonValue | unknown): value is Record<string, JsonValue> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function formatLabel(value: string) {
  return value
    .replace(/_/g, " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function formatValue(value: JsonValue | undefined) {
  if (value === null || value === undefined || value === "") return "None";
  if (typeof value === "boolean") return value ? "Yes" : "No";
  if (Array.isArray(value)) return value.length ? value.join(", ") : "None";
  if (typeof value === "object") return JSON.stringify(value);
  return String(value);
}
