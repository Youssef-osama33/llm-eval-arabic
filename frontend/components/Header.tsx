import React from "react";
import Link from "next/link";
import { useRouter } from "next/router";

const TABS = [
  { href: "/",            label: "ARENA",       ar: "الساحة"    },
  { href: "/leaderboard", label: "LEADERBOARD", ar: "الترتيب"   },
  { href: "/benchmarks",  label: "BENCHMARKS",  ar: "المعايير"  },
  { href: "/history",     label: "HISTORY",     ar: "السجل"     },
];

export function Header() {
  const router = useRouter();

  return (
    <header className="sticky top-0 z-50 border-b border-amber-500/10 bg-[#050508]/90 backdrop-blur-2xl">
      <div className="max-w-[1440px] mx-auto px-6 h-14 flex items-center gap-6">

        {/* Logo */}
        <Link href="/" className="flex items-center gap-3 shrink-0 group">
          <div className="w-8 h-8 border border-amber-500/50 flex items-center justify-center rotate-45 group-hover:border-amber-500 transition-colors">
            <span className="-rotate-45 text-amber-500 text-base" style={{ fontFamily: "'Scheherazade New', serif" }}>م</span>
          </div>
          <div>
            <div className="text-[10px] font-bold text-amber-500 tracking-[3px]" style={{ fontFamily: "'Cinzel', serif" }}>
              LLM·EVAL·ARABIC
            </div>
            <div className="text-[8px] text-amber-500/30 tracking-widest">v2.0.0</div>
          </div>
        </Link>

        {/* Nav */}
        <nav className="flex gap-1">
          {TABS.map((t) => {
            const active = router.pathname === t.href;
            return (
              <Link
                key={t.href}
                href={t.href}
                className={`flex flex-col items-center px-3.5 py-2 border text-center transition-all ${
                  active
                    ? "border-amber-500/35 bg-amber-500/10 text-amber-400"
                    : "border-transparent text-white/30 hover:text-white/60 hover:border-white/10"
                }`}
              >
                <span className="text-[9px] tracking-[2px] font-mono font-bold">{t.label}</span>
                <span className="text-[9px]" style={{ fontFamily: "'Scheherazade New', serif" }}>{t.ar}</span>
              </Link>
            );
          })}
        </nav>

        {/* Right side */}
        <div className="ml-auto flex items-center gap-5">
          <div className="flex items-center gap-1.5">
            <div className="w-1.5 h-1.5 rounded-full bg-emerald-400 shadow-[0_0_6px_rgba(52,211,153,0.8)]" />
            <span className="text-[8px] text-white/25 tracking-widest">ONLINE</span>
          </div>
          <a
            href="https://github.com/your-org/llm-eval-arabic"
            target="_blank"
            rel="noopener noreferrer"
            className="text-[9px] border border-white/10 text-white/30 px-3 py-1.5 hover:border-amber-500/30 hover:text-amber-400 transition-all tracking-widest font-mono"
          >
            ⌥ GITHUB
          </a>
        </div>
      </div>
    </header>
  );
}
