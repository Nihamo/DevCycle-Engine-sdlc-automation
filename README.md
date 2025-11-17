

# 🚀 DevCycle Engine — Agentic SDLC Automation Platform

DevCycle Engine is an **Agentic AI–powered SDLC Orchestrator** that automates the entire software development lifecycle — from requirements → user stories → design docs → frontend/backend code → test cases → QA → deployment steps.

Built using:
- FastAPI (Backend)
- React + Vite + Tailwind (Frontend)
- LangGraph Agentic Workflows
- Redis for Checkpointing
- LLMs: Groq, Gemini, Anthropic

---

## 📦 Features

### 🤖 Agentic AI Automation
AI Agents automatically:
- Interpret requirements
- Generate & revise user stories
- Create functional & technical design documents
- Generate frontend & backend code
- Produce test cases
- Perform QA testing
- Generate deployment steps

Includes **interrupt points** → human approval required at key nodes.

---

## 🗂️ Project Structure



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



---

## 🔧 Prerequisites

### Mac
- Python 3.11
- Node.js ≥ 18
- Redis (`brew install redis`)

### Windows
- Python 3.11
- Node.js ≥ 18
- Redis (MSI installer or Docker)

---

## ⚙️ Environment Variables (.env)

Create file: `backend/.env`



# === LLM KEYS ===

GROQ_API_KEY=your_key_here

GOOGLE_API_KEY=your_key_here

ANTHROPIC_API_KEY=your_key_here

# === Env Modes ===

PROJECT_ENVIRONMENT=production

AGENTIC=true

# === Redis ===

REDIS_HOST=localhost

REDIS_PORT=6379

REDIS_PASSWORD=

# === LangSmith (Optional) ===

LANGSMITH_API_KEY=

LANGSMITH_PROJECT=DevCycleEngine

LANGSMITH_TRACING=true



---

# 🚀 Running the Backend

## Mac / Linux

cd backend

python3.11 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

# Start Redis (Mac)
brew services start redis

# Run backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000


## Windows (PowerShell)


cd backend

py -3.11 -m venv venv
.\venv\Scripts\activate

pip install -r requirements.txt

# Start Redis
redis-server

# Run backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000


Backend URL:
👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)

API Docs:
👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

# 🎨 Running the Frontend


cd frontend
npm install
npm run dev


Frontend URL:
👉 [http://127.0.0.1:5173](http://127.0.0.1:5173)

---

# 🤖 Agentic Mode (Autonomous SDLC)

Enable autonomous multi-step AI:


AGENTIC=true
PROJECT_ENVIRONMENT=production


Disable autonomous mode (manual + safe):


AGENTIC=false
PROJECT_ENVIRONMENT=development


---

# 🧪 Test the API Quickly

### Generate user stories


curl -X POST http://127.0.0.1:8000/stories/generate \
  -H "Content-Type: application/json" \
  -d '{
    "title": "UPI App",
    "description": "A payments app",
    "requirements": ["UPI", "KYC", "Security"]
  }'


### Approve user stories


curl -X POST http://127.0.0.1:8000/stories/review/{session_id} \
  -H "Content-Type: application/json" \
  -d '{"feedback":"approved"}'


---

# 🛠️ Troubleshooting

### Redis Error: Connection Refused

Error 61 connecting to localhost:6379


Fix:


brew services start redis       # Mac
redis-server                    # Windows


---

# 🎯 Roadmap

* Multi-user SDLC graph sessions
* Plugin-based SDLC node system
* GitHub integration (agentic PR creation)
* RAG for SDLC standards & compliance

---

# 📝 License

MIT License.



---

If you want:
✅ an ASCII logo  
✅ badges  
✅ diagrams  
Just tell me — I’ll format everything in copy-paste blocks.

