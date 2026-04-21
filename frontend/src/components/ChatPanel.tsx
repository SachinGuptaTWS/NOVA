import { useState, useRef, useEffect } from "react";
import { X, Send } from "lucide-react";
import { useChat } from "../useChat";
import { MessageComponent } from "./Message";
import { LeadForm } from "./LeadForm";

interface Props {
    onClose: () => void;
}

export const ChatPanel = ({ onClose }: Props) => {
    const { messages, loading, leadActive, error, sendMessage, submitLead } = useChat();
    const [input, setInput] = useState("");
    const scrollRef = useRef<HTMLDivElement>(null);

    const hasInit = useRef(false);

    useEffect(() => {
        // Auto-greeting on session start
        if (!hasInit.current && messages.length === 0 && !loading) {
            hasInit.current = true;
            sendMessage("");
        }
    }, [messages.length, loading, sendMessage]);

    useEffect(() => {
        scrollRef.current?.scrollTo(0, scrollRef.current.scrollHeight);
    }, [messages]);

    const handleSend = () => {
        if (!input.trim() || loading) return;
        sendMessage(input);
        setInput("");
    };

    return (
        <div className="flex flex-col h-full bg-white border border-gray-200 rounded-md shadow-lg overflow-hidden">
            <div className="flex items-center justify-between px-4 py-3 border-b border-gray-200">
                <h2 className="font-semibold text-gray-900">NexPath NOVA</h2>
                <button onClick={onClose} className="p-1 hover:bg-gray-100 rounded-md">
                    <X size={18} className="text-gray-600" />
                </button>
            </div>

            <div ref={scrollRef} className="flex-1 overflow-y-auto p-4 bg-gray-50">
                {messages.map((m) => (
                    <MessageComponent key={m.id} {...m} />
                ))}
                {loading && (
                    <div className="text-xs text-gray-500 italic mt-2">Sending...</div>
                )}
                {error && (
                    <div className="text-xs text-red-600 mt-2 p-2 bg-red-50 border border-red-200 rounded-md">
                        {error}
                    </div>
                )}
            </div>

            {leadActive ? (
                <LeadForm onSubmit={submitLead} isLoading={loading} />
            ) : (
                <div className="p-4 border-t border-gray-200 bg-white">
                    <div className="flex items-center gap-2">
                        <textarea
                            rows={1}
                            placeholder="Type a message..."
                            className="flex-1 p-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:border-gray-900 resize-none"
                            value={input}
                            onChange={e => setInput(e.target.value)}
                            onKeyDown={e => e.key === "Enter" && !e.shiftKey && (e.preventDefault(), handleSend())}
                        />
                        <button
                            onClick={handleSend}
                            disabled={!input.trim() || loading}
                            className="p-2 bg-gray-900 text-white rounded-md disabled:opacity-50"
                        >
                            <Send size={18} />
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};
