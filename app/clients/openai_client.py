from openai import AsyncOpenAI

from app.core.config import settings


openai_client = AsyncOpenAI(
    api_key=settings.openai_api_key,
    timeout=settings.openai_timeout_seconds,
    max_retries=2,
)