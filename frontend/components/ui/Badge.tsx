import React from "react";

interface BadgeProps {
  children: React.ReactNode;
  variant?: "default" | "gold" | "green" | "red" | "blue";
  size?: "sm" | "md";
}

const variants = {
  default: "border-white/20 text-white/50",
  gold:    "border-amber-500/40 text-amber-400",
  green:   "border-emerald-500/40 text-emerald-400",
  red:     "border-red-500/40 text-red-400",
  blue:    "border-blue-500/40 text-blue-400",
};

export function Badge({ children, variant = "default", size = "sm" }: BadgeProps) {
  return (
    <span className={`
      inline-flex items-center border font-mono tracking-widest uppercase
      ${size === "sm" ? "text-[9px] px-2 py-0.5" : "text-[11px] px-3 py-1"}
      ${variants[variant]}
    `}>
      {children}
    </span>
  );
}
