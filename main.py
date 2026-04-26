import os
import datetime
import json
import asyncio
import urllib.request
import xml.etree.ElementTree as ET
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
from openai import AsyncOpenAI

# 載入我們自訂的設定檔
import config

# ==========================================
# 0. 網絡與代理設定 (VPN 穿透)
# ==========================================
if config.NETWORK["use_proxy"]:
    os.environ["http_proxy"] = config.NETWORK["http_proxy"]
    os.environ["https_proxy"] = config.NETWORK["https_proxy"]
    os.environ["all_proxy"] = config.NETWORK["https_proxy"].replace("http", "socks5")
    print(f"🌐 [Network] 已啟用 Proxy 連線: {config.NETWORK['http_proxy']}")

app = FastAPI(title="Zoe Second Brain API Gateway (Config-driven 3-Tier Architecture)")

# ==========================================
# 1. 全域設定 (三層大腦 API 從 Config 載入)
# ==========================================
local_client = AsyncOpenAI(
    base_url=config.ENDPOINTS["local_llm_url"],
    api_key=config.API_KEYS["local"] 
)
LOCAL_MODEL = config.MODELS["local"]

cloud_client = AsyncOpenAI(
    base_url=config.ENDPOINTS["cloud_llm_url"],
    api_key=config.API_KEYS["groq"] 
)
CLOUD_MODEL_FAST = config.MODELS["cloud_fast"]
CLOUD_MODEL_SMART = config.MODELS["cloud_smart"]

# 🌟 全域狀態變數 (1=抖一抖先, 2=打醒精神, 3=超級模式)
AI_LEVEL = 1 

# ==========================================
# 2. 讀取 Markdown 記憶檔案 & 抓取 RSS
# ==========================================
def read_md_file(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def build_system_prompt():
    soul = read_md_file("soul/soul.md")
    persona = read_md_file("soul/persona.md")
    partner = read_md_file("people/partner.md")
    long_term_memory = read_md_file("memory/memory.md")
    
    base_prompt = f"{soul}\n\n{persona}\n\n【當前對話對象資訊】\n{partner}\n\n【Zoe嘅長期記憶 (重要事實)】\n{long_term_memory}"
    
    heartbeat_path = "memory/pending_heartbeat.txt"
    if os.path.exists(heartbeat_path):
        with open(heartbeat_path, "r", encoding="utf-8") as f:
            pending_msg = f.read().strip()
        os.remove(heartbeat_path) 
        if pending_msg:
            base_prompt += f"\n\n【最高系統指令：你在背景休息時，心裡面一直想對哥哥講以下這句話：「{pending_msg}」。請在你接下來的這次回覆中，非常自然、溫柔地將這句話融合在對話裡主動跟他說出來！】"
            
    return base_prompt

def fetch_rss_data(url, limit=5):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            xml_data = response.read()
        root = ET.fromstring(xml_data)
        items = []
        for item in root.findall('.//item')[:limit]:
            title = item.find('title').text if item.find('title') is not None else ""
            desc = item.find('description').text if item.find('description') is not None else ""
            items.append(f"標題：{title}\n內容：{desc}")
        return "\n\n".join(items)
    except Exception as e:
        print(f"❌ 讀取 RSS 失敗: {e}")
        return ""

# ==========================================
# 3. 寫入記憶漏斗 (Inbox)
# ==========================================
def log_to_memory(user_msg, ai_response):
    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    log_entry = f"\n### [{timestamp}]\n**哥哥:** {user_msg}\n**Zoe:** {ai_response}\n"
    os.makedirs("memory/dailynotes", exist_ok=True)
    os.makedirs("memory", exist_ok=True)
    with open("memory/inbox.md", "a", encoding="utf-8") as f:
        f.write(log_entry)
    with open(f"memory/dailynotes/{today_str}.md", "a", encoding="utf-8") as f:
        f.write(log_entry)

# ==========================================
# 4. 背景排程 (強制綁定 Layer 1 本地模型)
# ==========================================
async def janitor_task():
    print("🧹 [Janitor] Zoe 嘅大腦清道夫已啟動 (使用 Local LLM)...")
    while True:
        await asyncio.sleep(43200)
        inbox_path = "memory/inbox.md"
        memory_path = "memory/memory.md"
        inbox_content = read_md_file(inbox_path)
        if len(inbox_content.strip()) < 50:
            continue
            
        janitor_prompt = config.PROMPTS["janitor"].format(inbox_content=inbox_content)
        
        try:
            response = await local_client.chat.completions.create(
                model=LOCAL_MODEL, messages=[{"role": "user", "content": janitor_prompt}], temperature=0.2 
            )
            summary = response.choices.message.content if len(response.choices) > 0 else ""
            if summary:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                with open(memory_path, "a", encoding="utf-8") as f:
                    f.write(f"\n### 記憶提煉 ({timestamp})\n{summary}\n")
                with open(inbox_path, "w", encoding="utf-8") as f:
                    f.write("")
                print("🧹 [Janitor] 記憶提煉完成！")
        except Exception as e:
            pass

async def heartbeat_task():
    print("💓 [Heartbeat] 主動心跳引擎已啟動 (使用 Local LLM)...")
    while True:
        await asyncio.sleep(28800)
        partner_info = read_md_file("people/partner.md")
        long_term_memory = read_md_file("memory/memory.md")
        
        heartbeat_prompt = config.PROMPTS["heartbeat"].format(partner_info=partner_info, long_term_memory=long_term_memory)
        
        try:
            response = await local_client.chat.completions.create(
                model=LOCAL_MODEL, messages=[{"role": "user", "content": heartbeat_prompt}], temperature=0.8
            )
            heartbeat_msg = response.choices.message.content if len(response.choices) > 0 else ""
            if heartbeat_msg:
                with open("memory/pending_heartbeat.txt", "w", encoding="utf-8") as f:
                    f.write(heartbeat_msg.strip())
        except Exception as e:
            pass

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(janitor_task())
    asyncio.create_task(heartbeat_task())

# ==========================================
# 🔧 嚴格符合 OpenAI 格式的系統回應生成器
# ==========================================
async def stream_system_msg(text):
    chunk = {
        "id": "chatcmpl-sys",
        "object": "chat.completion.chunk",
        "model": "system-mode",
        "choices": [{"index": 0, "delta": {"role": "assistant", "content": text}}]
    }
    yield f"data: {json.dumps(chunk)}\n\n"
    yield "data: [DONE]\n\n"

def get_system_json_response(text):
    return JSONResponse(content={
        "id": "chatcmpl-sys",
        "object": "chat.completion",
        "model": "system-mode",
        "choices": [{"index": 0, "message": {"role": "assistant", "content": text}, "finish_reason": "stop"}]
    })

# ==========================================
# 5. API 網關與 🧭 三層智能路由
# ==========================================
@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    global AI_LEVEL 
    
    data = await request.json()
    is_stream = data.get("stream", False)
    
    messages = data.get("messages", [])
    user_message = ""
    for msg in reversed(messages):
        if msg.get("role") == "user":
            raw_content = msg.get("content", "")
            if isinstance(raw_content, list):
                user_message = "".join([part.get("text", "") for part in raw_content if part.get("type") == "text"])
            else:
                user_message = str(raw_content)
            break

    # 🕹️ 三層模式切換攔截 (完全在本地處理)
    if "抖一抖先" in user_message or "回復普通模式" in user_message:
        AI_LEVEL = 1
        sys_reply = config.SYS_MESSAGES["layer1"]
        log_to_memory(user_message, sys_reply)
        print("🟢 [Mode Switch] 切換至 Layer 1 (Local LLM)")
        return StreamingResponse(stream_system_msg(sys_reply), media_type="text/event-stream") if is_stream else get_system_json_response(sys_reply)
            
    if "打醒精神" in user_message:
        AI_LEVEL = 2
        sys_reply = config.SYS_MESSAGES["layer2"]
        log_to_memory(user_message, sys_reply)
        print("🟢 [Mode Switch] 切換至 Layer 2 (Groq 8B Fast)")
        return StreamingResponse(stream_system_msg(sys_reply), media_type="text/event-stream") if is_stream else get_system_json_response(sys_reply)

    if "超級模式" in user_message or "啟動超級大腦" in user_message:
        AI_LEVEL = 3
        sys_reply = config.SYS_MESSAGES["layer3"]
        log_to_memory(user_message, sys_reply)
        print("🟢 [Mode Switch] 切換至 Layer 3 (Groq 72B Smart)")
        return StreamingResponse(stream_system_msg(sys_reply), media_type="text/event-stream") if is_stream else get_system_json_response(sys_reply)

    system_instruction = build_system_prompt()
    
    # 🧠 決定使用邊層大腦
    active_client = local_client if AI_LEVEL == 1 else cloud_client
    if AI_LEVEL == 1:
        active_model = LOCAL_MODEL
    elif AI_LEVEL == 2:
        active_model = CLOUD_MODEL_FAST
    else:
        active_model = CLOUD_MODEL_SMART

    # 🧭 內容路由判定
    routing_prompt = ""
    if "天氣" in user_message:
        print(f"🧭 [Router] 讀取天氣 RSS (使用大腦 Layer {AI_LEVEL}: {active_model})")
        weather_warning = fetch_rss_data("https://rss.weather.gov.hk/rss/WeatherWarningBulletin_uc.xml", limit=2)
        local_forecast = fetch_rss_data("https://rss.weather.gov.hk/rss/LocalWeatherForecast_uc.xml", limit=1)
        weather_data = f"【天氣警告】\n{weather_warning}\n\n【本港天氣預報】\n{local_forecast}"
        routing_prompt = config.PROMPTS["weather"].format(data=weather_data)
        
    elif "世界政治" in user_message or "國際政治" in user_message:
        print(f"🧭 [Router] 讀取世界政治 RSS (使用大腦 Layer {AI_LEVEL}: {active_model})")
        news_data = fetch_rss_data("https://feeds.bbci.co.uk/news/politics/rss.xml", limit=5)
        routing_prompt = config.PROMPTS["politics"].format(data=news_data)

    elif "世界新聞" in user_message or "國際新聞" in user_message:
        print(f"🧭 [Router] 讀取世界新聞 RSS (使用大腦 Layer {AI_LEVEL}: {active_model})")
        news_data = fetch_rss_data("https://feeds.bbci.co.uk/news/rss.xml", limit=5)
        routing_prompt = config.PROMPTS["world_news"].format(data=news_data)
        
    elif "新聞" in user_message or "發生咩事" in user_message:
        print(f"🧭 [Router] 讀取香港新聞 RSS (使用大腦 Layer {AI_LEVEL}: {active_model})")
        news_data = fetch_rss_data("https://rthk.hk/rthk/news/rss/c_expressnews_clocal.xml", limit=5)
        routing_prompt = config.PROMPTS["local_news"].format(data=news_data)
        
    elif AI_LEVEL == 3 and ("八字" in user_message or "迷惘" in user_message):
        print(f"🔮 [Router] 觸發八字解盤 (使用大腦 Layer 3: {active_model})")
        bazi_data = read_md_file("memory/resources/姜氏八字內核 v2.8.txt")
        routing_prompt = config.PROMPTS["bazi"].format(data=bazi_data, user_message=user_message)

    if routing_prompt:
        lm_studio_messages = [{"role": "system", "content": system_instruction}, {"role": "user", "content": routing_prompt}]
    else:
        print(f"🧭 [Router] 觸發日常閒聊模式 (使用大腦 Layer {AI_LEVEL}: {active_model})")
        lm_studio_messages = [{"role": "system", "content": system_instruction}, {"role": "user", "content": user_message}]

    # 🛡️ 執行推理與「斷路器自動降級」
    async def generate_with_fallback():
        try:
            response_stream = await active_client.chat.completions.create(
                model=active_model, messages=lm_studio_messages, stream=True, temperature=0.7
            )
        except Exception as e:
            error_str = str(e).lower()
            if AI_LEVEL > 1 and ("429" in error_str or "too many requests" in error_str or "error" in error_str):
                print(f"🛡️ [Circuit Breaker] 雲端大腦超載或連線出錯，自動降級至 Layer 1 (Local LLM) 兜底...")
                response_stream = await local_client.chat.completions.create(
                    model=LOCAL_MODEL, messages=lm_studio_messages, stream=True, temperature=0.7
                )
            else:
                raise e

        full_reply = ""
        async for chunk in response_stream:
            for choice in chunk.choices:
                if choice.delta and choice.delta.content:
                    content = choice.delta.content
                    full_reply += content
            yield f"data: {chunk.model_dump_json()}\n\n"
        
        yield "data: [DONE]\n\n"
        log_to_memory(user_message, full_reply)

    if is_stream:
        return StreamingResponse(generate_with_fallback(), media_type="text/event-stream")
    else:
        try:
            response = await active_client.chat.completions.create(
                model=active_model, messages=lm_studio_messages, stream=False, temperature=0.7
            )
        except Exception as e:
            if AI_LEVEL > 1:
                print(f"🛡️ [Circuit Breaker] 雲端大腦超載，自動降級至 Layer 1...")
                response = await local_client.chat.completions.create(
                    model=LOCAL_MODEL, messages=lm_studio_messages, stream=False, temperature=0.7
                )
            else:
                raise e
                
        ai_reply = response.choices.message.content if len(response.choices) > 0 else ""
        log_to_memory(user_message, ai_reply)
        return JSONResponse(content=response.model_dump())

if __name__ == "__main__":
    import uvicorn
    print(f"🚀 啟動 Zoe 第二大腦 API Gateway (模組化 Config 版)...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
