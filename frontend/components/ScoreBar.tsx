/**ScoreBar — animated score bar with Arabic label. */

import React, { useEffect, useState } from "react";

interface Props {
  label: string;
  value: number | null;
  color: string;
  delay?: number;
}

export function ScoreBar({ label, value, color, delay = 0 }: Props) {
  const [width, setWidth] = useState(0);
  const pct = value != null ? value * 10 : 0;

  useEffect(() => {
    const t = setTimeout(() => setWidth(pct), delay + 80);
    return () => clearTimeout(t);
  }, [pct, delay]);

  return (
    <div className="mb-2">
      <div className="flex justify-between items-center mb-1">
        <span className="text-[10px] text-white/40" style={{ fontFamily: "'Scheherazade New', serif" }}>
          {label}
        </span>
        <span className="text-[10px] font-bold font-mono" style={{ color }}>
          {value != null ? value.toFixed(1) : "—"}
        </span>
      </div>
      <div className="h-[3px] bg-white/[0.06] rounded-full overflow-hidden">
        <div
          className="h-full rounded-full transition-all duration-[900ms] ease-[cubic-bezier(0.4,0,0.2,1)]"
          style={{ width: `${width}%`, background: `linear-gradient(90deg, ${color}80, ${color})` }}
        />
      </div>
    </div>
  );
}
