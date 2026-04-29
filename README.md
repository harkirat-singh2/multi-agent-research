# 🧠 Multi-Agent Research AI System

A **full-stack AI-powered research assistant** that uses multiple agents to search, scrape, analyze, and generate structured reports in real-time with streaming output.

---

## 🚀 Live Demo

* 🌐 Frontend:https://multi-agentresearch.netlify.app/
* ⚡ Backend API: https://multi-agent-research-a9s2.onrender.com
* 📘 API Docs: https://multi-agent-research-a9s2.onrender.com/docs

---

## ✨ Features

* 🔍 **Search Agent** – Finds relevant information from the web
* 📖 **Reader Agent** – Scrapes and extracts meaningful content
* ✍️ **Writer Agent** – Generates structured research reports
* 🧠 **Critic Agent** – Evaluates report quality and provides feedback
* ⚡ **Streaming Responses** – Real-time output like ChatGPT
* 🌐 **Live Deployment** – Fully deployed frontend + backend
* 🔗 **Source Extraction** – Displays references used in research

---

## 🧠 System Architecture

```
User Query
   ↓
Search Agent (web search)
   ↓
Reader Agent (scraping)
   ↓
Writer Chain (report generation)
   ↓
Critic Chain (evaluation)
   ↓
Streaming Response → Frontend UI
```

---

## 🛠️ Tech Stack

### Backend

* ⚡ FastAPI
* 🧠 LangChain
* 🤖 NVIDIA AI Endpoints (LLM)
* 🔍 Tavily (Web Search)
* 🐍 Python 3.11

### Frontend

* 🌐 HTML, CSS, JavaScript
* ⚡ Streaming Fetch API

### Deployment

* 🚀 Render (Backend)
* 🌍 Netlify (Frontend)

---

## 📁 Project Structure

```
multi-agent-research/
│
├── app/
│   ├── agents/        # Search & Reader agents
│   ├── chains/        # Writer & Critic chains
│   ├── tools/         # Web search & scraper tools
│   ├── pipeline/      # Research pipeline (core logic)
│   └── api/           # FastAPI routes
│
├── frontend/          # UI (index.html)
├── main.py            # FastAPI entry point
├── requirements.txt
├── start.sh
└── .env
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repo

```
git clone https://github.com/your-username/multi-agent-research.git
cd multi-agent-research
```

---

### 2️⃣ Install dependencies

```
pip install -r requirements.txt
```

---

### 3️⃣ Add environment variables

Create a `.env` file:

```
NVIDIA_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
```

---

### 4️⃣ Run backend

```
uvicorn main:app --reload
```

Open:

```
http://127.0.0.1:8000/docs
```

---

### 5️⃣ Run frontend

Open:

```
frontend/index.html
```

OR use Live Server in VS Code

---

## 🔌 API Endpoints

### Streaming Research

```
GET /research/stream?query=your_topic
```

👉 Returns real-time streaming response

---

## 🧪 Example Query

```
Latest advancements in AI agents in 2025
```

---

## 📸 Demo Flow

* User enters query
* Agents process in pipeline
* Report streams live
* Critique and sources appear

---

## ⚠️ Notes

* First request may be slow (Render cold start)
* Requires valid API keys
* Tavily improves search quality significantly

---

## 🔥 Future Improvements

* 🧠 LangGraph integration (advanced orchestration)
* 📄 Export report as PDF
* 🎨 Markdown rendering for rich UI
* 📊 Add memory & vector database (RAG)

---

## 💡 Key Highlights (Resume Ready)

* Built a **multi-agent AI system** using LangChain
* Implemented **real-time streaming architecture**
* Designed **modular, scalable backend**
* Integrated **external tools (search + scraping)**
* Deployed full-stack app using **Render + Netlify**

---

## 📜 License

MIT License

---

## 🙌 Acknowledgements

* LangChain
* NVIDIA AI Endpoints
* Tavily Search API
* FastAPI

---
