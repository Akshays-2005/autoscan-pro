import axios from "axios";

// Configure your Flask backend URL here (or via VITE_API_URL env var)
export const API_URL =
  import.meta.env.VITE_API_URL || "http://localhost:5000";

export interface ProcessResponse {
  imageBlob: Blob;
}

export async function processDocument(file: File): Promise<Blob> {
  const formData = new FormData();
  formData.append("image", file);

  const response = await axios.post(`${API_URL}/process-document`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
    responseType: "blob",
  });

  // If server returned JSON error with blob responseType, parse it
  if (response.data.type === "application/json") {
    const text = await response.data.text();
    const json = JSON.parse(text);
    throw new Error(json.error || "Processing failed");
  }

  return response.data as Blob;
}
