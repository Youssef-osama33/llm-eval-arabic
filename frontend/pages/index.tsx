/**
 * Arena page — main evaluation interface.
 */

import React from "react";
import { GetStaticProps } from "next";
import Head from "next/head";
import { Layout } from "@/components/Layout";
import { EvalForm } from "@/components/EvalForm";
import { ModelCard } from "@/components/ModelCard";
import { Badge } from "@/components/ui/Badge";
import { useEvaluation } from "@/hooks/useEvaluation";
import { ModelInfo, ModelResponse } from "@/types";

interface Props {
  initialModels: ModelInfo[];
}

export default function ArenaPage({ initialModels }: Props) {
  const { evaluation, streamingTokens, status, error, isLoading, submit, reset } = useEvaluation();

  // Sort responses by overall score descending
  const rankedResponses: ModelResponse[] = React.useMemo(() => {
    if (!evaluation?.model_responses?.length) return [];
    return [...evaluation.model_responses].sort(
      (a, b) => (b.scores.overall ?? -1) - (a.scores.overall ?? -1)
    );
  }, [evaluation]);

  const isStreaming = status === "running" && Object.keys(streamingTokens).length > 0;
  const winner = rankedResponses[0];

  return (
    <>
      <Head>
        <title>Arena — LLM-Eval-Arabic</title>
        <meta name="description" content="Compare Arabic LLMs side by side" />
      </Head>
      <Layout>
        {/* Hero */}
        <div className="relative my-8 border border-amber-500/10 bg-gradient-to-br from-amber-500/[0.03] to-transparent p-10 overflow-hidden">
          <div className="relative z-10">
            <div className="text-[9px] tracking-[6px] text-amber-500/40 mb-3 font-mono">
              المنصة العربية لتقييم نماذج اللغة
            </div>
            <h1 className="text-5xl font-black leading-[1.1] mb-3"
              style={{ fontFamily: "'Cinzel', serif",
                background: "linear-gradient(135deg,#fff 0%,#d4a843 50%,#8b1a1a 100%)",
                WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>
              THE ARABIC<br />LLM BATTLEFIELD
            </h1>
            <p className="text-[13px] text-white/35 max-w-md leading-relaxed">
              Upload technical Arabic prompts. Watch frontier models compete in real-time.
              LLM-as-Judge scoring across 6 linguistic dimensions.
            </p>
            <div className="flex gap-2 mt-4">
              {["DIALECT-AWARE", "LLM-AS-JUDGE", "REAL-TIME", "OPEN SOURCE"].map((b) => (
                <Badge key={b} variant="gold">{b}</Badge>
              ))}
            </div>
          </div>
          {/* Decorative Arabic */}
          <div className="absolute right-12 top-1/2 -translate-y-1/2 text-[100px] text-amber-500/[0.04] pointer-events-none select-none"
            style={{ fontFamily: "'Scheherazade New', serif" }}>
            قَيِّم
          </div>
        </div>

        {/* Main grid */}
        <div className="grid grid-cols-[340px_1fr] gap-5 items-start">

          {/* Left panel */}
          <EvalForm
            models={initialModels}
            onSubmit={submit}
            isLoading={isLoading}
          />

          {/* Right panel */}
          <div>
            {error && (
              <div className="border border-red-500/30 bg-red-500/10 p-4 text-red-400 text-sm mb-4">
                ⚠ {error}
                <button onClick={reset} className="ml-3 text-white/40 hover:text-white underline text-xs">Reset</button>
              </div>
            )}

            {/* Running state */}
            {isLoading && !rankedResponses.length && !Object.keys(streamingTokens).length && (
              <div className="border border-amber-500/10 flex flex-col items-center justify-center min-h-[400px] gap-4">
                <div className="w-12 h-12 border-2 border-amber-500/20 border-t-amber-500 rounded-full animate-spin" />
                <div className="text-[11px] text-amber-500/50 tracking-[3px] font-mono">
                  {status === "pending" ? "INITIALIZING..." : "MODELS RUNNING..."}
                </div>
              </div>
            )}

            {/* Streaming in progress */}
            {isStreaming && !rankedResponses.length && (
              <div>
                {Object.entries(streamingTokens).map(([modelId, text], i) => {
                  const model = initialModels.find((m) => m.id === modelId);
                  if (!model) return null;
                  const fakeResp: ModelResponse = {
                    model_id: modelId,
                    model_name: model.name,
                    provider: model.provider,
                    response_text: null,
                    latency_ms: null,
                    token_count: null,
                    cost_usd: null,
                    error: null,
                    scores: { arabic_quality: null, accuracy: null, dialect_adherence: null,
                      technical_precision: null, completeness: null, cultural_sensitivity: null, overall: null },
                    arabic_metrics: null,
                  };
                  return (
                    <ModelCard
                      key={modelId}
                      response={fakeResp}
                      rank={i}
                      streamingText={text}
                      isStreaming
                    />
                  );
                })}
              </div>
            )}

            {/* Empty state */}
            {!isLoading && !rankedResponses.length && !error && (
              <div className="border border-dashed border-white/[0.06] flex flex-col items-center justify-center min-h-[500px] gap-3">
                <div className="text-6xl opacity-[0.07]" style={{ fontFamily: "'Scheherazade New', serif" }}>ميزان</div>
                <div className="text-[11px] text-white/15 tracking-[3px] font-mono">AWAITING EVALUATION</div>
                <div className="text-[10px] text-amber-500/20 font-mono">في انتظار التقييم</div>
              </div>
            )}

            {/* Results */}
            {rankedResponses.length > 0 && (
              <div>
                {/* Winner summary */}
                {winner && status === "completed" && (
                  <div className="border border-amber-500/20 bg-gradient-to-r from-amber-500/10 to-transparent p-4 flex items-center gap-4 mb-4">
                    <span className="text-2xl">🏆</span>
                    <div>
                      <div className="text-[9px] tracking-[3px] text-amber-500/50 font-mono">BATTLE WINNER</div>
                      <div className="text-base font-bold text-amber-400" style={{ fontFamily: "'Cinzel', serif" }}>
                        {winner.model_name}
                        {" "}·{" "}
                        {winner.scores.overall?.toFixed(2)}/10
                      </div>
                    </div>
                    <button
                      onClick={reset}
                      className="ml-auto text-[9px] border border-white/10 text-white/30 px-3 py-1.5 hover:border-white/20 hover:text-white/50 tracking-widest font-mono"
                    >
                      NEW EVAL
                    </button>
                  </div>
                )}

                {/* Model cards grid */}
                <div className={`grid gap-4 ${rankedResponses.length === 2 ? "grid-cols-2" : rankedResponses.length >= 3 ? "grid-cols-3" : "grid-cols-1"}`}>
                  {rankedResponses.map((resp, i) => (
                    <ModelCard
                      key={resp.model_id}
                      response={resp}
                      rank={i}
                      streamingText={streamingTokens[resp.model_id]}
                      isStreaming={isLoading}
                    />
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </Layout>
    </>
  );
}

export const getStaticProps: GetStaticProps = async () => {
  // Provide fallback model list if API not available at build time
  const fallbackModels: ModelInfo[] = [
    { id: "gpt-4o",           name: "GPT-4o",           provider: "OpenAI",      tier: "flagship",     description: "", context_window: 128000, max_output_tokens: 4096, cost_per_1k_input_usd: 0.005, cost_per_1k_output_usd: 0.015, supports_arabic: true, arabic_native: false, available: true },
    { id: "claude-3-5-sonnet",name: "Claude 3.5 Sonnet",provider: "Anthropic",   tier: "flagship",     description: "", context_window: 200000, max_output_tokens: 8096, cost_per_1k_input_usd: 0.003, cost_per_1k_output_usd: 0.015, supports_arabic: true, arabic_native: false, available: true },
    { id: "gemini-1.5-pro",   name: "Gemini 1.5 Pro",  provider: "Google",      tier: "flagship",     description: "", context_window: 1000000,max_output_tokens: 8192, cost_per_1k_input_usd: 0.00125,cost_per_1k_output_usd: 0.005, supports_arabic: true, arabic_native: false, available: true },
    { id: "jais-30b",         name: "Jais 30B",         provider: "G42 / MBZUAI",tier: "arabic-native",description: "", context_window: 4096,   max_output_tokens: 2048, cost_per_1k_input_usd: 0.001, cost_per_1k_output_usd: 0.002, supports_arabic: true, arabic_native: true,  available: true },
    { id: "llama-3-70b",      name: "LLaMA 3 70B",     provider: "Meta",        tier: "open-source",  description: "", context_window: 8192,   max_output_tokens: 2048, cost_per_1k_input_usd: 0.0004,cost_per_1k_output_usd: 0.0008,supports_arabic: true, arabic_native: false, available: true },
    { id: "mistral-large",    name: "Mistral Large",   provider: "Mistral AI",  tier: "challenger",   description: "", context_window: 32768,  max_output_tokens: 4096, cost_per_1k_input_usd: 0.002, cost_per_1k_output_usd: 0.006, supports_arabic: true, arabic_native: false, available: true },
  ];

  try {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"}/api/v1/models`);
    if (res.ok) {
      const models = await res.json();
      return { props: { initialModels: models }, revalidate: 300 };
    }
  } catch {
    // Use fallback
  }

  return { props: { initialModels: fallbackModels }, revalidate: 60 };
};
