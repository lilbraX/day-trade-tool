import { API_BASE } from "@/lib/constants/app";

async function request<T>(path: string, options: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    cache: "no-store",
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const detail = await res.text().catch(() => "");
    throw new Error(`${options.method ?? "GET"} ${path} failed (${res.status}): ${detail}`);
  }
  // 204 No Content など body なしのケースを考慮
  const text = await res.text();
  return text ? (JSON.parse(text) as T) : (undefined as T);
}

export async function apiGet<T>(path: string): Promise<T> {
  return request<T>(path, { method: "GET" });
}

export async function apiPost<T>(path: string, body: unknown): Promise<T> {
  return request<T>(path, { method: "POST", body: JSON.stringify(body) });
}

export async function apiPostForm<T>(path: string, form: FormData): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    cache: "no-store",
    body: form,
    // Content-Type は multipart のため意図的に未設定
  });
  if (!res.ok) {
    const detail = await res.text().catch(() => "");
    throw new Error(`POST ${path} failed (${res.status}): ${detail}`);
  }
  return res.json() as Promise<T>;
}

export async function apiPut<T>(path: string, body: unknown): Promise<T> {
  return request<T>(path, { method: "PUT", body: JSON.stringify(body) });
}

export async function apiDelete(path: string): Promise<void> {
  await request<void>(path, { method: "DELETE" });
}
