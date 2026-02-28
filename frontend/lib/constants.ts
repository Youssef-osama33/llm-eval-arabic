// ── Application constants and lookup maps ─────────────────

export const DIALECTS = [
  { id: "msa",       ar: "الفصحى المعاصرة", en: "Modern Standard Arabic", flag: "🌍" },
  { id: "gulf",      ar: "الخليجية",         en: "Gulf",                  flag: "🇸🇦" },
  { id: "egyptian",  ar: "المصرية",          en: "Egyptian",              flag: "🇪🇬" },
  { id: "levantine", ar: "الشامية",          en: "Levantine",             flag: "🇱🇧" },
  { id: "maghrebi",  ar: "المغاربية",        en: "Maghrebi",              flag: "🇲🇦" },
  { id: "iraqi",     ar: "العراقية",         en: "Iraqi",                 flag: "🇮🇶" },
] as const;

export const CATEGORIES = [
  { id: "dialect_understanding",  ar: "فهم اللهجات",       en: "Dialect Understanding" },
  { id: "technical_terminology",  ar: "المصطلحات التقنية",  en: "Technical Terminology" },
  { id: "reasoning",              ar: "التفكير المنطقي",    en: "Reasoning"             },
  { id: "instruction_following",  ar: "اتباع التعليمات",   en: "Instruction Following" },
  { id: "translation",            ar: "الترجمة",           en: "Translation"           },
  { id: "creative_writing",       ar: "الكتابة الإبداعية", en: "Creative Writing"      },
  { id: "code_generation",        ar: "توليد الكود",        en: "Code Generation"       },
  { id: "culture_heritage",       ar: "الثقافة والتراث",    en: "Culture & Heritage"    },
] as const;

export const MODEL_COLORS: Record<string, string> = {
  "gpt-4o":           "#10a37f",
  "gpt-4-turbo":      "#0ea5e9",
  "claude-3-5-sonnet":"#d97757",
  "gemini-1.5-pro":   "#4285f4",
  "llama-3-70b":      "#a78bfa",
  "mistral-large":    "#f59e0b",
  "jais-30b":         "#34d399",
};

export const SCORE_LABELS: Record<string, string> = {
  arabic_quality:       "جودة اللغة",
  accuracy:             "الدقة",
  dialect_adherence:    "التزام اللهجة",
  technical_precision:  "الدقة التقنية",
  completeness:         "الشمولية",
  cultural_sensitivity: "الحساسية الثقافية",
};

export const SAMPLE_PROMPTS = [
  { text: "اشرح الفرق بين التعلم الآلي التوليدي والتقليدي مع أمثلة من الصناعات العربية", dialect: "msa", category: "technical_terminology" },
  { text: "وش رأيك في توظيف الذكاء الاصطناعي في القطاع المالي الخليجي؟", dialect: "gulf", category: "dialect_understanding" },
  { text: "ممكن تشرحلي إزاي بيشتغل الـ transformer architecture بالمصري البسيط؟", dialect: "egyptian", category: "dialect_understanding" },
  { text: "كيف يمكن للمؤسسات العربية الحفاظ على الهوية الثقافية في عصر الرقمنة؟", dialect: "msa", category: "culture_heritage" },
  { text: "اكتب كود Python لتحليل مشاعر النصوص العربية باستخدام مكتبة Transformers", dialect: "msa", category: "code_generation" },
];

export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
export const WS_BASE_URL  = process.env.NEXT_PUBLIC_WS_URL  || "ws://localhost:8000";
