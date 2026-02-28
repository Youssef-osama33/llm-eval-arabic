/**useModels — fetch and cache the model registry. */

import { useState, useEffect } from "react";
import { modelsApi } from "@/lib/api";
import { ModelInfo } from "@/types";

export function useModels() {
  const [models, setModels] = useState<ModelInfo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    modelsApi
      .list()
      .then(setModels)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  return { models, loading, error };
}
