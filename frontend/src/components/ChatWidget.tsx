import { useState } from "react";
import { MessageCircle } from "lucide-react";
import { ChatPanel } from "./ChatPanel";

export const ChatWidget = () => {
    const [isOpen, setIsOpen] = useState(false);

    return (
        <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end">
            {isOpen && (
                <div className="mb-4 w-[384px] h-[600px] max-h-[80vh] max-w-[90vw]">
                    <ChatPanel onClose={() => setIsOpen(false)} />
                </div>
            )}
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="w-12 h-12 bg-gray-900 text-white rounded-md border border-gray-800 shadow-sm flex items-center justify-center hover:bg-gray-800 transition-colors"
                aria-label="Toggle chat"
            >
                <MessageCircle size={24} />
            </button>
        </div>
    );
};
