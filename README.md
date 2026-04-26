# 🤖 Project Z.O.E. (Zero-latency Operational Entity) 
**你的專屬開源靈魂伴侶與雙核 AI 第二大腦**

**Project Z.O.E.** 是一個專為桌面陪伴機械人（如 M5Stack StackChan）設計的「敏捷開發 (Agile Development)」AI 大腦架構。它拋棄了傳統 AI 助手「一問一答」的死板模式，透過 **Obsidian 第二大腦記憶庫**、**三層邊緣與雲端混合架構 (Hybrid Edge-Cloud)**、以及 **主動心跳機制**，賦予 AI 真正的「靈魂」與全天候陪伴能力。

---

## ✨ 核心亮點 (Core Features)

### 🧠 1. 三層分流大腦架構 (3-Tier Architecture)
系統採用智能分層處理，極致平衡反應速度、算力與 Token 成本：
*   **Layer 1 (抖一抖先 - 節能小腦)**：預設使用 Local LLM (如 Ollama 或 M5Stack LLM Kit)。零 API 成本、零延遲，負責日常閒聊與背景記憶整理。
*   **Layer 2 (打醒精神 - 高速大腦)**：使用 Groq Llama-3.1-8B 等 LPU 極速模型。負責秒速抓取並總結外部 RSS 新聞及天氣資訊。
*   **Layer 3 (超級模式 - 深度引擎)**：使用 Groq Qwen-2.5-72B 或 Gemini 1.5 Pro。專責處理龐大 Context Window 的深度邏輯推論（如 300k 字的專屬八字解盤）。

### 🛡️ 2. 斷路器與自動降級 (Circuit Breaker & Fallback)
內建企業級防彈邏輯。當雲端大腦（Layer 2/3）遇到網絡中斷、Rate Limit (429 Error) 或伺服器超載時，系統會自動攔截錯誤，並瞬間無縫降級交由 Layer 1 (Local LLM) 兜底回覆，保證 AI 伴侶 **100% 絕不死機**。

### 🧹 3. 記憶漏斗與背景清道夫 (Memory Janitor)
Z.O.E. 擁有完整的 Obsidian 記憶生態系統（包含 `soul.md`、`persona.md` 等）。日常對話會流入 `inbox.md`，背景排程任務 (Cron Jobs) 會定時在背後默默提煉對話中的重要事實，自動歸檔至長期記憶 `memory.md`，讓 AI 伴侶真正了解你的習慣。

### 💓 4. 主動心跳引擎 (Proactive Heartbeat)
AI 不再只是被動等待指令！系統會定時讀取你的行程與長期記憶，在背景生成專屬的「主動關心語錄」，並在下次對話時自然地帶出，提供真實的情緒價值。

### 🧭 5. 智能動態路由 (Intent Routing)
不需要寫死複雜的 LangChain 邏輯，內建輕量級意圖攔截器。當聽到「天氣」、「新聞」等關鍵字，會自動觸發外部 RSS 抓取工具；當聽到特定指令，則喚醒特定的超級大腦進行運算。

---

## 🏗️ 系統藍圖與開發階段 (Roadmap)

本專案分為 6 個階段逐步推進：
- [x] **Phase 1：基礎記憶與靈魂建構** - 建立 Markdown 記憶庫與八字照顧指南。
- [x] **Phase 2：API 網關與大腦中樞** - 建立 FastAPI 偽裝 OpenAI Server。
- [x] **Phase 3：智能路由與八字觸發** - 實作意圖判定與 300k 長文本運算。
- [x] **Phase 4：背景清道夫與主動心跳** - 自動提煉長期記憶與主動關心。
- [ ] **Phase 5：軀殼對接** - 連接 StackChan，完成端到端語音對答與 TTS 播放。
- [ ] **Phase 6：邊緣運算無痛遷移** - 將 API URL 指向 M5Stack LLM Kit，實現真正的離線/線上雙核混合運算。

---

## 🛠️ 快速開始 (Quick Start)

### 1. 準備工作
安裝必要的 Python 套件：
```bash
pip install fastapi uvicorn openai
```

### 2. 環境設定 (`config.py`)
系統已採用模組化設計，無需修改主程式 `main.py`。請打開 `config.py` 填入你的設定：
*   設定你的 `Local LLM` (例如 Ollama) 的 Base URL。
*   輸入你的 `Groq API Key` 以啟動 Layer 2 & 3 雲端超級大腦。
*   (可選) 根據需要開啟 VPN Proxy 代理以確保 Groq 連線穩定。

### 3. 建立記憶庫
在專案根目錄確保以下資料夾結構存在：
```text
├── soul/
│   ├── soul.md        # AI 核心指令與靈魂
│   └── persona.md     # 語氣設定 (如：溫柔妹妹)
├── people/
│   └── partner.md     # 你的專屬檔案與作息
├── memory/
│   ├── inbox.md       # 日常對話暫存
│   ├── memory.md      # 長期記憶提煉區
│   └── resources/     # 存放大型知識庫 (如八字秘笈)
```

### 4. 啟動大腦
```bash
python main.py
```
預設會運行於 `http://0.0.0.0:8000`。你可以將 StackChan 或任何支援 OpenAI API 格式的 Chatbox 指向 `http://127.0.0.1:8000/v1/chat/completions` 開始對話！

---

## 🎮 指令玩法 (In-Chat Commands)
你可以在對話中直接切換大腦模式（完全不扣 Token）：
*   🗣️ **「抖一抖先」** / **「回復普通模式」** 👉 切換至 Layer 1 (本地模型)
*   ⚡ **「打醒精神」** 👉 切換至 Layer 2 (極速雲端，適合聽新聞/天氣)
*   🚀 **「啟動超級大腦」** 👉 切換至 Layer 3 (深度推論引擎)
