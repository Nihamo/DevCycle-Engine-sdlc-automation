
import React, { useState } from "react";
import { useLocation } from "react-router-dom";
import ReactMarkdown from "react-markdown"
import { BACKEND_URL } from "../../config";
import { Download } from 'lucide-react';
import { marked } from "marked"
import Loading from "../components/Loading";
import ToastError from "../components/ToastError";

export default function FunctionalDesignPhase() {
  const location = useLocation();
  const data = location.state?.data
  const [functionalDocument, setFunctionalDocument] = useState<string>("");
  const [loading, setLoading] = useState(true);

  const getFunctionalDesignPhaseDoc = async () => {
    // console.log(location.state?.["functional-design"].document)
    setLoading(true);
    if (location.state?.["functional-design"]?.document) {
      console.log("function-design inside")
      setFunctionalDocument(location.state?.["functional-design"].document);
      setLoading(false);
      return
    }
    try {
      if (!data?.session_id) {
        throw new Error("Session ID is missing");
      }
      const payload = {
        session_id: data.session_id,
        feedback: "approved",
      }

      const response = await fetch(`${BACKEND_URL}/documents/functional/generate/${data.session_id}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error("failed to call /documents/functional/generate/{{session_id}}")
      }

      const functional_doc = await response.json();
      // console.log(functional_doc?.document)
      setFunctionalDocument(functional_doc?.document || "");
      setLoading(false);

    } catch (error) {
      console.error("error calling /documents/functional/generate/{{session_id}}")
      setLoading(false);
      ToastError(error)
    }
  }

  React.useEffect(() => {
    if (data) {
      getFunctionalDesignPhaseDoc()
    }
  }, [location.state])

  const generateMarkdown = (): string => {
    return functionalDocument
  }

  // - Wraps markdown content in a minimal HTML template.
  // - Sets the MIME type to "application/msword" so that Word opens the document.
  // - Downloads the file as "FunctionalDesignPhase.doc".
  const handleDownload = () => {
    const markdownContent = generateMarkdown();
    // Convert markdown to HTML using marked
    const htmlConverted = marked(markdownContent); // NEW: Convert markdown to HTML

    // Wrap the converted HTML in a minimal HTML template with inline CSS for professional styling
    const htmlContent = `
      <html xmlns:o='urn:schemas-microsoft-com:office:office'
            xmlns:w='urn:schemas-microsoft-com:office:word'
            xmlns='http://www.w3.org/TR/REC-html40'>
        <head>
          <meta charset='utf-8'>
          <title>Functional Design Phase Document</title>
          <style>
            /* Professional styling for Word document */
            body { font-family: 'Arial', sans-serif; margin: 20px; color: #374151; }
            h1 { font-size: 24px; color: #1e40af; font-weight: bold; margin: 20px 0 10px; }
            h2 { font-size: 20px; color: #1e3a8a; font-weight: 600; margin: 18px 0 8px; }
            h3 { font-size: 18px; color: #1e3a8a; margin: 16px 0 6px; }
            p { font-size: 14px; line-height: 1.6; margin: 8px 0; }
            table { width: 100%; border-collapse: collapse; margin: 10px 0; }
            th, td { border: 1px solid #4b5563; padding: 6px 8px; font-size: 14px; }
            th { background-color: #1f2937; color: #fff; }
            pre { font-family: 'Courier New', monospace; background: #f3f4f6; padding: 10px; }
          </style>
        </head>
        <body>
          ${htmlConverted}
        </body>
      </html>`;
    const blob = new Blob([htmlContent], { type: "application/msword" });
    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    var title = data?.project_requirements?.title
    link.download = `${title}_functional_doc`
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };


  if (loading) {
    return <Loading />;
  }

  return (
    <div
      className="flex-1 p-6 overflow-y-auto bg-gray-90 bg-gray-900"
    >
      <div className="max-w-6xl mx-auto">
        <div className="bg-gray-800 rounded-lg shadow-xl p-8 border border-gray-700">
          <div className="flex justify-between items-center mb-4">
            <h1 className="text-3xl font-bold">Functional Design Phase Document</h1>
            <button
              onClick={handleDownload}
              className="bg-green-600 hover:bg-green-700 text-green-200 font-bold py-2 px-4 
                          flex gap-2 items-center justify-center rounded-full text-sm active:scale-[.9]
                          hover:scale-[1.02]"
            >
              <Download className="h-4 w-4 font-bold animate-bounce" /> Download
            </button>
          </div>
          <div
            className="
            prose prose-invert 
            max-w-none
            prose-h1:text-xl prose-h1:mt-4 prose-h1:mb-2
            prose-h2:text-lg prose-h2:mt-3 prose-h2:mb-2
            prose-h3:text-base prose-h3:mt-2 prose-h3:mb-1
            prose-p:my-2 
            prose-hr:my-4
            prose-headings:font-semibold prose-headings:text-blue-400 
            prose-strong:text-white
          "
          >
            <ReactMarkdown>{generateMarkdown()}</ReactMarkdown>
          </div>
        </div>
      </div>
    </div>
  )
}
