/**
 * API client — typed wrappers around all backend endpoints.
 */

import {
  Evaluation, EvaluationRequest, PaginatedEvaluations,
  ModelInfo, EvaluationListItem
} from "@/types";
import { API_BASE_URL } from "./constants";

class ApiError extends Error {
  constructor(public status: number, public code: string, message: string) {
    super(message);
    this.name = "ApiError";
  }
}

async function request<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json", ...options.headers },
    ...options,
  });

  if (!res.ok) {
    let code = "UNKNOWN_ERROR";
    let message = `HTTP ${res.status}`;
    try {
      const body = await res.json();
      code = body?.error?.code ?? code;
      message = body?.error?.message ?? message;
    } catch {
      // keep defaults
    }
    throw new ApiError(res.status, code, message);
  }

  return res.json() as Promise<T>;
}

// ── Evaluations ───────────────────────────────────────────

export const evaluationsApi = {
  run: (data: EvaluationRequest): Promise<Evaluation> =>
    request<Evaluation>("/api/v1/evaluations/run", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  list: (params: {
    page?: number;
    page_size?: number;
    dialect?: string;
    status?: string;
  } = {}): Promise<PaginatedEvaluations> => {
    const qs = new URLSearchParams();
    if (params.page)       qs.set("page",      String(params.page));
    if (params.page_size)  qs.set("page_size", String(params.page_size));
    if (params.dialect)    qs.set("dialect",   params.dialect);
    if (params.status)     qs.set("status",    params.status);
    return request<PaginatedEvaluations>(`/api/v1/evaluations?${qs}`);
  },

  get: (id: string): Promise<Evaluation> =>
    request<Evaluation>(`/api/v1/evaluations/${id}`),
};

// ── Models ────────────────────────────────────────────────

export const modelsApi = {
  list: (): Promise<ModelInfo[]> =>
    request<ModelInfo[]>("/api/v1/models"),

  get: (id: string): Promise<ModelInfo> =>
    request<ModelInfo>(`/api/v1/models/${id}`),
};

// ── Health ────────────────────────────────────────────────

export const healthApi = {
  check: () =>
    request<{ status: string; version: string }>("/api/v1/health"),
};

export { ApiError };
