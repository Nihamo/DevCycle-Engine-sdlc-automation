import React, { useState } from "react";
import { useLocation } from "react-router-dom";
import SDLCPhaseSelector from "../components/SDLCPhaseSelector";
import ChatInterface from "../components/ChatInterface";
import type { SDLCPhase, ProjectRequirements } from "../types";
import RequirementsPhase from "../phases/RequirementsPhase";
import UserStoriesPhase from "../phases/UserStoriesPhase";
import FunctionalDesignPhase from "../phases/FunctionalDesignPhase";
import { CodeDevelopmentPhase } from "../phases/CodeDevelopmentPhase";
import { FileItem } from "../types";
import TechnicalDesignPhase from "../phases/TechnicalDesignPhase";
import Security from "../phases/Security";
import TestCases from "../phases/TestCases";
import QATesting from "../phases/QATesting";

export default function SDLC() {
  const location = useLocation();
  const requirements = location.state?.requirements as ProjectRequirements;
  const completedPhases = location.state?.completedPhases || [];
  const [selectedPhase, setSelectedPhase] = useState<SDLCPhase>("requirements");
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const [files, setFiles] = useState<FileItem[]>([]);
  const [backendFiles, setBackendFiles] = useState<FileItem[]>([]);

  // If requirements phase is completed, automatically navigate to user stories
  // React.useEffect(() => {
  //   // console.log(requirements)
  //   if (
  //     completedPhases.includes("requirements") &&
  //     selectedPhase === "requirements"
  //   ) {
  //     setSelectedPhase("user-stories");
  //   }
  // }, [completedPhases, selectedPhase]);

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <div className="h-screen flex">
        <SDLCPhaseSelector
          selectedPhase={selectedPhase}
          onPhaseSelect={setSelectedPhase}
          isCollapsed={isSidebarCollapsed}
          onToggleCollapse={() => setIsSidebarCollapsed(!isSidebarCollapsed)}
          completedPhases={completedPhases}
        />

        <div className="flex-1 flex flex-col">
          <div className="h-20 px-5 bg-gray-900 border-b border-gray-800 flex flex-col justify-center">
            <h2 className="text-xl">{requirements?.title}</h2>
          </div>

          {selectedPhase === "requirements" && <RequirementsPhase />}
          {selectedPhase === "user-stories" && <UserStoriesPhase />}
          {selectedPhase === "functional-design" && <FunctionalDesignPhase />}
          {selectedPhase === "technical-design" && <TechnicalDesignPhase />}
          {selectedPhase === "frontend-coding" && <CodeDevelopmentPhase selectedPhase={selectedPhase} files={files} setFiles={setFiles} />}
          {selectedPhase === "backend-coding" && <CodeDevelopmentPhase selectedPhase={selectedPhase} files={backendFiles} setFiles={setBackendFiles} />}
          {selectedPhase === "security" && <Security />}
          {selectedPhase === "testing" && <TestCases />}
          {selectedPhase === "qa-testing" && <QATesting />}
          {/* {selectedPhase === "technical-design" && <TechnicalDesignPhase />} */}

          {/* <div className="flex-1 p-6 overflow-y-auto">
            <h3 className="text-xl font-semibold mb-4 capitalize">
              {selectedPhase} Phase
            </h3>
            <p className="text-gray-400">
              This section will display detailed information about the{" "}
              {selectedPhase} phase.
            </p>
          </div> */}

          <ChatInterface selectedPhase={selectedPhase} setSelectedPhase={setSelectedPhase} />
        </div>
      </div>
    </div>
  );
}
