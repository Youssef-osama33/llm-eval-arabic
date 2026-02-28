import React from "react";

interface CardProps {
  children: React.ReactNode;
  className?: string;
  highlight?: boolean;
  onClick?: () => void;
}

export function Card({ children, className = "", highlight = false, onClick }: CardProps) {
  return (
    <div
      onClick={onClick}
      className={`
        relative border bg-white/[0.02] backdrop-blur-sm transition-all duration-200
        ${highlight
          ? "border-amber-500/30 bg-amber-500/[0.03] shadow-[0_0_30px_rgba(217,168,67,0.08)]"
          : "border-white/[0.06] hover:border-white/[0.1]"
        }
        ${onClick ? "cursor-pointer" : ""}
        ${className}
      `}
    >
      {children}
    </div>
  );
}
