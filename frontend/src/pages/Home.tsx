import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import RequirementsForm from "../components/RequirementsForm";
import type { ProjectRequirements } from "../types";
import { BACKEND_URL } from "../../config";
import Loading from "../components/Loading";
import ToastError from "../components/ToastError";

export default function Home() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (requirements: ProjectRequirements) => {
    setLoading(true);
    // console.log(requirements)
    try {
      // console.log(BACKEND_URL)
      const payload = {
        title: requirements.title,
        description: requirements.description,
        requirements: requirements.objectives,
      }
      // console.log(payload)
      const response = await fetch(`${BACKEND_URL}/stories/generate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error("failed to call /stories/generate API");
      }

      const data = await response.json();

      console.log(data);
      setLoading(false);
      // In a real app, you'd save this to state management or backend
      navigate("/sdlc", { state: { requirements, data } });

    } catch (error) {
      console.error("error calling /stories/generate API:", error);
      setLoading(false);
      ToastError(error)
    }
  };

  return (
    <div className="min-h-screen bg-gray-950 text-white pt-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 ">
        <div className="text-center mb-6">
          <h1 className="text-4xl font-bold mb-4">Welcome to SDLC Copilot</h1>
          <p className="text-gray-400 max-w-2xl mx-auto">
            Your AI-powered companion for streamlining the Software Development
            Life Cycle.
            <p> Start by entering your project requirements below.</p>
          </p>
        </div>

        <div className="flex justify-center">
          <RequirementsForm onSubmit={handleSubmit} />
        </div>
      </div>
      {loading && <Loading />}
    </div>
  );
}
