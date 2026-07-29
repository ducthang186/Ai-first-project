from openai import AsyncOpenAI

from app.core.config import settings


groq_client = AsyncOpenAI(
    api_key=settings.groq_api_key,
    base_url=settings.groq_base_url,
    timeout=settings.llm_timeout_seconds,
    max_retries=2,
)