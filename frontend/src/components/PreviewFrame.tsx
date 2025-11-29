import { WebContainer } from "@webcontainer/api";
import { useEffect, useState, useRef } from "react";

interface PreviewFrameProps {
  webContainer: WebContainer | undefined;
  filesMounted?: boolean;
  isFrontend?: boolean;
  webContainerReady?: boolean;
  webContainerError?: string;
}

export function PreviewFrame({ 
  webContainer, 
  filesMounted = false, 
  isFrontend = true,
  webContainerReady = false,
  webContainerError = ""
}: PreviewFrameProps) {
  const [url, setUrl] = useState("");
  const [status, setStatus] = useState<"idle" | "installing" | "starting" | "ready" | "error">("idle");
  const [error, setError] = useState<string>("");
  const [debugInfo, setDebugInfo] = useState<string>("");
  const hasStartedRef = useRef(false);
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    // Cleanup timeout on unmount
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, []);

  useEffect(() => {
    if (!isFrontend) {
      setStatus("error");
      setError("Preview is only available for frontend code");
      return;
    }

    if (webContainerError) {
      setStatus("error");
      setError(`WebContainer initialization failed: ${webContainerError}`);
      return;
    }

    if (!webContainer || !webContainerReady) {
      setStatus("idle");
      setDebugInfo("Initializing WebContainer...");
      return;
    }

    if (!filesMounted) {
      setStatus("idle");
      setDebugInfo("Waiting for files to be mounted...");
      return;
    }

    if (hasStartedRef.current) return;

    async function startDevServer() {
      try {
        hasStartedRef.current = true;
        setStatus("installing");
        setError("");
        setDebugInfo("Checking package.json...");

        // Check if package.json exists
        let packageJson: string;
        try {
          // First, list the root directory to see what's there
          try {
            const rootFiles = await webContainer.fs.readdir(".", { withFileTypes: true });
            console.log("Root directory contents:", rootFiles.map(f => `${f.name} (${f.isDirectory() ? 'dir' : 'file'})`));
          } catch (listErr) {
            console.warn("Could not list root directory:", listErr);
          }
          
          packageJson = await webContainer.fs.readFile("package.json", "utf-8");
          if (!packageJson) {
            throw new Error("package.json is empty");
          }
          console.log("package.json found:", packageJson.substring(0, 200));
        } catch (err: any) {
          console.error("Error reading package.json:", err);
          
          // Try to find package.json in subdirectories
          try {
            const rootFiles = await webContainer.fs.readdir(".", { withFileTypes: true });
            console.log("Searching for package.json in:", rootFiles.map(f => f.name));
            
            // Check if there's a project folder
            for (const file of rootFiles) {
              if (file.isDirectory()) {
                try {
                  const subFiles = await webContainer.fs.readdir(file.name, { withFileTypes: true });
                  console.log(`Files in ${file.name}:`, subFiles.map(f => f.name));
                  if (subFiles.some(f => f.name === "package.json")) {
                    setError(`package.json found in subdirectory '${file.name}' but not in root. The project structure may be incorrect.`);
                    setStatus("error");
                    hasStartedRef.current = false;
                    return;
                  }
                } catch (subErr) {
                  // Ignore errors reading subdirectories
                }
              }
            }
          } catch (searchErr) {
            console.error("Error searching for package.json:", searchErr);
          }
          
          setError(`package.json not found: ${err.message}. Please ensure the project files are properly loaded and package.json is in the root directory.`);
          setStatus("error");
          hasStartedRef.current = false;
          return;
        }

        // Set up server-ready listener BEFORE starting dev server
        const serverReadyHandler = (port: number, serverUrl: string) => {
          console.log("Server ready on port:", port, "URL:", serverUrl);
          setUrl(serverUrl);
          setStatus("ready");
          setDebugInfo("");
          if (timeoutRef.current) {
            clearTimeout(timeoutRef.current);
          }
        };
        
        webContainer.on("server-ready", serverReadyHandler);

        // Set timeout for npm install (3 minutes - reduced from 5)
        setDebugInfo("Starting npm install...");
        const installTimeout = setTimeout(() => {
          console.error("npm install timeout after 3 minutes");
          setError("npm install is taking too long (>3 minutes). The project may have dependency issues. Check the console for details.");
          setStatus("error");
          hasStartedRef.current = false;
        }, 3 * 60 * 1000);

        // Install dependencies
        console.log("Spawning npm install...");
        const installProcess = await webContainer.spawn("npm", ["install"], {
          output: true,
        });
        
        // Collect install output
        let installOutput = "";
        installProcess.output.pipeTo(
          new WritableStream({
            write(data) {
              const text = new TextDecoder().decode(data);
              installOutput += text;
              console.log("[npm install]", text);
              setDebugInfo(`Installing... (check console for details)`);
            },
          })
        );
        
        // Wait for install to complete
        const installExitCode = await installProcess.exit;
        clearTimeout(installTimeout);

        console.log("npm install completed with exit code:", installExitCode);
        console.log("Install output:", installOutput);

        if (installExitCode !== 0) {
          throw new Error(`npm install failed with exit code ${installExitCode}. Check console for details.`);
        }

        console.log("Dependencies installed successfully");

        // Set timeout for dev server (2 minutes)
        setStatus("starting");
        setDebugInfo("Starting dev server...");
        const devTimeout = setTimeout(() => {
          setError("Dev server is taking too long to start. Please check the console for errors.");
          setStatus("error");
          hasStartedRef.current = false;
        }, 2 * 60 * 1000);
        timeoutRef.current = devTimeout;

        // Start dev server
        console.log("Spawning npm run dev...");
        const devProcess = await webContainer.spawn("npm", ["run", "dev"], {
          output: true,
        });
        
        let devOutput = "";
        devProcess.output.pipeTo(
          new WritableStream({
            write(data) {
              const text = new TextDecoder().decode(data);
              devOutput += text;
              console.log("[npm run dev]", text);
              // Check for common error patterns
              if (text.includes("error") || text.includes("Error") || text.includes("EADDRINUSE")) {
                setDebugInfo(`Server error detected. Check console.`);
              }
            },
          })
        );

        // Handle dev server errors
        devProcess.exit.then((code) => {
          clearTimeout(devTimeout);
          if (code !== 0) {
            console.error("Dev server exited with code:", code);
            console.error("Dev server output:", devOutput);
            setError(`Dev server exited with code ${code}. Check console for details.`);
            setStatus("error");
            hasStartedRef.current = false;
          }
        });

      } catch (err: any) {
        console.error("Error starting dev server:", err);
        setError(err.message || "Failed to start preview. Check console for details.");
        setStatus("error");
        hasStartedRef.current = false; // Allow retry
        if (timeoutRef.current) {
          clearTimeout(timeoutRef.current);
        }
      }
    }

    startDevServer();
  }, [webContainer, filesMounted, isFrontend, webContainerReady, webContainerError]);

  const handleRetry = () => {
    hasStartedRef.current = false;
    setUrl("");
    setStatus("idle");
    setError("");
  };

  return (
    <div className="h-full flex items-center justify-center text-gray-400 bg-gray-900">
      {(status === "idle" || status === "installing") && (
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="mb-2">
            {status === "installing" ? "Installing dependencies..." : "Preparing preview..."}
          </p>
          {debugInfo && (
            <p className="text-sm text-gray-500 mt-2">{debugInfo}</p>
          )}
          <p className="text-xs text-gray-600 mt-4">
            This may take a few minutes. Check the browser console for progress.
          </p>
        </div>
      )}
      {status === "starting" && (
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="mb-2">Starting development server...</p>
          {debugInfo && (
            <p className="text-sm text-gray-500 mt-2">{debugInfo}</p>
          )}
          <p className="text-xs text-gray-600 mt-4">
            Waiting for server to be ready. Check the browser console for details.
          </p>
        </div>
      )}
      {status === "error" && (
        <div className="text-center p-6 max-w-md">
          <div className="text-red-400 mb-4">
            <p className="font-semibold mb-2">Error: {error}</p>
            {debugInfo && (
              <p className="text-sm text-gray-500">{debugInfo}</p>
            )}
          </div>
          <div className="space-y-2">
            <button
              onClick={handleRetry}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md transition-colors mr-2"
            >
              Retry
            </button>
            <p className="text-xs text-gray-600 mt-4">
              Tip: Open browser console (F12) to see detailed error messages
            </p>
          </div>
        </div>
      )}
      {status === "ready" && url && (
        <iframe
          width="100%"
          height="100%"
          src={url}
          className="border-0"
          title="Preview"
          sandbox="allow-scripts allow-same-origin allow-forms allow-popups allow-modals"
        />
      )}
    </div>
  );
}
