import React from "react";
import Head from "next/head";
import { Layout } from "@/components/Layout";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";

const DATASETS = [
  { name: "ArabicMMLU",       prompts: 14042, status: "LIVE", doi: "arXiv:2402.12840", desc: "57 academic subjects in Arabic — university-level mastery" },
  { name: "DialectBench-AR",  prompts: 8640,  status: "LIVE", doi: "arXiv:2403.00891", desc: "Cross-dialect comprehension across 18 regional varieties" },
  { name: "ArabiTechQA",      prompts: 5600,  status: "LIVE", doi: "arXiv:2401.09204", desc: "Technical terminology: engineering, medicine, law, finance" },
  { name: "Jais-Bench",       prompts: 4800,  status: "LIVE", doi: "arXiv:2308.16149", desc: "Native Arabic LLM evaluation by MBZUAI & G42" },
  { name: "TLDR-AR",          prompts: 6200,  status: "BETA", doi: "arXiv:2402.01388", desc: "Arabic summarization quality — news, legal, medical" },
  { name: "ACVA",             prompts: 3200,  status: "BETA", doi: "arXiv:2311.03833", desc: "Arabic Cultural Values Alignment benchmark" },
  { name: "ArabiCode-Eval",   prompts: 1840,  status: "NEW",  doi: "internal",         desc: "Code generation with Arabic instructions & documentation" },
  { name: "ArabiMath-Pro",    prompts: 2400,  status: "NEW",  doi: "internal",         desc: "Mathematical reasoning with Arabic word problems K-12→PhD" },
];

const TOTAL = DATASETS.reduce((a, b) => a + b.prompts, 0);

export default function BenchmarksPage() {
  return (
    <>
      <Head><title>Benchmarks — LLM-Eval-Arabic</title></Head>
      <Layout>
        <div className="py-10">
          <div className="text-center mb-8">
            <div className="text-[9px] tracking-[6px] text-amber-500/40 mb-3 font-mono">EVALUATION ARSENAL</div>
            <h1 className="text-4xl font-black text-amber-400 mb-2" style={{ fontFamily: "'Cinzel', serif" }}>
              BENCHMARK DATASETS
            </h1>
            <p className="text-white/30 text-sm">{TOTAL.toLocaleString()} total prompts · {DATASETS.length} curated benchmarks</p>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-4 gap-4 mb-8">
            {[
              { v: TOTAL.toLocaleString(), l: "Total Prompts",  ar: "إجمالي التقييمات" },
              { v: DATASETS.length,        l: "Benchmarks",     ar: "معايير التقييم"   },
              { v: "6",                    l: "Dialects",       ar: "لهجات عربية"      },
              { v: "8",                    l: "Categories",     ar: "فئات التقييم"      },
            ].map((s) => (
              <Card key={s.l} className="p-5 text-center">
                <div className="text-3xl font-black text-amber-400" style={{ fontFamily: "'Cinzel', serif" }}>{s.v}</div>
                <div className="text-[9px] tracking-[2px] text-white/30 mt-1">{s.l}</div>
                <div className="text-[10px] text-amber-500/30 mt-0.5" style={{ fontFamily: "'Scheherazade New', serif" }}>{s.ar}</div>
              </Card>
            ))}
          </div>

          {/* Benchmark grid */}
          <div className="grid grid-cols-2 gap-4">
            {DATASETS.map((b, i) => (
              <Card key={b.name} className="p-5">
                <div className="flex justify-between items-start mb-3">
                  <h3 className="text-[14px] font-bold text-white" style={{ fontFamily: "'Cinzel', serif" }}>{b.name}</h3>
                  <Badge variant={b.status === "LIVE" ? "green" : b.status === "NEW" ? "gold" : "blue"}>
                    {b.status}
                  </Badge>
                </div>
                <p className="text-[11px] text-white/40 mb-4 leading-relaxed">{b.desc}</p>
                <div className="flex justify-between items-center">
                  <div>
                    <span className="text-xl font-black text-amber-400 font-mono">{b.prompts.toLocaleString()}</span>
                    <span className="text-[9px] text-white/25 ml-1.5">PROMPTS</span>
                  </div>
                  <span className="text-[9px] text-white/20 font-mono">{b.doi}</span>
                </div>
                <div className="mt-3 h-[3px] bg-white/[0.04]">
                  <div
                    className="h-full"
                    style={{ width: `${(b.prompts / 14042) * 100}%`,
                      background: "linear-gradient(90deg, #8b1a1a, #d4a843)" }}
                  />
                </div>
              </Card>
            ))}
          </div>
        </div>
      </Layout>
    </>
  );
}
