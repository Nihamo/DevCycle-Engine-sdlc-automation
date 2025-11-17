import { useEffect, useState } from "react";
import axios from "axios";
import { BACKEND_URL } from "../../config"
import { FileExplorer } from "../components/FileExplorer";
import { FilePreview } from "../components/FilePreview";
import { useInitializeProject } from "../hooks/useInitializeProject";
import { useLocation } from "react-router-dom";
import { parseXml } from "../utils";
import { FileItem, Step, StepType } from "../types";
import { TabView } from "../components/TabView";
import { useWebContainer } from "../hooks/useWebContainer";
import { PreviewFrame } from "../components/PreviewFrame";
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
  const webContainer = useWebContainer();
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
  const [activeTab, setActiveTab] = useState<"code" | "preview">("code");

  useEffect(() => {
    const createMountStructure = (files: FileItem[]): Record<string, any> => {
      const mountStructure: Record<string, any> = {};

      const processFile = (file: FileItem, isRootFolder: boolean) => {
        if (file.type === "folder") {
          // For folders, create a directory entry
          mountStructure[file.name] = {
            directory: file.children
              ? Object.fromEntries(
                file.children.map((child) => [
                  child.name,
                  processFile(child, false),
                ])
              )
              : {},
          };
        } else if (file.type === "file") {
          if (isRootFolder) {
            mountStructure[file.name] = {
              file: {
                contents: file.content || "",
              },
            };
          } else {
            // For files, create a file entry with contents
            return {
              file: {
                contents: file.content || "",
              },
            };
          }
        }

        return mountStructure[file.name];
      };

      // Process each top-level file/folder
      files.forEach((file) => processFile(file, true));
      return mountStructure;
    };

    const mountStructure = createMountStructure(files);
    // Mount the structure if WebContainer is available
    // console.log(mountStructure);
    webContainer?.mount(mountStructure);
    // console.log("Web container is");
    // console.log(webContainer);
  }, [files, webContainer]);

  useEffect(() => {
    let originalFiles = [...files];
    let updateHappened = false;
    steps
      .filter(({ status }) => status === "pending")
      .map((step) => {
        updateHappened = true;
        if (step?.type === StepType.CreateFile) {
          let parsedPath = step.path?.split("/") ?? []; // ["src", "components", "App.tsx"]

          let currentFileStructure = [...originalFiles]; // {}
          const finalAnswerRef = currentFileStructure;

          let currentFolder = "";
          while (parsedPath.length) {
            currentFolder = `${currentFolder}/${parsedPath[0]}`;
            const currentFolderName = parsedPath[0];
            // console.log(currentFolderName);
            parsedPath = parsedPath.slice(1);

            if (!parsedPath.length) {
              // final file
              const file = currentFileStructure.find(
                (x) => x.path === currentFolder
              );
              if (!file) {
                currentFileStructure.push({
                  name: currentFolderName,
                  type: "file",
                  path: currentFolder,
                  content: step.code,
                });
              } else {
                file.content = step.code;
              }
            } else {
              /// in a folder
              const folder = currentFileStructure.find(
                (x) => x.path === currentFolder
              );
              if (!folder) {
                // create the folder
                currentFileStructure.push({
                  name: currentFolderName,
                  type: "folder",
                  path: currentFolder,
                  children: [],
                });
              }

              currentFileStructure = currentFileStructure.find(
                (x) => x.path === currentFolder
              )!.children!;
            }
          }
          originalFiles = finalAnswerRef;
        }
      });

    if (updateHappened) {
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
    // console.log(files);
  }, [steps, files]);

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

          const frontendSteps = parseXml(frontendResponse).map((x) => ({
            ...x,
            status: "pending" as "pending",
            code_type: "frontend" as "frontend",
          }));
          // console.log(frontendSteps)

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
          <TabView selectedPhase={selectedPhase} activeTab={activeTab} onTabChange={setActiveTab} />
          <div className="h-[calc(100%-4rem)]">
            {activeTab === "code" ? (
              <FilePreview selectedFile={selectedFile} />
            ) : (
              <PreviewFrame webContainer={webContainer} />
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
