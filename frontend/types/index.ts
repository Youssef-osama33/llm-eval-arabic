// ── Core types shared across the application ──────────────

export type Dialect = "msa" | "gulf" | "egyptian" | "levantine" | "maghrebi" | "iraqi";
export type EvalCategory =
  | "dialect_understanding" | "technical_terminology" | "reasoning"
  | "instruction_following" | "translation" | "creative_writing"
  | "code_generation" | "culture_heritage";
export type EvalStatus = "pending" | "running" | "completed" | "failed";

export interface ScoreBreakdown {
  arabic_quality: number | null;
  accuracy: number | null;
  dialect_adherence: number | null;
  technical_precision: number | null;
  completeness: number | null;
  cultural_sensitivity: number | null;
  overall: number | null;
  reasoning?: string | null;
}

export interface ArabicMetrics {
  token_count: number;
  arabic_char_ratio: number;
  detected_dialect: string;
  dialect_match: boolean;
  sentence_count: number;
  avg_sentence_length_tokens: number;
  formal_marker_count: number;
  technical_term_count: number;
  unique_word_ratio: number;
}

export interface ModelResponse {
  model_id: string;
  model_name: string;
  provider: string;
  response_text: string | null;
  latency_ms: number | null;
  token_count: number | null;
  cost_usd: number | null;
  error: string | null;
  scores: ScoreBreakdown;
  arabic_metrics: ArabicMetrics | null;
}

export interface Evaluation {
  id: string;
  prompt: string;
  dialect: Dialect;
  category: EvalCategory;
  status: EvalStatus;
  winner_model_id: string | null;
  ranking: string[];
  model_responses: ModelResponse[];
  created_at: string;
  completed_at: string | null;
}

export interface EvaluationListItem {
  id: string;
  prompt: string;
  dialect: Dialect;
  category: EvalCategory;
  status: EvalStatus;
  winner_model_id: string | null;
  model_count: number;
  created_at: string;
}

export interface PaginatedEvaluations {
  items: EvaluationListItem[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}

export interface ModelInfo {
  id: string;
  name: string;
  provider: string;
  tier: string;
  description: string;
  context_window: number;
  max_output_tokens: number;
  cost_per_1k_input_usd: number;
  cost_per_1k_output_usd: number;
  supports_arabic: boolean;
  arabic_native: boolean;
  available: boolean;
}

export interface EvaluationRequest {
  prompt: string;
  dialect: Dialect;
  category: EvalCategory;
  models: string[];
  reference_answer?: string;
  max_tokens?: number;
}

// WebSocket event types
export type WsEventType =
  | "evaluation_start" | "stream_start" | "token"
  | "stream_end" | "stream_error" | "evaluation_complete" | "error";

export interface WsEvent {
  type: WsEventType;
  model_id?: string;
  token?: string;
  latency_ms?: number;
  token_count?: number;
  evaluation_id?: string;
  models?: string[];
  error?: string;
  arabic_metrics?: ArabicMetrics;
}
