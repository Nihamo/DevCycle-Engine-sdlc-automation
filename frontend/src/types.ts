export interface ProjectRequirements {
  title: string;
  description: string;
  objectives: string[];
}

export interface UserStories {
  messages: string[];
  user_stories: UserStory[];
}

export interface UserStory {
  story_id: string;
  title: string;
  description: string;
  acceptance_criteria: string[];
}
export type SDLCPhase =
  | "requirements"
  | "user-stories"
  | "functional-design"
  | "technical-design"
  | "frontend-coding"
  | "backend-coding"
  | "security"
  | "testing"
  | "qa-testing"
  | "deployment"
  | "maintenance";

export interface ChatMessage {
  id: string;
  content: string;
  sender: "user" | "ai";
  timestamp: Date;
}


export interface FileItem {
  name: string;
  type: "file" | "folder";
  children?: FileItem[];
  content?: string;
  path: string;
}

export interface ProjectTask {
  id: string;
  title: string;
  status: "pending" | "in-progress" | "completed";
}


export interface Project {
  id: string;
  name: string;
  description: string;
  files: ProjectFile[];
  tasks: ProjectTask[];
}

export interface ProjectFile {
  id: string;
  name: string;
  path: string;
  content: string;
  type: "html" | "css" | "javascript" | "typescript" | "json" | "other";
}


export enum StepType {
  CreateFile,
  CreateFolder,
  EditFile,
  DeleteFile,
  RunScript,
}

export interface Step {
  id: number;
  title: string;
  description: string;
  type: StepType;
  status: "pending" | "in-progress" | "completed";
  code?: string;
  path?: string;
  code_type?: "frontend" | "backend"; // NEW: Optional property to indicate code type
}

export interface FileItem {
  name: string;
  type: "file" | "folder";
  children?: FileItem[];
  content?: string;
  path: string;
}


export interface SecurityReview {
  reviews: Review[];
}

export interface Review {
  sec_id: string;
  review: string;
  file_path: string;
  recommendation: string;
  priority: string;
}

export interface TestCases {
  testCases: TestCase[];
}

export interface QATesting {
  qaTesting: TestCase[];
}

export interface TestCase {
  test_id: string;
  description: string;
  steps: string[];
  status: string;
}