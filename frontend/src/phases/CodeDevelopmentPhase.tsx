import { useEffect, useState } from "react";
import axios from "axios";
import { BACKEND_URL } from "../../config"
import { FileExplorer } from "../components/FileExplorer";
import { FilePreview } from "../components/FilePreview";
import { useInitializeProject } from "../hooks/useInitializeProject";
import { useLocation } from "react-router-dom";
import { parseXml } from "../utils";
import { FileItem, Step, StepType } from "../types";
import { Code2 } from "lucide-react";
import Loading from "../components/Loading";
import ToastError from "../components/ToastError";
// import { Loader } from "lucide-react";

interface BuilderProps {
  selectedPhase: string;
  files: FileItem[];
  setFiles: (files: FileItem[]) => void;
}

export function CodeDevelopmentPhase({ selectedPhase, files, setFiles }: BuilderProps) {
  useInitializeProject();

  const location = useLocation();
  const { task } = location.state as { task: string };
  const data = location.state?.data;
  const [loading, setLoading] = useState(true);

  // const [loading, setLoading] = useState(false);
  // const [templateSet, setTemplateSet] = useState(false);
  const [steps, setSteps] = useState<Step[]>([]);
  // const [followUpPrompt, setFollowUpPrompt] = useState("");
  const [llmMessages, setLlmMessages] = useState<
    {
      role: "user" | "assistant";
      content: string;
    }[]
  >([]);

  // console.log(llmMessages);

  const [selectedFile, setSelectedFile] = useState<FileItem | null>(null);

  useEffect(() => {
    let originalFiles = [...files];
    let updateHappened = false;
    steps
      .filter(({ status }) => status === "pending")
      .forEach((step) => {
        updateHappened = true;
        if (step?.type === StepType.CreateFile && step.path) {
          // Remove leading slash if present
          const cleanPath = step.path.startsWith("/") ? step.path.slice(1) : step.path;
          let parsedPath = cleanPath.split("/").filter(Boolean); // ["src", "components", "App.tsx"] or ["package.json"]

          let currentFileStructure = [...originalFiles];
          const finalAnswerRef = currentFileStructure;

          let currentFolder = "";
          while (parsedPath.length) {
            const currentFolderName = parsedPath[0];
            currentFolder = currentFolder ? `${currentFolder}/${currentFolderName}` : currentFolderName;
            parsedPath = parsedPath.slice(1);

            if (!parsedPath.length) {
              // final file - check if it already exists
              const existingFile = currentFileStructure.find(
                (x) => x.path === currentFolder || x.name === currentFolderName
              );
              if (!existingFile) {
                currentFileStructure.push({
                  name: currentFolderName,
                  type: "file",
                  path: currentFolder,
                  content: step.code || "",
                });
                console.log(`Created file: ${currentFolder} (${currentFolderName})`);
              } else {
                existingFile.content = step.code || "";
                console.log(`Updated file: ${currentFolder} (${existingFile.name})`);
              }
            } else {
              // in a folder - find or create the folder
              let folder = currentFileStructure.find(
                (x) => (x.path === currentFolder || x.name === currentFolderName) && x.type === "folder"
              );
              if (!folder) {
                folder = {
                  name: currentFolderName,
                  type: "folder",
                  path: currentFolder,
                  children: [],
                };
                currentFileStructure.push(folder);
                console.log(`Created folder: ${currentFolder} (${currentFolderName})`);
              }

              currentFileStructure = folder.children!;
            }
          }
          originalFiles = finalAnswerRef;
        }
      });

    if (updateHappened) {
      console.log("Files after processing steps:", originalFiles);
      setFiles(originalFiles);
      setSteps((steps) =>
        steps.map((s: Step) => {
          return {
            ...s,
            status: "completed",
          };
        })
      );
    }
  }, [steps]);

  // async function init() {
  //   const response = await axios.post(`${BACKEND_URL}/api/template`, {
  //     prompt: task,
  //   });
  //   setTemplateSet(true);
  //   console.log(response.data);
  //   const { prompts, uiPrompts } = response.data;

  //   setSteps(
  //     parseXml(uiPrompts[0]).map((x) => ({
  //       ...x,
  //       status: "pending",
  //     }))
  //   );
  //   setLoading(true);

  //   const stepsResponse = await axios.post(`${BACKEND_URL}/api/chat`, {
  //     messages: [...task, prompts].map((content) => ({
  //       role: "user",
  //       content,
  //     })),
  //   });
  //   setLoading(false);

  //   setSteps((s) => [
  //     ...s,
  //     ...parseXml(stepsResponse.data.response).map((x) => ({
  //       ...x,
  //       status: "pending" as "pending",
  //     })),
  //   ]);

  //   setLlmMessages(
  //     [...prompts, prompt].map((content) => ({
  //       role: "user",
  //       content,
  //     }))
  //   );

  //   setLlmMessages((x) => [
  //     ...x,
  //     { role: "assistant", content: stepsResponse.data.response },
  //   ]);
  // }

  async function init() {
    setLoading(true)
    if (data) {
      try {
        let stepsToSet: Step[] = [];
        let messagesToSet: { role: "user" | "assistant"; content: string }[] = [
          { role: "user", content: task },
        ]
        if (selectedPhase === "frontend-coding") {
          var frontendResponse;
          if (location.state?.["frontend-coding"]?.code) {
            console.log("frontend-coding inside")
            frontendResponse = location.state?.["frontend-coding"]?.code;
          } else {
            const response = await axios.post(
              `${BACKEND_URL}/code/frontend/generate/${data.session_id}`,
              { prompt: task }
            );
            frontendResponse = response.data.code;
          }

          // console.log(frontendResponse.data.code)

          // Check if package.json is in the raw response
          const hasPackageJsonInResponse = frontendResponse.includes("package.json") || 
                                          frontendResponse.includes('filePath="package.json"') ||
                                          frontendResponse.includes("type=\"file\"") && frontendResponse.includes("package.json");
          console.log("package.json in raw response:", hasPackageJsonInResponse);
          if (hasPackageJsonInResponse) {
            console.log("Raw response snippet (package.json area):", 
              frontendResponse.substring(
                Math.max(0, frontendResponse.indexOf("package.json") - 200),
                frontendResponse.indexOf("package.json") + 500
              )
            );
          }
          
          const frontendSteps = parseXml(frontendResponse).map((x) => ({
            ...x,
            status: "pending" as "pending",
            code_type: "frontend" as "frontend",
          }));
          
          console.log("Parsed frontend steps:", frontendSteps);
          console.log("Steps with package.json:", frontendSteps.filter(s => s.path?.includes("package.json")));
          console.log("All step paths:", frontendSteps.map(s => s.path).filter(Boolean));
          
          stepsToSet = frontendSteps;
          messagesToSet.push({
            role: "assistant",
            content: frontendResponse,
          });
          // console.log(frontendResponse.data.code)
        }
        if (selectedPhase === "backend-coding") {
          var backendResponse
          if (location.state?.["backend-coding"]?.code) {
            console.log("backend-coding inside")
            backendResponse = location.state?.["backend-coding"]?.code;
          } else {
            const response = await axios.post(
              `${BACKEND_URL}/code/backend/generate/${data.session_id}`,
              { prompt: task }
            );
            backendResponse = response.data.code
          }
          // console.log(backendResponse.data.code);
          const backendSteps = parseXml(backendResponse).map((x) => ({
            ...x,
            status: "pending" as "pending",
            code_type: "backend" as "backend",
          }));

          // console.log(backendSteps)

          stepsToSet = backendSteps;
          messagesToSet.push({
            role: "assistant",
            content: backendResponse,
          });
          // console.log(backendResponse.data.code)
        }
        // console.log(stepsToSet)
        setSteps(stepsToSet);
        setLlmMessages(messagesToSet);
        setLoading(false)

      } catch (error: any) {
        console.error("Error during code generation", error);
        setLoading(false)
        ToastError(error);
      }
    }
  }

  useEffect(() => {
    init();
  }, [selectedPhase, location.state]);


  if (loading) {
    return <Loading />;
  }

  return (
    <div className="flex-1 overflow-hidden">
      <div className="h-full grid grid-cols-3 gap-6 p-6">
        <div className="col-span-1">
          <FileExplorer files={files} onFileSelect={setSelectedFile} />
        </div>
        <div className="col-span-2 bg-gray-900 rounded-lg shadow-lg h-[calc(100vh-8rem)]">
          <div className="p-4 border-b border-gray-700">
            <div className="flex items-center gap-2">
              <Code2 className="w-4 h-4 text-gray-400" />
              <span className="text-gray-300 font-medium">Code</span>
            </div>
          </div>
          <div className="h-[calc(100%-4rem)]">
            <FilePreview selectedFile={selectedFile} />
          </div>
        </div>
      </div>
    </div>
  );
}
