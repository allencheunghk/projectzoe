# config.py

# ==========================================
# 1. Network & API Settings
# ==========================================
# If you experience connection issues with Groq, set use_proxy to True and enter your VPN proxy ports.
NETWORK = {
    "use_proxy": False, 
    "http_proxy": "http://127.0.0.1:7890",
    "https_proxy": "http://127.0.0.1:7890"
}

API_KEYS = {
    "groq": "gsk_your_groq_api_key_here",
    "local": "ollama"
}

ENDPOINTS = {
    "cloud_llm_url": "https://api.groq.com/openai/v1",
    "local_llm_url": "http://127.0.0.1:11434/v1"
}

MODELS = {
    "cloud_smart": "qwen-2.5-76b-versatile",
    "cloud_fast": "llama-3.1-8b-instant",
    "local": "gemma4:e2b"
}

# ==========================================
# 2. System Messages (Mode Switching)
# ==========================================
SYS_MESSAGES = {
    "layer1": "💤 [System Switch: Layer 1 Initiated. Zoe has switched to the Local Brain (Local LLM) for power-saving companionship mode.]",
    "layer2": "⚡ [System Switch: Layer 2 Initiated. Zoe is connected to the Groq Fast Brain (Llama-3.1-8B), ready to summarize info instantly!]",
    "layer3": "🚀 [System Switch: Layer 3 Initiated. Zoe is connected to the Groq Super Engine (Qwen-2.5-72B), ready for deep logical analysis!]"
}

# ==========================================
# 3. Zoe's Brain Prompts & Routing Directives
# ==========================================
PROMPTS = {
    "janitor": """Extract important facts, preferences, and habits about the user from the following chat logs. Reply concisely in bullet points. Output ONLY in JSON format.

{inbox_content}""",

    "heartbeat": """You are Zoe, a personal AI companion. Based on the user's background data and memory, generate a short, sweet, and caring proactive greeting. Do not use any filler words or preambles.

[Data]
{partner_info}
{long_term_memory}""",

    "weather": """The user is asking about the weather. Here is the latest forecast data:
{data}

[Highest Directive]: Report this in a natural, voice-assistant style. Be concise. NEVER say things like 'I have digested this for you' or use any AI-like filler phrases!""",

    "politics": """The user is asking about world politics. Here is the latest news data:
{data}

[Highest Directive]: Summarize and report this in a natural conversational tone. Be concise. NEVER use any AI filler phrases!""",

    "world_news": """The user is asking about world news. Here is the latest news data:
{data}

[Highest Directive]: Summarize and report this in a natural conversational tone. Be concise. NEVER use any AI filler phrases!""",

    "local_news": """The user is asking about local news. Here is the latest news data:
{data}

[Highest Directive]: Summarize and report this in a natural conversational tone. Be concise. NEVER use any AI filler phrases!""",

    "bazi": """The user is asking a metaphysical question or requesting a Bazi (Four Pillars of Destiny) reading. Please answer based on the core logic of the provided knowledge base:
{data}

[Highest Directive]: Answer the user's question in a gentle, natural, and empathetic tone.
User's question: {user_message}"""
}
```
