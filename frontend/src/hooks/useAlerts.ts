"use client";

import { useState, useCallback } from "react";
import { fetchAlerts } from "@/api/alerts";
import { AlertItem, PaginatedResponse } from "@/types";

export function useAlerts(pageSize = 20) {
  const [data, setData] = useState<PaginatedResponse<AlertItem> | null>(null);
  const [page, setPage] = useState(1);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async (p: number = page) => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await fetchAlerts(p, pageSize);
      setData(result);
      setPage(p);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Произошла ошибка");
    } finally {
      setIsLoading(false);
    }
  }, [page, pageSize]);

  return { data, page, isLoading, error, load, setPage: (p: number) => load(p) };
}
