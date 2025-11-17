import React from "react";
import {
  ChevronLeft,
  FileText,
  Palette,
  Code,
  TestTube,
  Upload,
  Settings,
  Shield,
  Book,
  Layers,
  CheckCircle,
  Server,
  Bug,
  LockIcon,
  UnlockIcon,
} from "lucide-react";
import type { SDLCPhase } from "../types";
import { toast } from "sonner";
import ToastError from "./ToastError";

interface Props {
  selectedPhase: SDLCPhase;
  onPhaseSelect: (phase: SDLCPhase) => void;
  isCollapsed: boolean;
  onToggleCollapse: () => void;
  completedPhases: string[];
}

export const phases: { id: SDLCPhase; icon: React.ElementType; label: string }[] = [
  { id: "requirements", icon: FileText, label: "Requirements" },
  { id: "user-stories", icon: Book, label: "User Stories" },
  { id: "functional-design", icon: Palette, label: "Functional Design" },
  { id: "technical-design", icon: Layers, label: "Technical Design" },
  { id: "frontend-coding", icon: Code, label: "Frontend Coding" },
  { id: "backend-coding", icon: Server, label: "Backend Coding" },
  { id: "security", icon: Shield, label: "Security Reviews" },
  { id: "testing", icon: TestTube, label: "Test Cases" },
  { id: "qa-testing", icon: Bug, label: "QA Testing" },
  { id: "deployment", icon: Upload, label: "Deployment" },
  { id: "maintenance", icon: Settings, label: "Maintenance" },
];


const isPhaseUnlocked = (
  phaseId: SDLCPhase,
  completedPhases: string[]
): boolean => {
  const phaseIndex = phases.findIndex((p) => p.id === phaseId);
  if (phaseIndex === 0) return true;
  const previousPhaseId = phases[phaseIndex - 1].id;
  return completedPhases.includes(previousPhaseId)
}

export default function SDLCPhaseSelector({
  selectedPhase,
  onPhaseSelect,
  isCollapsed,
  onToggleCollapse,
  completedPhases,
}: Props) {
  return (
    <div
      className={`h-full bg-gray-900 border-r border-gray-800 transition-all duration-300 ${isCollapsed ? "w-16" : "w-64"
        }`}
    >
      <button
        onClick={onToggleCollapse}
        className="h-20 w-full p-4 flex items-center justify-between hover:bg-gray-800"
      >
        <span
          className={`text-gray-400 transition-opacity duration-300 text-2xl font-bold`}
        >
          {isCollapsed ? "" : "SDLC Phases"}
        </span>
        <ChevronLeft
          className={`w-6 h-6 text-gray-400 transition-transform duration-300 ${isCollapsed ? "rotate-180" : ""
            }`}
        />
      </button>

      <nav className="">
        {phases.map(({ id, icon: Icon, label }) => {
          const isCompleted = completedPhases.includes(id);
          const unlocked = isPhaseUnlocked(id, completedPhases);
          const handleClick = () => {
            if (!unlocked) {
              ToastError("Please approve the previous phase!!");
              return;
            }
            onPhaseSelect(id);
          };
          return (
            <button
              key={id}
              onClick={() => handleClick()}
              className={`w-full p-4 flex items-center justify-between transition-colors duration-300 
                ${selectedPhase === id
                  ? "bg-blue-600 text-white"
                  : "text-gray-400 hover:bg-gray-800"
                } ${!unlocked ? "filter blur-xs opacity-50" : ""} `}
            >
              <div className="flex items-center">
                <Icon className="w-6 h-6" />
                {!isCollapsed && <span className="ml-3">{label}</span>}
              </div>
              {isCompleted && (
                <CheckCircle className="w-5 h-5 text-green-500" />
              )}
              {!isCompleted && !unlocked && (
                <LockIcon className="w-5 h-5" />
              )}
              {!isCompleted && unlocked && (
                <UnlockIcon className="w-5 h-5" />
              )}
            </button>
          );
        })}
      </nav>
    </div>
  );
}
