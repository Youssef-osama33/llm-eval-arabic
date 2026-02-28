import React from "react";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "ghost";
  loading?: boolean;
  children: React.ReactNode;
}

export function Button({
  variant = "primary", loading = false,
  children, className = "", disabled, ...props
}: ButtonProps) {
  const base = "relative inline-flex items-center justify-center gap-2 font-mono text-sm tracking-widest uppercase transition-all duration-200 disabled:opacity-40 disabled:cursor-not-allowed focus:outline-none";
  const variants = {
    primary:   "bg-gradient-to-r from-amber-700 via-amber-500 to-amber-700 text-black px-6 py-3 shadow-[0_0_24px_rgba(217,168,67,0.25)] hover:shadow-[0_0_32px_rgba(217,168,67,0.4)] hover:brightness-110 active:scale-[0.98]",
    secondary: "border border-white/10 text-white/60 hover:border-amber-500/40 hover:text-amber-400 px-4 py-2 hover:bg-amber-500/5",
    ghost:     "text-white/40 hover:text-white/80 px-3 py-2",
  };

  return (
    <button
      {...props}
      disabled={disabled || loading}
      className={`${base} ${variants[variant]} ${className}`}
    >
      {loading && (
        <span className="w-3.5 h-3.5 border-2 border-current/30 border-t-current rounded-full animate-spin" />
      )}
      {children}
    </button>
  );
}
