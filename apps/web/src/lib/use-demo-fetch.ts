"use client";

import { useEffect, useState } from "react";

import { getApiBaseUrl } from "./api-base-url";

type DemoFetchState<T> = {
  data: T | null;
  error: string | null;
  loading: boolean;
};

export function useDemoFetch<T>(path: string): DemoFetchState<T> {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      setLoading(true);
      try {
        const response = await fetch(`${getApiBaseUrl()}${path}`);
        if (!response.ok) {
          throw new Error(`API returned ${response.status}`);
        }
        const payload = (await response.json()) as T;
        if (!cancelled) {
          setData(payload);
          setError(null);
        }
      } catch (caught) {
        if (!cancelled) {
          setError(caught instanceof Error ? caught.message : "Unable to load demo data");
          setData(null);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    void load();

    return () => {
      cancelled = true;
    };
  }, [path]);

  return { data, error, loading };
}
