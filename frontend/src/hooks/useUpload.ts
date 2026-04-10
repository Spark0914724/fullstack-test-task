"use client";

import { useState } from "react";
import { uploadFile } from "@/api/files";

export function useUpload(onSuccess: () => void) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function submit(title: string, file: File) {
    setIsSubmitting(true);
    setError(null);
    try {
      await uploadFile(title, file);
      onSuccess();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Произошла ошибка");
    } finally {
      setIsSubmitting(false);
    }
  }

  return { isSubmitting, error, submit };
}
