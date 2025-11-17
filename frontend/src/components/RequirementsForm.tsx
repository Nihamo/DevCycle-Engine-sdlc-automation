import React, { useState } from "react";
import { CloudCog, CloudHail, Send, Trash2 } from "lucide-react";
import type { ProjectRequirements } from "../types";

interface Props {
  onSubmit: (requirements: ProjectRequirements) => void;
}

export default function RequirementsForm({ onSubmit }: Props) {
  const [requirements, setRequirements] = useState<ProjectRequirements>({
    title: "PayMate: Your Ultimate Payment Companion",
    description: "PayMate is a comprehensive payment application that allows users to perform seamless transactions using the Unified Payments Interface (UPI). Beyond basic payments, PayMate offers features such as quick loans, bill payments, and a user-friendly interface, making it a one-stop solution for all financial needs.",
    objectives: ["Implement multi-factor authentication, including biometrics (fingerprint and facial recognition) and MPIN, to secure user accounts.​", "Enable users to link multiple bank accounts and perform instant fund transfers using UPI.", "Provide users with access to instant micro-loans with minimal documentation.", "Allow users to pay utility bills such as electricity, water, gas, and broadband directly through the app."],
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(requirements);
  };

  const addObjective = () => {
    setRequirements((prev) => ({
      ...prev,
      objectives: [...prev.objectives, ""],
    }));
  };

  const deleteObjective = (index: number) => {
    setRequirements((prev) => {
      const updatedObjectives = prev.objectives.filter((_, i) => i != index);
      return { ...prev, objectives: updatedObjectives };
    })
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6 w-full max-w-2xl">
      <div>
        <label
          htmlFor="title"
          className="block text-sm font-medium text-gray-300"
        >
          Project Title
        </label>
        <input
          type="text"
          id="title"
          value={requirements.title}
          onChange={(e) =>
            setRequirements((prev) => ({ ...prev, title: e.target.value }))
          }
          placeholder="e.g. Task management app, E-commerce Platform, etc."
          className="mt-1 block w-full rounded-md bg-gray-800 border-gray-700 text-white shadow-sm focus:border-blue-500 focus:ring-blue-500 py-3 px-4 text-sm"
          required
        />
      </div>

      <div>
        <label
          htmlFor="description"
          className="block text-sm font-medium text-gray-300"
        >
          Project Description
        </label>
        <textarea
          id="description"
          value={requirements.description}
          onChange={(e) =>
            setRequirements((prev) => ({
              ...prev,
              description: e.target.value,
            }))
          }
          rows={2}
          placeholder="e.g. Description of the project in detail..."
          className="mt-1 block w-full rounded-md bg-gray-800 border-gray-700 text-white shadow-sm focus:border-blue-500 focus:ring-blue-500 py-3 px-4 text-sm"
          required
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-300 mb-2">
          Project Requirements
        </label>
        {requirements.objectives.map((objective, index) => (
          <div
            className="flex items-center justify-center"
          >
            <input
              key={index}
              type="text"
              value={objective}
              onChange={(e) => {
                const newObjectives = [...requirements.objectives];
                newObjectives[index] = e.target.value;
                setRequirements(prev => ({ ...prev, objectives: newObjectives }));
              }}
              className="mt-1 block w-full rounded-md bg-gray-800 border-gray-700 text-white shadow-sm focus:border-blue-500 focus:ring-blue-500 mb-2 py-3 px-4 text-sm"
              placeholder={`Requirement ${index + 1}`}
              required
            />
            <button
              type="button"
              onClick={() => deleteObjective(index)}
              className="ml-3 active:scale-[.9] p-3 rounded-3xl 
                        text-red-500 hover:text-red-700 hover:bg-red-300
                        shadow-lg hover:shadow-red-300
                        transition-colors duration-300 ease-in-out"
            >
              <Trash2
                className="w-4 h-4  hover:scale-[1.2]"
              />
            </button>
          </div>
        ))}
        {requirements.objectives.length < 4 && <button
          type="button"
          onClick={addObjective}
          className="text-sm text-blue-500 hover:text-blue-400 py-2"
        >
          + Add another requirement
        </button>}
      </div>

      {/* <button
        type="submit"
        className="w-full flex items-center justify-center px-6 py-3 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
      >
        <Send className="w-4 h-4 mr-2" />
        Submit Requirements
      </button> */}

      <button
        type="submit"
        className="w-full relative inline-flex items-center justify-center p-2 overflow-hidden font-medium text-blue-100
           bg-blue-700 border border-transparent rounded-md shadow-sm transition duration-300 
          ease-out group focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-700
          active:scale-[0.9]"
      >
        <span
          className="absolute inset-0 flex items-center justify-center w-full h-full bg-blue-800 transform -translate-x-full transition duration-300 ease-out group-hover:translate-x-0"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
        </span>
        <span
          className="absolute flex items-center justify-center w-full h-full transition-transform duration-300 transform group-hover:translate-x-full"
        >
          <Send className="w-4 h-4 mr-2" />
          Submit Requirements
        </span>

        <span
          className="relative invisible flex items-center"
        >
          <Send className="w-4 h-4 mr-2" />
          Submit Requirements
        </span>
      </button>

    </form>
  );
}
