/**
 * useEvaluation — manages evaluation state and API calls.
 * Polls for completion after submitting (or uses WebSocket for streaming).
 */

import { useState, useCallback, useRef } from "react";
import { evaluationsApi } from "@/lib/api";
import { Evaluation, EvaluationRequest, EvalStatus } from "@/types";
import { WS_BASE_URL } from "@/lib/constants";

export type StreamingTokens = Record<string, string>;

interface UseEvaluationReturn {
  evaluation: Evaluation | null;
  streamingTokens: StreamingTokens;
  status: EvalStatus | "idle";
  error: string | null;
  isLoading: boolean;
  submit: (req: EvaluationRequest) => Promise<void>;
  reset: () => void;
}

const POLL_INTERVAL_MS = 2000;
const MAX_POLLS = 60; // 2 minutes max

export function useEvaluation(): UseEvaluationReturn {
  const [evaluation, setEvaluation] = useState<Evaluation | null>(null);
  const [streamingTokens, setStreamingTokens] = useState<StreamingTokens>({});
  const [status, setStatus] = useState<EvalStatus | "idle">("idle");
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);
  const pollRef = useRef<NodeJS.Timeout | null>(null);

  const reset = useCallback(() => {
    wsRef.current?.close();
    if (pollRef.current) clearInterval(pollRef.current);
    setEvaluation(null);
    setStreamingTokens({});
    setStatus("idle");
    setError(null);
    setIsLoading(false);
  }, []);

  // ── REST submit + polling ──────────────────────────────
  const submitRest = useCallback(async (req: EvaluationRequest) => {
    const created = await evaluationsApi.run(req);
    setEvaluation(created);
    setStatus("running");

    let polls = 0;
    pollRef.current = setInterval(async () => {
      polls++;
      try {
        const updated = await evaluationsApi.get(created.id);
        setEvaluation(updated);
        setStatus(updated.status);

        if (updated.status === "completed" || updated.status === "failed") {
          clearInterval(pollRef.current!);
          setIsLoading(false);
        }
      } catch (err) {
        if (polls >= MAX_POLLS) {
          clearInterval(pollRef.current!);
          setError("Polling timed out. Please refresh the page.");
          setIsLoading(false);
        }
      }
    }, POLL_INTERVAL_MS);
  }, []);

  // ── WebSocket streaming submit ─────────────────────────
  const submitWs = useCallback(async (req: EvaluationRequest) => {
    return new Promise<void>((resolve, reject) => {
      const ws = new WebSocket(`${WS_BASE_URL}/ws/evaluate`);
      wsRef.current = ws;

      ws.onopen = () => {
        ws.send(JSON.stringify({
          prompt: req.prompt,
          dialect: req.dialect,
          models: req.models,
          max_tokens: req.max_tokens ?? 1024,
        }));
      };

      ws.onmessage = (event) => {
        try {
          const msg = JSON.parse(event.data);

          switch (msg.type) {
            case "evaluation_start":
              setStatus("running");
              // Create a placeholder evaluation
              setEvaluation({
                id: msg.evaluation_id,
                prompt: req.prompt,
                dialect: req.dialect,
                category: req.category,
                status: "running",
                winner_model_id: null,
                ranking: [],
                model_responses: [],
                created_at: new Date().toISOString(),
                completed_at: null,
              });
              break;

            case "token":
              setStreamingTokens((prev) => ({
                ...prev,
                [msg.model_id]: (prev[msg.model_id] ?? "") + msg.token,
              }));
              break;

            case "evaluation_complete":
              setStatus("completed");
              setIsLoading(false);
              ws.close();
              resolve();
              break;

            case "error":
              setError(msg.message ?? "Unknown WebSocket error");
              setStatus("failed");
              setIsLoading(false);
              ws.close();
              reject(new Error(msg.message));
              break;
          }
        } catch {
          // ignore parse errors
        }
      };

      ws.onerror = () => {
        // Fall back to REST on WebSocket failure
        ws.close();
        submitRest(req).then(resolve).catch(reject);
      };

      ws.onclose = () => {
        wsRef.current = null;
      };
    });
  }, [submitRest]);

  // ── Public submit ──────────────────────────────────────
  const submit = useCallback(async (req: EvaluationRequest) => {
    setIsLoading(true);
    setError(null);
    setStatus("pending");
    setStreamingTokens({});

    try {
      const wsSupported = typeof WebSocket !== "undefined";
      if (wsSupported) {
        await submitWs(req);
      } else {
        await submitRest(req);
      }
    } catch (err) {
      const message = err instanceof Error ? err.message : "Unknown error";
      setError(message);
      setStatus("failed");
      setIsLoading(false);
    }
  }, [submitWs, submitRest]);

  return { evaluation, streamingTokens, status, error, isLoading, submit, reset };
}
