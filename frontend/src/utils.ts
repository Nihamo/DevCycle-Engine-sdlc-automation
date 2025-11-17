import { Step, StepType } from "./types";

/**
 * Parse the LLM response and convert it into steps.
 *
 * Example input:
 * <boltArtifact id="project-import" title="Project Files">
 *   <boltAction type="file" filePath="eslint.config.js">
 *      import js from '@eslint/js';
 *      import globals from 'globals';
 *   </boltAction>
 *   <boltAction type="shell">
 *      node index.js
 *   </boltAction>
 * </boltArtifact>
 *
 * Example output:
 * [{
 *      title: "Project Files",
 *      status: "pending"
 * }, {
 *      title: "Create eslint.config.js",
 *      type: StepType.CreateFile,
 *      code: "import js from '@eslint/js';\nimport globals from 'globals';\n"
 * }, {
 *      title: "Run command",
 *      code: "node index.js",
 *      type: StepType.RunScript
 * }]
 */
export function parseXml(response: string): Step[] {
  // Clean the response by trimming whitespace
  const cleanedResponse = response.trim();
  // console.log("Cleaned response:", cleanedResponse);

  // Remove any text before the first occurrence of <boltArtifact>
  const artifactIndex = cleanedResponse.indexOf("<boltArtifact");
  if (artifactIndex === -1) {
    console.warn("No <boltArtifact> tag found in response:", cleanedResponse);
    return [];
  }
  const artifactString = cleanedResponse.slice(artifactIndex);
  
  // Try to match the XML content from <boltArtifact> to the closing tag, or to the end of the string if no closing tag exists.
  const xmlMatch = artifactString.match(/<boltArtifact[^>]*>([\s\S]*?)(<\/boltArtifact>|$)/);
  if (!xmlMatch) {
    console.warn("No valid <boltArtifact> block found in artifactString:", artifactString);
    return [];
  }

  // xmlMatch[1] holds the inner content of the artifact tag.
  const xmlContent = xmlMatch[1];
  const steps: Step[] = [];
  let stepsId = 1;

  // Extract the artifact's title (defaulting to "Project Files" if not found)
  const titleMatch = xmlContent.match(/title="([^"]*)"/);
  const artifactsTitle = titleMatch ? titleMatch[1] : "Project Files";

  // Add an initial artifact step as a folder
  steps.push({
    id: stepsId++,
    title: artifactsTitle,
    description: "",
    status: "pending",
    type: StepType.CreateFolder,
  });

  // Regular expression to find boltAction tags.
  const actionRegex = /<boltAction\s+type="([^"]*)"(?:\s+filePath="([^"]*)")?>([\s\S]*?)<\/boltAction>/g;
  let match;
  
  // Process each <boltAction> tag found
  while ((match = actionRegex.exec(xmlContent)) !== null) {
    const [, type, filePath, content] = match;

    if (type === "file") {
      // Create a file creation step
      steps.push({
        id: stepsId++,
        title: filePath,
        description: "",
        status: "pending",
        type: StepType.CreateFile,
        code: content.trim(),
        path: filePath,
      });
    } else if (type === "shell") {
      // Create a shell command step
      steps.push({
        id: stepsId++,
        title: filePath,
        description: "",
        status: "pending",
        type: StepType.RunScript,
        code: content.trim(),
      });
    }
  }

  return steps;
}
