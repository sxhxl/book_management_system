import ollama
from app.config import settings

async def generate_summary(content: str) -> str:
    if not content:
        return ""
    try:
        response = ollama.chat(
            model=settings.LLM_MODEL,
            messages=[{"role": "user", "content": f"Summarize this book: {content}"}]
        )
        return response['message']['content']
    except:
        return "Summary generation failed"
