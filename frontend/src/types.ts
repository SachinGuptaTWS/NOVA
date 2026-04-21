export interface Message {
    id: string;
    role: "user" | "bot";
    content: string;
}

export interface ChatRequest {
    session_id: string;
    message: string;
}

export interface ChatResponse {
    reply: string;
    intent: string;
    mode: string;
    lead_flow_active: boolean;
    handoff: boolean;
}

export interface LeadRequest {
    session_id: string;
    name: string;
    email: string;
    phone: string;
}

export interface LeadResponse {
    status: string;
    message: string;
    lead_id: string;
}
