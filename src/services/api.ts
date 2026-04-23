// Configure your Flask backend URL via VITE_API_URL or change the default below
export const API_URL =
  (import.meta.env.VITE_API_URL as string) || "http://localhost:5000";

export async function processDocument(file: File): Promise<Blob> {
  const formData = new FormData();
  formData.append("image", file);

  const res = await fetch(`${API_URL}/process-document`, {
    method: "POST",
    body: formData,
  });

  const contentType = res.headers.get("content-type") || "";
  if (!res.ok || contentType.includes("application/json")) {
    let message = `Request failed (${res.status})`;
    try {
      const json = await res.json();
      message = json.error || message;
    } catch {}
    throw new Error(message);
  }

  return await res.blob();
}
