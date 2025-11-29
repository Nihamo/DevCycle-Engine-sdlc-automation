import React, { createContext, useContext, useEffect, useState, useRef } from "react";
import { WebContainer } from "@webcontainer/api";

interface WebContainerContextType {
  webContainer: WebContainer | undefined;
  isReady: boolean;
  error: string;
}

const WebContainerContext = createContext<WebContainerContextType>({
  webContainer: undefined,
  isReady: false,
  error: "",
});

// Singleton instance to prevent multiple boots
let webContainerInstance: WebContainer | null = null;
let bootPromise: Promise<WebContainer> | null = null;
let isBooting = false;

export function WebContainerProvider({ children }: { children: React.ReactNode }) {
  const [webContainer, setWebContainer] = useState<WebContainer | undefined>(undefined);
  const [isReady, setIsReady] = useState(false);
  const [error, setError] = useState<string>("");
  const hasInitialized = useRef(false);

  useEffect(() => {
    // Only boot once
    if (hasInitialized.current) return;
    hasInitialized.current = true;

    async function bootWebContainer() {
      try {
        // If already booted, use existing instance
        if (webContainerInstance) {
          console.log("Using existing WebContainer instance");
          setWebContainer(webContainerInstance);
          setIsReady(true);
          return;
        }

        // If currently booting, wait for it
        if (isBooting && bootPromise) {
          console.log("WebContainer is already booting, waiting...");
          webContainerInstance = await bootPromise;
          setWebContainer(webContainerInstance);
          setIsReady(true);
          return;
        }

        // Start booting
        console.log("Booting WebContainer...");
        isBooting = true;
        bootPromise = WebContainer.boot();
        
        webContainerInstance = await bootPromise;
        isBooting = false;
        bootPromise = null;
        
        console.log("WebContainer booted successfully");
        setWebContainer(webContainerInstance);
        setIsReady(true);
      } catch (err: any) {
        console.error("Error booting WebContainer:", err);
        setError(err.message || "Failed to initialize WebContainer");
        isBooting = false;
        bootPromise = null;
        hasInitialized.current = false; // Allow retry
      }
    }

    bootWebContainer();
  }, []);

  return (
    <WebContainerContext.Provider value={{ webContainer, isReady, error }}>
      {children}
    </WebContainerContext.Provider>
  );
}

export function useWebContainer() {
  const context = useContext(WebContainerContext);
  if (!context) {
    throw new Error("useWebContainer must be used within WebContainerProvider");
  }
  return context;
}

