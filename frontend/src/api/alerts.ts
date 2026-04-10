import { API_URL } from "./client";
import { AlertItem, PaginatedResponse } from "@/types";

export async function fetchAlerts(page: number, pageSize: number): Promise<PaginatedResponse<AlertItem>> {
  const res = await fetch(`${API_URL}/alerts?page=${page}&page_size=${pageSize}`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch alerts");
  return res.json();
}
