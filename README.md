🚀 DevCycle Engine — Agentic SDLC Automation Platform

DevCycle Engine is an Agentic AI–powered SDLC Orchestrator that automates the entire software development lifecycle — from requirements → user stories → design docs → frontend/backend code → test cases → QA → deployment steps.

Built using:

FastAPI

LangGraph

Agentic AI workflows

Groq, Gemini, Anthropic LLMs

React + Vite + Tailwind frontend

Redis for state checkpointing

📦 Features
🤖 Agentic AI Workflows

AI Agents automatically:

interpret requirements

generate user stories

create functional & technical design documents

generate & revise frontend + backend code

generate test cases

perform QA review

create deployment steps

Agentic Mode supports autonomous multi-step execution with human approvals at defined nodes.

🧭 SDLC State Graph

Uses LangGraph to orchestrate the full lifecycle with:

Checkpoints

Interrupt points

Parallel LLM routing

Deterministic workflow execution

🌐 Multi-Provider LLM Support

Supports:

Google Gemini

Groq Qwen / Mixtral / Llama

Anthropic Claude
(You can enable/disable providers via .env.)

🗂️ Project Structure
sdlc-automation/
│
├── backend/
│   ├── app.py
│   ├── src/sdlccopilot/
│   ├── requirements.txt
│   └── .env.example
│
└── frontend/
    ├── index.html
    ├── vite.config.ts
    ├── tsconfig.json
    └── src/

🔧 Prerequisites
Mac

Python 3.11

Node.js ≥ 18

Redis (brew install redis)

Windows

Python 3.11

Node.js ≥ 18

Redis (install from Redis MSI or use Docker)

⚙️ Environment Variables (.env)

Create this file at:

backend/.env

# === LLM KEYS ===
GROQ_API_KEY=your_key
GOOGLE_API_KEY=your_key
ANTHROPIC_API_KEY=your_key

# === Env Modes ===
PROJECT_ENVIRONMENT=production
AGENTIC=true

# === Redis ===
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

# === LangSmith Tracing (Optional) ===
LANGSMITH_API_KEY=
LANGSMITH_PROJECT=DevCycleEngine
LANGSMITH_TRACING=true

🚀 How to Run – Backend
Mac / Linux
cd backend

python3.11 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

# Start Redis (Mac)
brew services start redis

# Run backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000

Windows (PowerShell)
cd backend

py -3.11 -m venv venv
.\venv\Scripts\activate

pip install -r requirements.txt

# Start Redis (Windows)
redis-server

# Run backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000


Backend will run at:
👉 http://127.0.0.1:8000

API docs:
👉 http://127.0.0.1:8000/docs

🎨 How to Run – Frontend
Mac / Windows
cd frontend
npm install
npm run dev


Frontend runs at:
👉 http://127.0.0.1:5173

🤖 Agentic Mode

You can toggle autonomous multi-step workflows:

Enable Agentic AI (default)
AGENTIC=true

Safe / Manual / Development Mode
AGENTIC=false
PROJECT_ENVIRONMENT=development


When disabled, the system avoids:

LLM-heavy pipelines

Multi-step autonomous loops

High-cost iterative graph execution

🧪 Test the API
Generate user stories
curl -X POST http://127.0.0.1:8000/stories/generate \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Payment App",
    "description": "UPI + Bill Payments",
    "requirements": ["UPI", "Bill Payments", "KYC", "Security"]
  }'

Review user stories
curl -X POST http://127.0.0.1:8000/stories/review/{session_id} \
  -H "Content-Type: application/json" \
  -d '{"feedback":"approved"}'

🛠️ Troubleshooting
❗ Redis Connection Error
Error 61 connecting to localhost:6379


Fix:

brew services start redis   # Mac
redis-server                # Windows

🎯 Roadmap

 GitHub Actions CI pipeline with agentic build/test

 Multi-user session mode

 Plugin system for new SDLC nodes

 Add RAG knowledge-base for company SDLC policies

📝 License

MIT License.
