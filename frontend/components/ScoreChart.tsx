/**
 * ScoreChart — SVG radar chart for model score breakdown.
 */

import React from "react";
import { ScoreBreakdown } from "@/types";
import { SCORE_LABELS } from "@/lib/constants";

interface Props {
  scores: ScoreBreakdown;
  color: string;
  size?: number;
}

const DIMS = Object.keys(SCORE_LABELS) as (keyof typeof SCORE_LABELS)[];

export function ScoreChart({ scores, color, size = 130 }: Props) {
  const cx = size / 2;
  const cy = size / 2;
  const r = size / 2 - 20;
  const n = DIMS.length;

  const toXY = (i: number, frac: number) => {
    const angle = (i / n) * Math.PI * 2 - Math.PI / 2;
    return [cx + r * frac * Math.cos(angle), cy + r * frac * Math.sin(angle)] as const;
  };

  const gridPoly = (frac: number) =>
    DIMS.map((_, i) => toXY(i, frac).join(",")).join(" ");

  const dataPoints = DIMS.map((dim, i) => {
    const val = scores[dim] ?? 0;
    return toXY(i, val / 10);
  });
  const dataPoly = dataPoints.map((p) => p.join(",")).join(" ");

  const labelPositions = DIMS.map((_, i) => toXY(i, 1.28));

  return (
    <svg viewBox={`0 0 ${size} ${size}`} width={size} height={size}>
      {/* Grid rings */}
      {[0.25, 0.5, 0.75, 1].map((f) => (
        <polygon
          key={f}
          points={gridPoly(f)}
          fill="none"
          stroke="rgba(255,255,255,0.06)"
          strokeWidth="1"
        />
      ))}
      {/* Spokes */}
      {DIMS.map((_, i) => {
        const [x, y] = toXY(i, 1);
        return (
          <line key={i} x1={cx} y1={cy} x2={x} y2={y}
            stroke="rgba(255,255,255,0.06)" strokeWidth="1" />
        );
      })}
      {/* Data polygon */}
      <polygon
        points={dataPoly}
        fill={`${color}20`}
        stroke={color}
        strokeWidth="1.5"
        strokeLinejoin="round"
      />
      {/* Data points */}
      {dataPoints.map(([x, y], i) => (
        <circle key={i} cx={x} cy={y} r="2.5" fill={color} />
      ))}
      {/* Labels */}
      {labelPositions.map(([x, y], i) => (
        <text
          key={i} x={x} y={y}
          textAnchor="middle" dominantBaseline="middle"
          fontSize="7.5" fill="rgba(255,255,255,0.35)"
          fontFamily="'Scheherazade New', serif"
        >
          {SCORE_LABELS[DIMS[i]]}
        </text>
      ))}
    </svg>
  );
}
