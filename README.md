Vimal R---Backend Dev ---Capstone Sandbox — Full Agent Pipeline

# Nexus Intelligence Suite 🌌

A premium, end-to-end multi-agent orchestration pipeline built with **LangGraph**, **Groq**, and **FastAPI**. This suite automates complex research tasks by coordinating specialized AI agents with persistent memory and real-time tool-calling.

## 🚀 Features

- **Multi-Agent Pipeline**:
  - `Researcher Agent`: Uses DuckDuckGo to find real-time data.
  - `Writer Agent`: Synthesizes data into high-quality executive reports.
- **Persistent Memory**: SQLite-backed checkpointer ensures agents remember context across reloads.
- **Tool-Calling**: Seamless integration with web search tools.
- **Premium Glassmorphic UI**: High-end React interface with real-time thought logging and dark mode aesthetics.

## 🛠️ Tech Stack

- **Backend**: Python, LangChain, LangGraph, FastAPI, SQLite.
- **Frontend**: React (Vite), Vanilla CSS (Glassmorphism).
- **LLM**: Groq (Llama 3.1 70B).

## 📂 Project Structure

```text
src/
├── backend/
│   ├── agents/      # Agent logic & LangGraph definition
│   ├── tools/       # Tool implementations (Web Search)
│   ├── core/        # State & Memory management
│   └── api/         # FastAPI endpoints
├── ui/              # Vite + React Frontend
└── main.py          # Backend entry point
```

## 🚥 Getting Started

### 1. Backend Setup

1. **Environment Variables**:
   Copy `.env.example` to `.env` and add your **GROQ_API_KEY**.
   ```bash
   cp .env.example .env
   ```

2. **Install Dependencies**:
   ```bash
   python -m pip install -r requirements.txt
   ```

3. **Run Server**:
   ```bash
   python main.py
   ```
   The API will be available at `http://localhost:8000`.

### 2. Frontend Setup

1. **Install Dependencies**:
   ```bash
   cd src/ui
   npm install
   ```

2. **Run UI**:
   ```bash
   npm run dev
   ```
   Open the browser at the provided Vite URL (usually `http://localhost:5173`).

## 🧪 Usage

1. Enter a research query in the search bar.
2. Click **"Submit"**.
3. Watch the **Agent Log** for real-time progress.
4. Review the **Executive Report** once synthesized.
