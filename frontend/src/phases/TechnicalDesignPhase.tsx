import React, { useState } from "react";
import { useLocation } from "react-router-dom";
import { BACKEND_URL } from "../../config";
import { Download } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import Loading from "../components/Loading";
import ToastError from "../components/ToastError";
import jsPDF from "jspdf";
import { marked } from "marked";

export default function TechnicalDesignPhase() {
    const location = useLocation();
    const data = location.state?.data
    const [technicalDocument, setTechnicalDocument] = useState<string>("");
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

    const getTechnicalDesignPhaseDoc = async () => {
        setLoading(true);

        if (location.state?.["technical-design"]?.document) {
            console.log("technical-design inside")
            setTechnicalDocument(location.state?.["technical-design"]?.document);
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

            const response = await fetch(`${BACKEND_URL}/documents/technical/generate/${data.session_id}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                throw new Error("failed to call /documents/technical/generate/{{session_id}}")
            }

            const technical_doc = await response.json();

            setTechnicalDocument(technical_doc?.document || "");
            setLoading(false);

        } catch (error) {
            console.error("error calling /documents/technical/generate/{{session_id}}")
            setLoading(false)
            ToastError(error)
        }
    }

    React.useEffect(() => {
        if (data) {
            getTechnicalDesignPhaseDoc();
        }
    }, [location.state])


    const generateMarkdown = (): string => {
        return sanitizeDocument(technicalDocument);
    }


    const handleDownload = async () => {
        const title = data?.project_requirements?.title || "TechnicalDesign";
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
                .replace(/<\/?[^>]+>/g, " ")
                .replace(/[*_`]/g, "")
                .replace(/#+\s*/g, "")
                .replace(/\s+/g, " ")
                .trim();

        // Use Times everywhere
        doc.setFont("times", "bold");

        // Title on first page
        let cursorY = margin;
        const docTitle = `${title} – Technical Design Document (TDD)`;
        doc.setFontSize(16);
        const titleWrapped = doc.splitTextToSize(docTitle, maxWidth);
        doc.text(titleWrapped, margin, cursorY);
        cursorY += titleWrapped.length * 22;

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
            if (!text || typeof text !== 'string') return;
            const cleaned = cleanInline(text);
            if (!cleaned || cleaned.length === 0) return;
            doc.setFont("times", "normal");
            doc.setFontSize(12);
            const wrapped = doc.splitTextToSize(cleaned, maxWidth);
            if (wrapped.length === 0) return;
            wrapped.forEach((line) => {
                cursorY = ensureSpace(cursorY, 16);
                doc.text(line, margin, cursorY);
                cursorY += 16;
            });
            cursorY += 4;
        };

        const renderList = (items: marked.Tokens.ListItem[], ordered: boolean) => {
            doc.setFont("times", "normal");
            doc.setFontSize(12);
            items.forEach((item, index) => {
                const bullet = ordered ? `${index + 1}. ` : "• ";
                
                // Process all tokens in the list item
                let itemText = "";
                if (item.tokens && item.tokens.length > 0) {
                    item.tokens.forEach((token: any) => {
                        if (token.type === "text") {
                            itemText += token.text + " ";
                        } else if (token.type === "strong" || token.type === "em") {
                            itemText += token.text + " ";
                        } else if (token.type === "code") {
                            itemText += token.text + " ";
                        } else if (token.type === "paragraph" && token.tokens) {
                            token.tokens.forEach((t: any) => {
                                if (t.text) itemText += t.text + " ";
                            });
                        }
                    });
                } else if ((item as any).text) {
                    itemText = String((item as any).text);
                }
                
                const cleaned = cleanInline(itemText);
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
            doc.setFont("times", "normal");
            doc.setFontSize(12);

            const headers = table.header.map((cell) => cleanInline(cell.text));

            table.rows.forEach((row) => {
                const cells = row.map((cell) => cleanInline(cell.text));
                const parts: string[] = [];
                cells.forEach((value, idx) => {
                    const label = headers[idx] || `Col${idx + 1}`;
                    if (value) {
                        parts.push(`${label}: ${value}`);
                    }
                });
                if (parts.length === 0) return;

                const bulletText = `• ${parts.join("; ")}`;
                const wrapped = doc.splitTextToSize(bulletText, maxWidth);
                wrapped.forEach((line) => {
                    cursorY = ensureSpace(cursorY, 16);
                    doc.text(line, margin, cursorY);
                    cursorY += 16;
                });
                cursorY += 4;
            });

            cursorY += 8;
        };

        const renderCodeBlock = (code: marked.Tokens.Code) => {
            doc.setFont("times", "normal");
            doc.setFontSize(11);
            const codeText = code.text || "";
            const lines = codeText.split("\n");
            lines.forEach((line) => {
                if (line.trim()) {
                    const wrapped = doc.splitTextToSize(`  ${line}`, maxWidth);
                    wrapped.forEach((wrappedLine) => {
                        cursorY = ensureSpace(cursorY, 14);
                        doc.text(wrappedLine, margin, cursorY);
                        cursorY += 14;
                    });
                } else {
                    cursorY += 8;
                }
            });
            cursorY += 4;
        };

        const renderBlockquote = (quote: marked.Tokens.Blockquote) => {
            doc.setFont("times", "italic");
            doc.setFontSize(12);
            if (quote.tokens) {
                quote.tokens.forEach((token: any) => {
                    if (token.type === "paragraph" && token.text) {
                        const wrapped = doc.splitTextToSize(`  "${token.text}"`, maxWidth);
                        wrapped.forEach((line) => {
                            cursorY = ensureSpace(cursorY, 16);
                            doc.text(line, margin, cursorY);
                            cursorY += 16;
                        });
                    }
                });
            }
            cursorY += 4;
        };

        // Process all tokens, ensuring we capture everything
        for (let i = 0; i < tokens.length; i++) {
            const token = tokens[i];
            
            try {
                switch (token.type) {
                    case "heading":
                        renderHeading(
                            (token as marked.Tokens.Heading).text,
                            (token as marked.Tokens.Heading).depth
                        );
                        break;
                    case "paragraph":
                        const paraToken = token as marked.Tokens.Paragraph;
                        // Handle paragraph text directly or from tokens
                        if (paraToken.text) {
                            renderParagraph(paraToken.text);
                        } else if (paraToken.tokens && paraToken.tokens.length > 0) {
                            // Extract text from paragraph tokens
                            let paraText = "";
                            paraToken.tokens.forEach((t: any) => {
                                if (t.type === "text") {
                                    paraText += t.text + " ";
                                } else if (t.type === "strong" || t.type === "em") {
                                    paraText += t.text + " ";
                                } else if (t.type === "code") {
                                    paraText += t.text + " ";
                                }
                            });
                            if (paraText.trim()) {
                                renderParagraph(paraText.trim());
                            }
                        }
                        break;
                    case "list":
                        renderList(
                            (token as marked.Tokens.List).items,
                            (token as marked.Tokens.List).ordered ?? false
                        );
                        break;
                    case "table":
                        renderTable(token as marked.Tokens.Table);
                        break;
                    case "code":
                        renderCodeBlock(token as marked.Tokens.Code);
                        break;
                    case "blockquote":
                        renderBlockquote(token as marked.Tokens.Blockquote);
                        break;
                    case "space":
                        cursorY += 8;
                        break;
                    case "hr":
                        cursorY = ensureSpace(cursorY, 20);
                        cursorY += 20;
                        break;
                    default:
                        // Handle any other token types - try to extract text
                        // @ts-ignore
                        if (token.text) {
                            // @ts-ignore
                            renderParagraph(token.text as string);
                        } else if ((token as any).tokens) {
                            // Recursively handle nested tokens
                            // @ts-ignore
                            (token as any).tokens.forEach((t: any) => {
                                if (t.type === "paragraph" && t.text) {
                                    renderParagraph(t.text);
                                } else if (t.type === "text") {
                                    renderParagraph(t.text);
                                }
                            });
                        } else {
                            // Log unhandled token for debugging
                            console.warn("Unhandled token type:", token.type, token);
                        }
                }
            } catch (error) {
                console.error("Error rendering token:", token.type, error);
                // Continue processing other tokens
            }
        }

        doc.save(`${title}_technical_doc.pdf`);
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
                        <h1 className="text-3xl font-bold">Technical Design Phase Document</h1>
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