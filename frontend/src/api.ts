import type { ChatRequest, ChatResponse, LeadRequest, LeadResponse } from "./types";

const BASE_URL = "http://localhost:8000";

async function handleResponse<T>(response: Response): Promise<T> {
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    const errorMsg = data.detail || data.message || `HTTP ${response.status}: ${response.statusText}`;
    throw new Error(`NexPath API Error: ${errorMsg}`);
  }
  return data as T;
}

export const chat = async (data: ChatRequest): Promise<ChatResponse> => {
    const res = await fetch(`${BASE_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });
    return handleResponse<ChatResponse>(res);
};

export const saveLead = async (data: LeadRequest): Promise<LeadResponse> => {
    const res = await fetch(`${BASE_URL}/lead`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });
    return handleResponse<LeadResponse>(res);
};
