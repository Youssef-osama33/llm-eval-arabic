import React from "react";
import { Header } from "./Header";

interface LayoutProps {
  children: React.ReactNode;
}

function GeometricBg() {
  return (
    <svg
      className="fixed inset-0 w-full h-full opacity-[0.022] pointer-events-none z-0"
      preserveAspectRatio="xMidYMid slice"
    >
      <defs>
        <pattern id="geo" x="0" y="0" width="100" height="100" patternUnits="userSpaceOnUse">
          <polygon
            points="50,5 61,35 94,35 68,54 79,84 50,66 21,84 32,54 6,35 39,35"
            fill="none" stroke="#d4a843" strokeWidth="0.3"
          />
          <circle cx="50" cy="50" r="28" fill="none" stroke="#d4a843" strokeWidth="0.2" />
          <circle cx="50" cy="50" r="14" fill="none" stroke="#d4a843" strokeWidth="0.15" />
          <line x1="50" y1="5" x2="50" y2="95" stroke="#d4a843" strokeWidth="0.1" />
          <line x1="5" y1="50" x2="95" y2="50" stroke="#d4a843" strokeWidth="0.1" />
        </pattern>
      </defs>
      <rect width="100%" height="100%" fill="url(#geo)" />
    </svg>
  );
}

export function Layout({ children }: LayoutProps) {
  return (
    <div className="min-h-screen bg-[#050508] text-white relative">
      <GeometricBg />
      <div className="fixed inset-0 pointer-events-none z-0"
        style={{ background: "repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,0.025) 2px,rgba(0,0,0,0.025) 4px)" }}
      />
      <div className="relative z-10">
        <Header />
        <main className="max-w-[1440px] mx-auto px-6 pb-20">
          {children}
        </main>
      </div>
    </div>
  );
}
