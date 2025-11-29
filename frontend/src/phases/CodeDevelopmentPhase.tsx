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
  const { webContainer, isReady: webContainerReady, error: webContainerError } = useWebContainer();
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
  const [filesMounted, setFilesMounted] = useState(false);

  useEffect(() => {
    if (!webContainer || files.length === 0) {
      setFilesMounted(false);
      return;
    }

    // Ensure package.json exists - create a default one if missing
    const ensurePackageJson = (files: FileItem[]): FileItem[] => {
      const hasPackageJson = files.some(f => 
        f.name === "package.json" || 
        f.path === "package.json" ||
        (f.type === "file" && f.name?.endsWith("package.json"))
      );
      
      // Check recursively
      const checkRecursive = (fileList: FileItem[]): boolean => {
        for (const file of fileList) {
          if (file.name === "package.json" || file.path?.endsWith("/package.json") || file.path === "package.json") {
            return true;
          }
          if (file.children && checkRecursive(file.children)) {
            return true;
          }
        }
        return false;
      };
      
      if (!hasPackageJson && !checkRecursive(files)) {
        console.warn("package.json not found in files, creating default package.json");
        // Create a default package.json for React + Vite project
        const defaultPackageJson = {
          name: "vite-react-typescript-starter",
          private: true,
          version: "0.0.0",
          type: "module",
          scripts: {
            dev: "vite",
            build: "vite build",
            lint: "eslint .",
            preview: "vite preview"
          },
          dependencies: {
            "react": "^18.3.1",
            "react-dom": "^18.3.1",
            "react-router-dom": "^6.22.3",
            "lucide-react": "^0.344.0"
          },
          devDependencies: {
            "@types/react": "^18.3.5",
            "@types/react-dom": "^18.3.0",
            "@vitejs/plugin-react": "^4.3.1",
            "typescript": "^5.5.3",
            "vite": "^5.4.2",
            "tailwindcss": "^3.4.1",
            "autoprefixer": "^10.4.18",
            "postcss": "^8.4.35"
          }
        };
        
        return [
          {
            name: "package.json",
            type: "file" as const,
            path: "package.json",
            content: JSON.stringify(defaultPackageJson, null, 2),
          },
          ...files
        ];
      }
      
      return files;
    };

    // Also ensure index.html exists for Vite
    const ensureIndexHtml = (files: FileItem[]): FileItem[] => {
      const hasIndexHtml = files.some(f => 
        f.name === "index.html" || 
        f.path === "index.html"
      );
      
      if (!hasIndexHtml) {
        console.warn("index.html not found in files, creating default index.html");
        const defaultIndexHtml = `<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Vite + React + TS</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>`;
        
        return [
          {
            name: "index.html",
            type: "file" as const,
            path: "index.html",
            content: defaultIndexHtml,
          },
          ...files
        ];
      }
      
      return files;
    };

    let filesWithDefaults = ensurePackageJson(files);
    filesWithDefaults = ensureIndexHtml(filesWithDefaults);

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

    const mountStructure = createMountStructure(filesWithDefaults);
    console.log("Mount structure:", JSON.stringify(mountStructure, null, 2));
    console.log("Files to mount:", files);
    console.log("Files to mount (detailed):", files.map(f => ({
      name: f.name,
      type: f.type,
      path: f.path,
      hasContent: !!f.content,
      contentLength: f.content?.length || 0,
      childrenCount: f.children?.length || 0
    })));
    
    // Check if package.json exists in files
    const hasPackageJson = files.some(f => 
      f.name === "package.json" || 
      f.path === "package.json" ||
      (f.type === "file" && f.name?.endsWith("package.json"))
    );
    console.log("Has package.json in files:", hasPackageJson);
    
    // Also check recursively in folders
    const checkForPackageJson = (fileList: FileItem[]): boolean => {
      for (const file of fileList) {
        if (file.name === "package.json" || file.path?.endsWith("/package.json") || file.path === "package.json") {
          return true;
        }
        if (file.children) {
          if (checkForPackageJson(file.children)) return true;
        }
      }
      return false;
    };
    console.log("Has package.json (recursive):", checkForPackageJson(files));
    
    // Mount the structure if WebContainer is available
    webContainer.mount(mountStructure).then(async () => {
      console.log("Files mounted successfully");
      
      // Verify package.json exists after mounting
      try {
        const packageJson = await webContainer.fs.readFile("package.json", "utf-8");
        console.log("package.json found after mount:", packageJson.substring(0, 200));
      } catch (err) {
        console.error("package.json NOT found after mount:", err);
        // List root directory to see what's actually there
        try {
          const rootFiles = await webContainer.fs.readdir(".", { withFileTypes: true });
          console.log("Root directory contents:", rootFiles.map(f => f.name));
        } catch (listErr) {
          console.error("Error listing root directory:", listErr);
        }
      }
      
      setFilesMounted(true);
    }).catch((error) => {
      console.error("Error mounting files:", error);
      setFilesMounted(false);
    });
  }, [files, webContainer]);

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
          <TabView selectedPhase={selectedPhase} activeTab={activeTab} onTabChange={setActiveTab} />
          <div className="h-[calc(100%-4rem)]">
            {activeTab === "code" ? (
              <FilePreview selectedFile={selectedFile} />
            ) : (
              <PreviewFrame 
                webContainer={webContainer} 
                filesMounted={filesMounted}
                isFrontend={selectedPhase === "frontend-coding"}
                webContainerReady={webContainerReady}
                webContainerError={webContainerError}
              />
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
