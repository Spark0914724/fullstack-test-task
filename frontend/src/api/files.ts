import { API_URL } from "./client";
import { FileItem, PaginatedResponse } from "@/types";

export async function fetchFiles(page: number, pageSize: number): Promise<PaginatedResponse<FileItem>> {
  const res = await fetch(`${API_URL}/files?page=${page}&page_size=${pageSize}`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch files");
  return res.json();
}

export async function uploadFile(title: string, file: File): Promise<FileItem> {
  const formData = new FormData();
  formData.append("title", title);
  formData.append("file", file);
  const res = await fetch(`${API_URL}/files`, { method: "POST", body: formData });
  if (!res.ok) throw new Error("Failed to upload file");
  return res.json();
}

export function getDownloadUrl(fileId: string): string {
  return `${API_URL}/files/${fileId}/download`;
}
