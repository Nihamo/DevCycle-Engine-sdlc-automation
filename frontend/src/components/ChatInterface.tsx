import React, { useState } from "react";
import { Send } from "lucide-react";
import type { ChatMessage, ProjectRequirements, SDLCPhase } from "../types";
import { json, useLocation, useNavigate } from "react-router-dom";
import { BACKEND_URL } from "../../config";
import Loading from "./Loading";
import ToastError from "./ToastError";
import { toast } from "sonner";
import ToastSuccess from "./ToastSuccess";
import { phases } from "./SDLCPhaseSelector";

interface Props {
  selectedPhase: SDLCPhase,
  setSelectedPhase: (phase: SDLCPhase) => void;
}

export default function ChatInterface({ selectedPhase, setSelectedPhase }: Props) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const navigate = useNavigate();
  const location = useLocation();
  const requirements = location.state?.requirements as ProjectRequirements;
  const data = location.state?.data
  const [loading, setLoading] = useState(false);

  const getNextPhase = (current: SDLCPhase): SDLCPhase => {
    const phaseOrder: SDLCPhase[] = [
      "requirements",
      "user-stories",
      "functional-design",
      "technical-design",
      "frontend-coding",
      "backend-coding",
      "security",
      "testing",
      "qa-testing",
      "deployment",
      "maintenance",
    ];
    const currentIndex = phaseOrder.indexOf(current);

    if (currentIndex === -1 || currentIndex === phaseOrder.length - 1) {
      return current;
    }
    return phaseOrder[currentIndex + 1];
  }

  const phaseApiMapping: Partial<Record<SDLCPhase, string>> = {
    "user-stories": "stories/review",
    "functional-design": "documents/functional/review",
    "technical-design": "documents/technical/review",
    "frontend-coding": "code/frontend/review",
    "backend-coding": "code/backend/review",
    "security": "security/review/review",
    "testing": "test/cases/review"
  }

  const getPhaseLabel = (phaseId: SDLCPhase) => {
    const phase = phases.find(p => p.id === phaseId);
    return phase ? phase.label : "Unknown Phase";
  }

  const handleApproveAndContinue = async () => {
    setLoading(true);
    const relativeUrl = phaseApiMapping[selectedPhase];
    const prevState = location.state || {};

    if (relativeUrl && data?.session_id) {
      const fullUrl = `${BACKEND_URL}/${relativeUrl}/${data.session_id}`;
      try {
        const response = await fetch(fullUrl, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ feedback: "approved" })
        });

        const jsonResponse = await response.json();
        console.log(jsonResponse)
        ToastSuccess(`Approved ${getPhaseLabel(selectedPhase)}!!`)
        navigate("/sdlc", {
          state: {
            ...prevState,
            completedPhases: [
              ...(prevState?.completedPhases || []),
              selectedPhase
            ],
            [selectedPhase]: jsonResponse,
          }
        })
        const nextPhase = getNextPhase(selectedPhase);
        setLoading(false);
        setSelectedPhase(nextPhase);
        return
      } catch (error) {
        console.log(`Error while calling ${fullUrl}: `, error)
        setLoading(false);
        ToastError(`Error while calling ${fullUrl}: ${error}`);
      }
    }
    if (!data?.session_id && selectedPhase !== "requirements") {
      console.error("no data.session_id");
      setLoading(false);
      ToastError("no data session_id");
    }
    if (selectedPhase === "requirements") {
      ToastSuccess(`Approved ${getPhaseLabel(selectedPhase)}!!`);
    }

    setLoading(false);
    // In a real app, you'd save the completion status to state management or backend
    navigate("/sdlc", {
      state: {
        ...prevState,
        completedPhases: [...(prevState?.completedPhases || []), selectedPhase],
      }
    });
    // console.log(location.state)
    const nextPhase = getNextPhase(selectedPhase);
    setSelectedPhase(nextPhase);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    setLoading(true);
    e.preventDefault();
    if (!input.trim()) {
      setLoading(false);
      return;
    };

    const relativeUrl = phaseApiMapping[selectedPhase];
    const prevState = location.state || {};

    if (relativeUrl && data?.session_id) {
      const fullUrl = `${BACKEND_URL}/${relativeUrl}/${data.session_id}`;
      try {
        const response = await fetch(fullUrl, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ feedback: input }),
        });
        console.log(input)

        const jsonResponse = await response.json();
        console.log(jsonResponse);
        navigate("/sdlc", {
          state: {
            ...prevState,
            [selectedPhase]: jsonResponse
          }
        })
      } catch (error) {
        console.log(`error while calling ${fullUrl}: `, error)
        ToastError(`error while calling ${fullUrl}: ${error}`);
      } finally {
        setLoading(false);
      }
    }

    const newMessage: ChatMessage = {
      id: Date.now().toString(),
      content: input,
      sender: "user",
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, newMessage]);
    setInput("");
    setLoading(false);

    // Simulate AI response
    setTimeout(() => {
      const aiResponse: ChatMessage = {
        id: (Date.now() + 1).toString(),
        content: "I understand your question. Let me help you with that.",
        sender: "ai",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, aiResponse]);
    }, 1000);
  };

  return (
    <div className="flex flex-col h-20 bg-gray-900 border-t border-gray-800">
      {/* <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-xs md:max-w-md p-3 rounded-lg ${
                message.sender === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-800 text-gray-200'
              }`}
            >
              {message.content}
            </div>
          </div>
        ))}
      </div> */}

      <form onSubmit={handleSubmit} className="p-4 border-t border-gray-800">
        <div className={`flex space-x-2 ${selectedPhase === 'requirements' && 'items-center justify-center'}`}>
          <button
            onClick={handleApproveAndContinue}
            className="px-6 py-3 bg-blue-600 text-white rounded-md 
              hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500
                focus:ring-offset-2 focus:ring-offset-gray-800 transition-colors duration-200
                active:scale-[0.8]"
          >
            Approve & Continue
          </button>
          {selectedPhase !== "requirements" &&
            <>
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Provide feedback..."
                className="flex-1 bg-gray-800 border-gray-700 rounded-md px-4 py-2 text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <button
                type="submit"
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
              >
                <Send className="w-5 h-5" />
              </button>
            </>}
        </div>
      </form>
      {loading && <Loading />}
    </div>
  );
}
