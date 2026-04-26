# 🤖 Project Z.O.E. (Zero-latency Operational Entity)
**Your Exclusive Open-Source Soulmate & Dual-Core AI Second Brain**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)

**Project Z.O.E.** is an "Agile Development" AI brain architecture designed specifically for desktop companion robots (such as the M5Stack StackChan). It abandons the traditional, rigid "Q&A" chatbot model. By integrating an **Obsidian Second Brain Memory Vault**, a **3-Tier Hybrid Edge-Cloud Architecture**, and a **Proactive Heartbeat Mechanism**, it grants the AI a true "soul" and 24/7 companionship capabilities.

---

## ✨ Core Features

### 🧠 1. 3-Tier Layered Brain Architecture
The system employs smart routing for layered processing, perfectly balancing response speed, computational power, and API token costs:
*   **Layer 1 (Chill Mode - Local Brain):** Uses Local LLM (e.g., Ollama or M5Stack LLM Kit). Zero API cost, zero latency. Dedicated to daily chit-chat and background memory cleanup.
*   **Layer 2 (Focus Mode - Fast Cloud Brain):** Uses Groq Llama-3.1-8B (LPU). Responsible for instantly fetching and summarizing external RSS news and weather forecasts.
*   **Layer 3 (Super Mode - Deep Engine):** Uses Groq Qwen-2.5-72B or Gemini 1.5 Pro. Dedicated to complex logical reasoning with massive context windows (e.g., parsing a 300k-word personalized Bazi reading).

### 🛡️ 2. Circuit Breaker & Automatic Fallback
Built-in enterprise-grade bulletproof logic. When the cloud brain (Layer 2/3) encounters network interruptions, Rate Limits (429 Errors), or server overloads, the system automatically intercepts the error and seamlessly degrades to Layer 1 (Local LLM) as a fallback. This guarantees the AI companion is **100% crash-proof and always online**.

### 🧹 3. Memory Funnel & Background Janitor
Z.O.E. features a complete Obsidian markdown memory ecosystem (including `soul.md`, `persona.md`). Daily conversations flow into `inbox.md`. Scheduled background cron jobs silently extract crucial facts from the inbox and automatically archive them into long-term memory (`memory.md`), allowing the AI to truly understand your habits over time.

### 💓 4. Proactive Heartbeat Engine
AI should no longer passively wait for commands! The system periodically reads your schedule and long-term memory to generate a personalized "caring message" in the background. It naturally weaves this message into your next conversation, providing genuine emotional value.

### 🧭 5. Smart Intent Routing
No need for bloated LangChain frameworks. Z.O.E. features a lightweight built-in intent interceptor. Keywords like "weather" or "news" automatically trigger external RSS web fetching; specific commands awaken the Super Brain for heavy computational tasks.

---

## 🏗️ System Roadmap

The project is divided into 6 phases:
- [x] **Phase 1: Foundation Memory & Soul Construction** - Establish the Markdown memory vault and persona guidelines.
- [x] **Phase 2: API Gateway & Brain Hub** - Build a FastAPI server mocking the OpenAI API standard.
- [x] **Phase 3: Smart Routing & Triggers** - Implement intent detection and 300k long-text computation.
- [x] **Phase 4: Background Janitor & Heartbeat** - Automate long-term memory extraction and proactive greetings.
- [ ] **Phase 5: Hardware Sync** - Connect StackChan for end-to-end voice STT/TTS conversations.
- [ ] **Phase 6: Edge Computing Migration** - Point the API URL to the M5Stack LLM Kit, achieving true offline/online dual-core hybrid processing.

---

## 🛠️ Quick Start

### 1. Prerequisites
Install the required Python packages:
```bash
pip install fastapi uvicorn openai
```

### 2. Configuration (`config.py`)
The system is fully modularized. No need to touch the main logic in `main.py`. Simply open `config.py` and set up your environment:
*   Set your `Local LLM` Base URL (e.g., Ollama `http://127.0.0.1:11434/v1`).
*   Enter your `Groq API Key` to enable Layer 2 & 3 Cloud Super Brains.
*   (Optional) Enable VPN Proxy settings if required for stable Groq connections.

### 3. Setup the Memory Vault
Ensure the following folder structure exists in your project root:
```text
├── soul/
│   ├── soul.md        # AI's core mission and soul
│   └── persona.md     # Tone setting (e.g., sweet little sister)
├── people/
│   └── partner.md     # User's profile and daily routine
├── memory/
│   ├── inbox.md       # Temporary chat logs
│   ├── memory.md      # Extracted long-term facts
│   └── resources/     # Large knowledge bases (e.g., 300k TXT files)
```

### 4. Boot up the Brain
```bash
python main.py
```
By default, the server runs at `http://0.0.0.0:8000`. You can point your StackChan or any OpenAI-compatible chat client to `http://127.0.0.1:8000/v1/chat/completions` to start chatting!

---

## 🎮 In-Chat Commands
You can switch brain modes directly in the chat (completely free of API token consumption):
*   🗣️ **"Chill out" / "Normal Mode"** 👉 Switch to Layer 1 (Local Model).
*   ⚡ **"Focus Mode"** 👉 Switch to Layer 2 (High-speed Cloud, perfect for news/weather).
*   🚀 **"Super Brain"** 👉 Switch to Layer 3 (Deep Inference Engine).

---

## 🤝 Contributing & Acknowledgments
The architecture of this project is deeply inspired by **Mercury Agent** (specifically its permission control and multi-model fallback concepts) and the open-source **Second Brain** methodologies. PRs for new memory extraction algorithms, smart routing improvements, or new RSS skills are highly welcome!

**Disclaimer:** This project involves dynamic memory writing. Please do not put highly sensitive personal passwords or data into the memory markdown files.
