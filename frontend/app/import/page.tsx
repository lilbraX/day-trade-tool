"use client";

import { useState } from "react";
import { Nav } from "@/components/nav";
import { API_BASE } from "@/lib/constants/app";

export default function ImportPage() {
  const [result, setResult] = useState<null | { success_count: number; error_count: number; errors: { row: number; reason: string }[] }>(null);

  async function onSubmit(formData: FormData) {
    const file = formData.get("file") as File;
    if (!file) return;
    const payload = new FormData();
    payload.set("file", file);
    const res = await fetch(`${API_BASE}/import/csv`, { method: "POST", body: payload });
    const json = await res.json();
    setResult(json);
  }

  return (
    <>
      <Nav />
      <div className="card">
        <h2>CSV Import</h2>
        <form action={onSubmit}>
          <input type="file" name="file" accept=".csv" />
          <button type="submit">Upload</button>
        </form>
        {result && (
          <div>
            <p>success: {result.success_count} / error: {result.error_count}</p>
            {result.errors.length > 0 && <ul>{result.errors.map((e, idx) => <li key={idx}>row {e.row}: {e.reason}</li>)}</ul>}
          </div>
        )}
      </div>
    </>
  );
}
