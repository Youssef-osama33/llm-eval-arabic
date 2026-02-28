/**
 * ModelCard — full comparison card for a single model's evaluation result.
 */

import React from "react";
import { ModelResponse } from "@/types";
import { MODEL_COLORS, SCORE_LABELS } from "@/lib/constants";
import { ScoreChart } from "./ScoreChart";
import { ScoreBar } from "./ScoreBar";
import { Card } from "./ui/Card";
import { Badge } from "./ui/Badge";

interface Props {
  response: ModelResponse;
  rank: number;
  streamingText?: string;
  isStreaming?: boolean;
}

const RANK_BADGES = ["🥇", "🥈", "🥉"];

export function ModelCard({ response, rank, streamingText, isStreaming }: Props) {
  const color = MODEL_COLORS[response.model_id] ?? "#94a3b8";
  const overall = response.scores.overall;
  const displayText = streamingText ?? response.response_text;
  const scoreEntries = Object.entries(SCORE_LABELS) as [keyof typeof SCORE_LABELS, string][];

  return (
    <Card
      highlight={rank === 0}
      className="p-4 flex flex-col gap-3 animate-[fadeUp_0.4s_ease_both]"
      style={{ animationDelay: `${rank * 120}ms` } as React.CSSProperties}
    >
      {/* Winner badge */}
      {rank === 0 && (
        <div
          className="absolute -top-px left-1/2 -translate-x-1/2 text-[8px] font-mono tracking-[3px] px-3 py-0.5 text-black"
          style={{ background: color }}
        >
          WINNER
        </div>
      )}

      {/* Header */}
      <div className="flex items-center gap-2.5 mt-1">
        <span className="text-xl">{RANK_BADGES[rank] ?? `#${rank + 1}`}</span>
        <div className="flex-1 min-w-0">
          <div className="text-[13px] font-bold text-white truncate" style={{ fontFamily: "'Cinzel', serif" }}>
            {response.model_name}
          </div>
          <div className="text-[9px] text-white/30 tracking-widest uppercase">{response.provider}</div>
        </div>
        <div className="text-right shrink-0">
          <div className="text-2xl font-black" style={{ color, fontFamily: "'Cinzel', serif" }}>
            {overall != null ? overall.toFixed(1) : "—"}
          </div>
          <div className="text-[8px] text-white/20 tracking-widest">/10</div>
        </div>
      </div>

      {/* Error */}
      {response.error && (
        <div className="text-[11px] text-red-400 bg-red-500/10 border border-red-500/20 p-2.5">
          ⚠ {response.error}
        </div>
      )}

      {/* Response text */}
      {!response.error && (
        <div
          className="text-[12px] text-white/65 leading-relaxed bg-black/30 border border-white/[0.04] p-3 min-h-[72px]"
          dir="rtl"
          style={{ fontFamily: "'Scheherazade New', serif", fontSize: 14, lineHeight: 1.9 }}
        >
          {displayText || <span className="text-white/20 italic">No response</span>}
          {isStreaming && (
            <span className="animate-pulse ml-0.5" style={{ color }}>█</span>
          )}
        </div>
      )}

      {/* Score bars */}
      <div>
        {scoreEntries.map(([key, label], i) => (
          <ScoreBar
            key={key}
            label={label}
            value={response.scores[key]}
            color={color}
            delay={rank * 120 + i * 60}
          />
        ))}
      </div>

      {/* Radar chart + meta */}
      <div className="flex gap-3 items-start">
        <div className="shrink-0">
          <ScoreChart scores={response.scores} color={color} size={120} />
        </div>
        <div className="flex-1 grid grid-cols-2 gap-2">
          {[
            { label: "LATENCY",  value: response.latency_ms != null ? `${response.latency_ms}ms` : "—", warn: (response.latency_ms ?? 0) > 3000 },
            { label: "TOKENS",   value: response.token_count ?? "—" },
            { label: "COST",     value: response.cost_usd != null ? `$${response.cost_usd.toFixed(4)}` : "—" },
            { label: "RANK",     value: `#${rank + 1}` },
          ].map(({ label, value, warn }) => (
            <div key={label} className="bg-white/[0.03] border border-white/[0.05] p-2">
              <div className="text-[7px] text-white/25 tracking-[2px] mb-0.5">{label}</div>
              <div
                className="text-[12px] font-bold font-mono"
                style={{ color: warn ? "#ef4444" : color }}
              >
                {String(value)}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Judge reasoning */}
      {response.scores.reasoning && (
        <div className="text-[10px] text-white/30 border-t border-white/[0.04] pt-2 italic leading-relaxed">
          {response.scores.reasoning}
        </div>
      )}
    </Card>
  );
}
