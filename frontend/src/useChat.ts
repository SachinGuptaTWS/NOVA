import { useState, useCallback } from "react";
import type { Message } from "./types";
import { chat, saveLead } from "./api";

export const useChat = () => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [sessionId] = useState(() => Math.random().toString(36).substring(7));
    const [loading, setLoading] = useState(false);
    const [leadActive, setLeadActive] = useState(false);
    const [handoff, setHandoff] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const sendMessage = useCallback(async (content: string) => {
        if (content.trim()) {
            setMessages(prev => [...prev, { id: Math.random().toString(), role: "user", content }]);
        }
        setError(null);
        setLoading(true);
        try {
            const res = await chat({ session_id: sessionId, message: content });
            setMessages(prev => [...prev, { id: Math.random().toString(), role: "bot", content: res.reply }]);
            setLeadActive(res.lead_flow_active);
            setHandoff(res.handoff);
        } catch (err: any) {
            setError(err.message || "An unexpected error occurred");
        } finally {
            setLoading(false);
        }
    }, [sessionId]);

    const submitLead = useCallback(async (name: string, email: string, phone: string) => {
        setError(null);
        setLoading(true);
        try {
            const res = await saveLead({ session_id: sessionId, name, email, phone });
            setLeadActive(false);
            setMessages(prev => [...prev, { id: Math.random().toString(), role: "bot", content: res.message }]);
        } catch (err: any) {
            setError(err.message || "Failed to save lead");
        } finally {
            setLoading(false);
        }
    }, [sessionId]);

    return { messages, loading, leadActive, handoff, error, sendMessage, submitLead };
};
