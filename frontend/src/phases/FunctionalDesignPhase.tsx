
import React, { useState } from "react";
import { useLocation } from "react-router-dom";
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import { BACKEND_URL } from "../../config";
import { Download } from 'lucide-react';
import Loading from "../components/Loading";
import ToastError from "../components/ToastError";
import jsPDF from "jspdf";
import { marked } from "marked";

export default function FunctionalDesignPhase() {
  const location = useLocation();
  const data = location.state?.data
  const [functionalDocument, setFunctionalDocument] = useState<string>("");
  const [loading, setLoading] = useState(true);

  const sanitizeDocument = (raw: string): string => {
    if (!raw) return "";
    // Remove hidden LLM "thinking" sections wrapped in <think> tags
    let cleaned = raw.replace(/<think>[\s\S]*?<\/think>/gi, "");
    // Unwrap fenced HTML blocks like ```html ... ```
    cleaned = cleaned.replace(/```html([\s\S]*?)```/gi, "$1");
    cleaned = cleaned.replace(/```([\s\S]*?)```/gi, "$1");
    return cleaned.trim();
  };

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
    return sanitizeDocument(functionalDocument);
  }

  // Generate and download PDF using a clean, light-theme HTML version
  const handleDownload = async () => {
    const title = data?.project_requirements?.title || "FunctionalDesign";
    const doc = new jsPDF("p", "pt", "a4");
    const markdown = generateMarkdown();

    const pageWidth = doc.internal.pageSize.getWidth();
    const pageHeight = doc.internal.pageSize.getHeight();
    const margin = 72; // 1 inch
    const maxWidth = pageWidth - margin * 2;

    const ensureSpace = (cursorY: number, needed: number): number => {
      if (cursorY + needed > pageHeight - margin) {
        doc.addPage();
        return margin;
      }
      return cursorY;
    };

    const cleanInline = (text: string): string =>
      text
        // strip HTML tags like <p>, <strong>, </p>, etc.
        .replace(/<\/?[^>]+>/g, " ")
        // remove markdown emphasis / code markers
        .replace(/[*_`]/g, "")
        // remove heading hashes
        .replace(/#+\s*/g, "")
        // collapse multiple spaces
        .replace(/\s+/g, " ")
        .trim();

    // Use Times family everywhere
    doc.setFont("times", "bold");

    // Document title on first page
    let cursorY = margin;
    const docTitle = `${title} – Functional Specification Document (FSD)`;
    doc.setFontSize(16);
    const titleWrapped = doc.splitTextToSize(docTitle, maxWidth);
    doc.text(titleWrapped, margin, cursorY);
    cursorY += titleWrapped.length * 22;

    // Parse markdown into tokens
    const tokens = marked.lexer(markdown);

    let startedMajorSection = false;

    const renderHeading = (text: string, level: number) => {
      const cleaned = cleanInline(text);
      if (!cleaned) return;

      if (level === 1) {
        // Level 1 (main sections): new page, center aligned, 14pt
        if (startedMajorSection) {
          doc.addPage();
          cursorY = margin;
        } else {
          startedMajorSection = true;
          cursorY = ensureSpace(cursorY, 14);
        }
        cursorY += 14;
        doc.setFont("times", "bold");
        doc.setFontSize(14);
        
        const wrapped = doc.splitTextToSize(cleaned, maxWidth);
        cursorY = ensureSpace(cursorY, wrapped.length * 18);
        // Center align level 1 headings
        wrapped.forEach((line) => {
          const textWidth = doc.getTextWidth(line);
          const xPos = (pageWidth - textWidth) / 2;
          doc.text(line, xPos, cursorY);
          cursorY += 18;
        });
        cursorY += 8;
      } else {
        // Level 2+ (subheadings): same page, left aligned, 12pt
        cursorY += 14;
        doc.setFont("times", "bold");
        doc.setFontSize(12);
        
        const wrapped = doc.splitTextToSize(cleaned, maxWidth);
        cursorY = ensureSpace(cursorY, wrapped.length * 16);
        // Left align subheadings
        doc.text(wrapped, margin, cursorY);
        cursorY += wrapped.length * 16 + 8;
      }
    };

    const renderParagraph = (text: string) => {
      const cleaned = cleanInline(text);
      if (!cleaned) return;
      doc.setFont("times", "normal");
      doc.setFontSize(12);
      const wrapped = doc.splitTextToSize(cleaned, maxWidth);
      wrapped.forEach((line) => {
        cursorY = ensureSpace(cursorY, 16);
        doc.text(line, margin, cursorY);
        cursorY += 16;
      });
      cursorY += 4; // small gap
    };

    const renderList = (items: marked.Tokens.ListItem[], ordered: boolean) => {
      doc.setFont("times", "normal");
      doc.setFontSize(12);
      items.forEach((item, index) => {
        const bullet = ordered ? `${index + 1}. ` : "• ";
        // Prefer raw text from the token instead of rendered HTML
        const rawText = (item as any).text ? String((item as any).text) : marked.parser(item.tokens || []);
        const cleaned = cleanInline(rawText);
        if (!cleaned) return;
        const wrapped = doc.splitTextToSize(`${bullet}${cleaned}`, maxWidth);
        wrapped.forEach((line) => {
          cursorY = ensureSpace(cursorY, 16);
          doc.text(line, margin, cursorY);
          cursorY += 16;
        });
      });
      cursorY += 4;
    };

    const renderTable = (table: marked.Tokens.Table) => {
      // Convert table content into bullet points instead of grid
      doc.setFont("times", "normal");
      doc.setFontSize(12);

      const headers = table.header.map((cell) => cleanInline(cell.text));

      table.rows.forEach((row, rowIndex) => {
        const cells = row.map((cell) => cleanInline(cell.text));

        // Build a descriptive bullet from header → value pairs
        const parts: string[] = [];
        cells.forEach((value, idx) => {
          const label = headers[idx] || `Col${idx + 1}`;
          if (value) {
            parts.push(`${label}: ${value}`);
          }
        });

        if (parts.length === 0) {
          return;
        }

        const bulletPrefix = "• ";
        const bulletText = `${bulletPrefix}${parts.join("; ")}`;
        const wrapped = doc.splitTextToSize(bulletText, maxWidth);

        wrapped.forEach((line) => {
          cursorY = ensureSpace(cursorY, 16);
          doc.text(line, margin, cursorY);
          cursorY += 16;
        });

        // Extra spacing between table rows rendered as bullets
        cursorY += 4;
      });

      cursorY += 8;
    };

    for (const token of tokens) {
      switch (token.type) {
        case "heading":
          renderHeading((token as marked.Tokens.Heading).text, (token as marked.Tokens.Heading).depth);
          break;
        case "paragraph":
          renderParagraph((token as marked.Tokens.Paragraph).text);
          break;
        case "list":
          renderList((token as marked.Tokens.List).items, (token as marked.Tokens.List).ordered ?? false);
          break;
        case "table":
          renderTable(token as marked.Tokens.Table);
          break;
        case "space":
          cursorY += 8;
          break;
        default:
          // Fallback: if token has text, render as paragraph
          // @ts-ignore
          if (token.text) {
            // @ts-ignore
            renderParagraph(token.text as string);
          }
      }
    }

    doc.save(`${title}_functional_doc.pdf`);
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
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {generateMarkdown()}
            </ReactMarkdown>
          </div>
        </div>
      </div>
    </div>
  )
}
