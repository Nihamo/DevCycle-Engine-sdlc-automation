// src/components/ToastError.tsx
import { toast } from "sonner";
import { CheckCircle, XCircleIcon } from "lucide-react";

export default function ToastSuccess(message: string) {
    toast.custom((t) => (
        <div
            className={`flex items-center gap-4 bg-black text-green-600 border border-blue-500 px-4 py-3 rounded-lg shadow-lg transition-all duration-300 w-[320px]`}
        >
            <CheckCircle className="w-5 h-5 text-green-500" />
            <span className="flex-1 text-xs font-bold">{message}</span>

            <button
                onClick={() => toast.dismiss(t)}
                className="text-green-500 hover:text-green-300 text-xl"
            >
                <XCircleIcon className="w-4 h-4 text-green-500" />
            </button>
        </div>
    ));
}
