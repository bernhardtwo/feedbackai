import type { Analysis } from "./types";

const BASE_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }

  return response.status === 204 ? (undefined as T) : ((await response.json()) as T);
}

export const listAnalyses = () => request<Analysis[]>("/analyses");

export const createAnalysis = (text: string) =>
  request<Analysis>("/analyses", {
    method: "POST",
    body: JSON.stringify({ text }),
  });

export const deleteAnalysis = (id: string) =>
  request<void>(`/analyses/${id}`, { method: "DELETE" });