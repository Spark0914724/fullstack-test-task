"use client";

import { useState, useCallback } from "react";
import { fetchFiles } from "@/api/files";
import { FileItem, PaginatedResponse } from "@/types";

export function useFiles(pageSize = 20) {
  const [data, setData] = useState<PaginatedResponse<FileItem> | null>(null);
  const [page, setPage] = useState(1);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async (p: number = page) => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await fetchFiles(p, pageSize);
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
