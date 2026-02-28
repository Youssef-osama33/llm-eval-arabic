/**
 * EvalForm — Left panel with prompt input and configuration controls.
 */

import React, { useState } from "react";
import { EvaluationRequest, Dialect, EvalCategory } from "@/types";
import { DIALECTS, CATEGORIES, SAMPLE_PROMPTS } from "@/lib/constants";
import { ModelInfo } from "@/types";
import { Button } from "./ui/Button";

interface Props {
  models: ModelInfo[];
  onSubmit: (req: EvaluationRequest) => void;
  isLoading: boolean;
}

export function EvalForm({ models, onSubmit, isLoading }: Props) {
  const [prompt, setPrompt]               = useState("");
  const [dialect, setDialect]             = useState<Dialect>("msa");
  const [category, setCategory]           = useState<EvalCategory>("technical_terminology");
  const [selectedModels, setSelectedModels] = useState<string[]>(["gpt-4o", "claude-3-5-sonnet"]);
  const [maxTokens, setMaxTokens]         = useState(1024);

  const toggleModel = (id: string) =>
    setSelectedModels((prev) =>
      prev.includes(id)
        ? prev.length > 2 ? prev.filter((m) => m !== id) : prev  // keep at least 2
        : prev.length < 6 ? [...prev, id] : prev
    );

  const handleSubmit = () => {
    if (!prompt.trim() || selectedModels.length < 2) return;
    onSubmit({ prompt: prompt.trim(), dialect, category, models: selectedModels, max_tokens: maxTokens });
  };

  const canSubmit = prompt.trim().length >= 10 && selectedModels.length >= 2 && !isLoading;

  return (
    <div className="flex flex-col gap-3">

      {/* Prompt */}
      <div className="border border-white/[0.08]">
        <div className="flex justify-between items-center px-3 py-2 border-b border-white/[0.06] bg-white/[0.02]">
          <span className="text-[9px] tracking-[3px] text-amber-500/60 font-mono">ARABIC PROMPT</span>
          <span className="text-[10px] text-amber-500/40" style={{ fontFamily: "'Scheherazade New', serif" }}>النص التقييمي</span>
        </div>
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="أدخل نصّك العربي هنا..."
          dir="rtl"
          className="w-full min-h-[110px] bg-transparent border-none p-3.5 text-white/90 placeholder-white/20 resize-none focus:outline-none leading-[1.9]"
          style={{ fontFamily: "'Scheherazade New', serif", fontSize: 14 }}
        />
        <div className="px-3 pb-2.5 border-t border-white/[0.04]">
          <p className="text-[8px] text-white/20 tracking-[2px] mb-2">SAMPLE PROMPTS</p>
          <div className="flex flex-wrap gap-1.5">
            {SAMPLE_PROMPTS.map((s, i) => (
              <button
                key={i}
                onClick={() => { setPrompt(s.text); setDialect(s.dialect as Dialect); setCategory(s.category as EvalCategory); }}
                className="text-[9px] text-amber-500/50 border border-amber-500/15 px-2 py-1 hover:bg-amber-500/10 hover:border-amber-500/30 hover:text-amber-400 transition-all"
                style={{ fontFamily: "'Scheherazade New', serif" }}
              >
                {s.text.slice(0, 20)}…
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Dialect */}
      <div className="border border-white/[0.08] p-3">
        <p className="text-[9px] tracking-[3px] text-amber-500/50 font-mono mb-2.5">DIALECT // اللهجة</p>
        <div className="grid grid-cols-3 gap-1.5">
          {DIALECTS.map((d) => (
            <button
              key={d.id}
              onClick={() => setDialect(d.id as Dialect)}
              className={`text-center py-2 px-1 border text-[9px] transition-all tracking-wide font-mono ${
                dialect === d.id
                  ? "border-amber-500/40 bg-amber-500/10 text-amber-400"
                  : "border-white/[0.06] text-white/30 hover:border-white/20 hover:text-white/50"
              }`}
            >
              <div style={{ fontFamily: "'Scheherazade New', serif", fontSize: 11 }}>{d.ar}</div>
              <div className="text-[8px] mt-0.5 opacity-70">{d.en.split(" ")[0]}</div>
            </button>
          ))}
        </div>
      </div>

      {/* Category */}
      <div className="border border-white/[0.08] p-3">
        <p className="text-[9px] tracking-[3px] text-amber-500/50 font-mono mb-2.5">CATEGORY // الفئة</p>
        <div className="flex flex-col gap-1">
          {CATEGORIES.map((c) => (
            <button
              key={c.id}
              onClick={() => setCategory(c.id as EvalCategory)}
              className={`flex items-center gap-2.5 px-2.5 py-2 border text-left transition-all ${
                category === c.id
                  ? "border-amber-500/30 bg-amber-500/08 text-amber-400"
                  : "border-transparent text-white/30 hover:border-white/[0.08] hover:text-white/50"
              }`}
            >
              <span className="text-[9px] font-mono tracking-widest opacity-60 w-16">{c.en.split(" ")[0].toUpperCase()}</span>
              <span style={{ fontFamily: "'Scheherazade New', serif", fontSize: 12 }}>{c.ar}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Model selection */}
      <div className="border border-white/[0.08] p-3">
        <div className="flex justify-between items-center mb-2.5">
          <p className="text-[9px] tracking-[3px] text-amber-500/50 font-mono">MODELS // النماذج</p>
          <p className="text-[8px] text-white/20">{selectedModels.length}/6 selected</p>
        </div>
        <div className="flex flex-col gap-1.5">
          {models.map((m) => {
            const on = selectedModels.includes(m.id);
            const color = { "OpenAI": "#10a37f", "Anthropic": "#d97757", "Google": "#4285f4",
              "Meta": "#a78bfa", "Mistral AI": "#f59e0b", "G42 / MBZUAI": "#34d399" }[m.provider] ?? "#94a3b8";
            return (
              <div
                key={m.id}
                onClick={() => toggleModel(m.id)}
                className={`flex items-center gap-2.5 p-2 border cursor-pointer transition-all ${
                  on ? "border-white/10 bg-white/[0.03]" : "border-transparent hover:border-white/[0.06]"
                }`}
                style={on ? { borderColor: `${color}40` } : {}}
              >
                <div
                  className={`w-3.5 h-3.5 border-2 flex items-center justify-center text-[8px] shrink-0`}
                  style={{ borderColor: on ? color : "rgba(255,255,255,0.2)", background: on ? color : "transparent", color: "#000" }}
                >
                  {on && "✓"}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="text-[11px] font-bold text-white/80 truncate" style={{ fontFamily: "'Cinzel', serif" }}>{m.name}</div>
                  <div className="text-[8px] text-white/25 tracking-widest">{m.provider}</div>
                </div>
                {m.arabic_native && (
                  <span className="text-[7px] border px-1.5 py-0.5 font-mono" style={{ borderColor: `${color}40`, color }}>ARABIC</span>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Max tokens */}
      <div className="border border-white/[0.08] p-3">
        <div className="flex justify-between mb-2">
          <p className="text-[9px] tracking-[3px] text-amber-500/50 font-mono">MAX TOKENS</p>
          <span className="text-[10px] text-amber-400 font-mono">{maxTokens}</span>
        </div>
        <input
          type="range" min={64} max={2048} step={64}
          value={maxTokens}
          onChange={(e) => setMaxTokens(Number(e.target.value))}
          className="w-full accent-amber-500"
        />
        <div className="flex justify-between text-[8px] text-white/20 mt-1">
          <span>64</span><span>2048</span>
        </div>
      </div>

      {/* Submit */}
      <Button
        onClick={handleSubmit}
        disabled={!canSubmit}
        loading={isLoading}
        className="w-full py-4 text-[11px] tracking-[4px]"
      >
        ⚔ LAUNCH EVALUATION
        <span style={{ fontFamily: "'Scheherazade New', serif", fontSize: 14, letterSpacing: 0 }}>
          أطلِق التقييم
        </span>
      </Button>

      {selectedModels.length < 2 && (
        <p className="text-[10px] text-red-400/70 text-center">Select at least 2 models</p>
      )}
    </div>
  );
}
