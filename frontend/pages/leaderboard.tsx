import React from "react";
import Head from "next/head";
import { Layout } from "@/components/Layout";
import { MODEL_COLORS } from "@/lib/constants";

const LEADERBOARD_DATA = [
  { id: "claude-3-5-sonnet", name: "Claude 3.5 Sonnet", provider: "Anthropic", scores: { overall: 9.47, arabic: 9.70, dialect: 9.40, technical: 9.20, accuracy: 9.50, culture: 9.40 }, latency: "1.1s" },
  { id: "jais-30b",          name: "Jais 30B",           provider: "G42/MBZUAI",scores: { overall: 9.35, arabic: 9.80, dialect: 9.90, technical: 8.60, accuracy: 8.80, culture: 9.80 }, latency: "1.9s" },
  { id: "gpt-4o",            name: "GPT-4o",             provider: "OpenAI",    scores: { overall: 9.22, arabic: 9.40, dialect: 9.60, technical: 9.30, accuracy: 9.20, culture: 8.90 }, latency: "1.2s" },
  { id: "mistral-large",     name: "Mistral Large",      provider: "Mistral AI",scores: { overall: 8.63, arabic: 8.60, dialect: 8.40, technical: 8.20, accuracy: 8.70, culture: 8.50 }, latency: "1.7s" },
  { id: "gemini-1.5-pro",    name: "Gemini 1.5 Pro",    provider: "Google",    scores: { overall: 8.55, arabic: 8.80, dialect: 8.60, technical: 8.70, accuracy: 8.90, culture: 9.10 }, latency: "1.9s" },
  { id: "llama-3-70b",       name: "LLaMA 3 70B",       provider: "Meta",      scores: { overall: 8.12, arabic: 8.30, dialect: 8.10, technical: 7.90, accuracy: 8.50, culture: 8.00 }, latency: "2.3s" },
];

const MEDALS = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣"];
const COLS = ["overall", "arabic", "dialect", "technical", "accuracy", "culture"] as const;
const COL_LABELS = { overall: "OVERALL", arabic: "ARABIC", dialect: "DIALECT", technical: "TECH", accuracy: "ACCURACY", culture: "CULTURE" };

function scoreColor(v: number) {
  if (v >= 9.5) return "#00ff88";
  if (v >= 9.0) return "#d4a843";
  if (v >= 8.5) return "#f97316";
  return "#ef4444";
}

export default function LeaderboardPage() {
  return (
    <>
      <Head><title>Leaderboard — LLM-Eval-Arabic</title></Head>
      <Layout>
        <div className="py-10">
          <div className="text-center mb-10">
            <div className="text-[9px] tracking-[6px] text-amber-500/40 mb-3 font-mono">GLOBAL RANKINGS // الترتيب العالمي</div>
            <h1 className="text-4xl font-black text-amber-400" style={{ fontFamily: "'Cinzel', serif" }}>
              ARABIC LLM LEADERBOARD
            </h1>
            <p className="text-white/30 mt-2 text-sm">Updated Feb 2026 · 14,000+ Arabic prompts evaluated</p>
          </div>

          <div className="border border-amber-500/10 overflow-hidden">
            {/* Header */}
            <div className="grid gap-px bg-white/[0.04] font-mono text-[8px] tracking-[2px] text-amber-500/40 px-5 py-3"
              style={{ gridTemplateColumns: "50px 1fr 80px 80px 80px 80px 80px 80px 70px" }}>
              <span>#</span>
              <span>MODEL</span>
              {COLS.map((c) => <span key={c}>{COL_LABELS[c]}</span>)}
              <span>LATENCY</span>
            </div>

            {LEADERBOARD_DATA.map((row, i) => {
              const color = MODEL_COLORS[row.id] ?? "#94a3b8";
              return (
                <div
                  key={row.id}
                  className="grid gap-px px-5 py-4 border-b border-white/[0.04] hover:bg-white/[0.02] transition-colors items-center"
                  style={{ gridTemplateColumns: "50px 1fr 80px 80px 80px 80px 80px 80px 70px",
                    background: i === 0 ? "rgba(212,168,67,0.03)" : undefined }}
                >
                  <span className="text-lg">{MEDALS[i]}</span>
                  <div className="flex items-center gap-3">
                    <div className="w-2 h-2 rounded-full" style={{ background: color, boxShadow: `0 0 6px ${color}` }} />
                    <div>
                      <div className="text-[13px] font-bold text-white" style={{ fontFamily: "'Cinzel', serif" }}>{row.name}</div>
                      <div className="text-[9px] text-white/25 tracking-widest">{row.provider}</div>
                    </div>
                  </div>
                  {COLS.map((c) => (
                    <span key={c} className="text-[14px] font-black font-mono" style={{ color: scoreColor(row.scores[c]) }}>
                      {row.scores[c].toFixed(1)}
                    </span>
                  ))}
                  <span className="text-[11px] text-white/30 font-mono">{row.latency}</span>
                </div>
              );
            })}
          </div>

          {/* Legend */}
          <div className="flex gap-6 mt-4 justify-center">
            {[{ color: "#00ff88", label: "≥ 9.5 Exceptional" }, { color: "#d4a843", label: "≥ 9.0 Excellent" },
              { color: "#f97316", label: "≥ 8.5 Strong" }, { color: "#ef4444", label: "< 8.5 Fair" }].map((l) => (
              <div key={l.label} className="flex items-center gap-1.5">
                <div className="w-2 h-2 rounded-full" style={{ background: l.color }} />
                <span className="text-[9px] text-white/30">{l.label}</span>
              </div>
            ))}
          </div>
        </div>
      </Layout>
    </>
  );
}
