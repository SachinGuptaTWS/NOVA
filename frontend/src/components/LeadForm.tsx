import { useState } from "react";

interface Props {
    onSubmit: (name: string, email: string, phone: string) => void;
    isLoading?: boolean;
}

export const LeadForm = ({ onSubmit, isLoading }: Props) => {
    const [step, setStep] = useState(1);
    const [data, setData] = useState({ name: "", email: "", phone: "" });

    const isValid = () => {
        if (step === 1) return data.name.trim().length > 2;
        if (step === 2) return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email);
        if (step === 3) return data.phone.trim().length >= 10;
        return false;
    };

    const next = () => {
        if (!isValid()) return;
        if (step < 3) setStep(s => s + 1);
        else onSubmit(data.name, data.email, data.phone);
    };

    return (
        <div className="p-4 border-t border-gray-200 bg-gray-50">
            <div className="flex items-center justify-between mb-3">
                <h3 className="text-xs font-semibold text-gray-500 uppercase">
                    Step {step} of 3
                </h3>
            </div>
            {step === 1 && (
                <input
                    type="text"
                    placeholder="Full Name"
                    className="w-full p-2 border border-gray-300 rounded-md text-sm mb-3 focus:outline-none focus:border-gray-900"
                    value={data.name}
                    onChange={e => setData({ ...data, name: e.target.value })}
                />
            )}
            {step === 2 && (
                <input
                    type="email"
                    placeholder="Email Address"
                    className="w-full p-2 border border-gray-300 rounded-md text-sm mb-3 focus:outline-none focus:border-gray-900"
                    value={data.email}
                    onChange={e => setData({ ...data, email: e.target.value })}
                />
            )}
            {step === 3 && (
                <input
                    type="tel"
                    placeholder="Phone Number (10+ digits)"
                    className="w-full p-2 border border-gray-300 rounded-md text-sm mb-3 focus:outline-none focus:border-gray-900"
                    value={data.phone}
                    onChange={e => setData({ ...data, phone: e.target.value })}
                />
            )}
            <button
                onClick={next}
                disabled={!isValid() || isLoading}
                className="w-full bg-gray-900 text-white py-2 rounded-md text-sm font-semibold disabled:opacity-50"
            >
                {isLoading ? "Submitting..." : step === 3 ? "Submit" : "Next"}
            </button>
        </div>
    );
};
