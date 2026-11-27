"""Optional OpenAI-compatible chat completions integration (standard library)."""
import json
import os
from urllib.request import Request, urlopen


def rewrite_with_llm(question, approved_answer):
    key = os.getenv("LLM_API_KEY")
    model = os.getenv("LLM_MODEL")
    base = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    if not key or not model:
        raise RuntimeError("Set LLM_API_KEY and LLM_MODEL to enable LLM mode.")
    if not base.startswith("https://"):
        raise ValueError("LLM_BASE_URL must use HTTPS.")
    payload = {
        "model": model,
        "temperature": 0,
        "messages": [
            {"role": "system", "content": (
                "You are a customer support writing assistant for a fictional company. "
                "Use ONLY the supplied approved answer. Do not add facts, advice, or links. "
                "Never provide medical guidance. If the answer is insufficient, say so."
            )},
            {"role": "user", "content": (
                f"Customer question: {question}\\n"
                f"Approved answer: {approved_answer}\\n"
                "Rewrite the approved answer clearly and briefly."
            )},
        ],
    }
    request = Request(
        base + "/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=25) as response:
        result = json.load(response)
    return result["choices"][0]["message"]["content"]
