// src/components/ToastError.tsx
import { toast } from "sonner";
import { AlertCircleIcon, XCircleIcon } from "lucide-react";

export default function ToastError(message: any) {
    const errorMessage = typeof message === 'string' ? message : message?.message || String(message);

    toast.custom((t) => (
        <div
            className={`flex items-center gap-4 bg-black text-red-500 border border-blue-500 px-4 py-3 rounded-lg shadow-lg transition-all duration-300 w-[320px]`}
        >
            <AlertCircleIcon className="w-5 h-5 text-red-500" />
            <span className="flex-1 text-xs font-bold">{errorMessage}</span>

            <button
                onClick={() => toast.dismiss(t)}
                className="text-red-500 hover:text-red-300 text-xl"
            >
                <XCircleIcon className="w-4 h-4 text-red-500" />
            </button>
        </div>
    ));
}
