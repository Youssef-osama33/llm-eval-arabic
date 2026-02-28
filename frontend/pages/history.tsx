import React, { useEffect, useState } from "react";
import Head from "next/head";
import Link from "next/link";
import { Layout } from "@/components/Layout";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { evaluationsApi } from "@/lib/api";
import { PaginatedEvaluations } from "@/types";

function StatusBadge({ status }: { status: string }) {
  const v = status === "completed" ? "green" : status === "failed" ? "red" : status === "running" ? "gold" : "default";
  return <Badge variant={v as any}>{status.toUpperCase()}</Badge>;
}

export default function HistoryPage() {
  const [data, setData] = useState<PaginatedEvaluations | null>(null);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    evaluationsApi.list({ page, page_size: 20 })
      .then(setData)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [page]);

  return (
    <>
      <Head><title>History — LLM-Eval-Arabic</title></Head>
      <Layout>
        <div className="py-10">
          <div className="text-center mb-8">
            <div className="text-[9px] tracking-[6px] text-amber-500/40 mb-3 font-mono">EVALUATION HISTORY</div>
            <h1 className="text-4xl font-black text-amber-400" style={{ fontFamily: "'Cinzel', serif" }}>
              PAST EVALUATIONS
            </h1>
          </div>

          {loading && (
            <div className="flex justify-center py-20">
              <div className="w-8 h-8 border-2 border-amber-500/20 border-t-amber-500 rounded-full animate-spin" />
            </div>
          )}

          {error && (
            <div className="border border-red-500/30 bg-red-500/10 p-4 text-red-400 text-sm text-center">
              ⚠ {error}
            </div>
          )}

          {data && !loading && (
            <>
              <div className="text-[9px] text-white/25 mb-4 font-mono">{data.total} evaluations total</div>
              <div className="flex flex-col gap-2">
                {data.items.length === 0 && (
                  <div className="text-center py-20 text-white/20 text-sm">No evaluations yet. Run your first evaluation!</div>
                )}
                {data.items.map((item) => (
                  <Link key={item.id} href={`/evaluation/${item.id}`}>
                    <Card className="p-4 hover:border-amber-500/20 cursor-pointer">
                      <div className="flex items-center gap-4">
                        <StatusBadge status={item.status} />
                        <div className="flex-1 min-w-0">
                          <div className="text-[12px] text-white/70 truncate" dir="rtl"
                            style={{ fontFamily: "'Scheherazade New', serif", fontSize: 13 }}>
                            {item.prompt}
                          </div>
                          <div className="flex gap-3 mt-1">
                            <span className="text-[9px] text-white/30">{item.dialect.toUpperCase()}</span>
                            <span className="text-[9px] text-white/20">{item.category}</span>
                            <span className="text-[9px] text-white/20">{item.model_count} models</span>
                          </div>
                        </div>
                        {item.winner_model_id && (
                          <div className="text-right shrink-0">
                            <div className="text-[9px] text-amber-500/50 mb-0.5">WINNER</div>
                            <div className="text-[11px] text-amber-400 font-mono">{item.winner_model_id}</div>
                          </div>
                        )}
                        <div className="text-[9px] text-white/20 shrink-0">
                          {new Date(item.created_at).toLocaleDateString()}
                        </div>
                      </div>
                    </Card>
                  </Link>
                ))}
              </div>

              {/* Pagination */}
              {data.pages > 1 && (
                <div className="flex justify-center gap-2 mt-6">
                  {Array.from({ length: data.pages }, (_, i) => i + 1).map((p) => (
                    <button
                      key={p}
                      onClick={() => setPage(p)}
                      className={`w-8 h-8 text-[11px] font-mono border transition-all ${
                        p === page
                          ? "border-amber-500/40 bg-amber-500/10 text-amber-400"
                          : "border-white/10 text-white/30 hover:border-white/20"
                      }`}
                    >
                      {p}
                    </button>
                  ))}
                </div>
              )}
            </>
          )}
        </div>
      </Layout>
    </>
  );
}
