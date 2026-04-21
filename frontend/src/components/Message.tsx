import type { Message } from "../types";

export const MessageComponent = ({ role, content }: Message) => (
    <div className={`flex ${role === "user" ? "justify-end" : "justify-start"} mb-4`}>
        <div className={`max-w-[80%] px-4 py-2 rounded-md text-sm ${
            role === "user" 
                ? "bg-gray-900 text-white" 
                : "bg-gray-100 text-gray-900 border border-gray-200"
        }`}>
            {content}
        </div>
    </div>
);
