import json
import logging
import uuid
from typing import Any, NoReturn

from openai import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    RateLimitError,
)

from app.clients.groq_client import groq_client
from app.core.config import settings
from app.core.exceptions import LLMServiceError
from app.prompts.support import SUPPORT_SYSTEM_INSTRUCTIONS
from app.schemas.llm import (
    LLMPlanningResponse,
    LLMTextResponse,
    LLMToolCall,
)
from app.tools.definitions import OPENAI_TOOL_DEFINITIONS


logger = logging.getLogger(__name__)


class LLMService:
    async def generate_text(
        self,
        message: str,
    ) -> LLMTextResponse:
        try:
            response = await groq_client.chat.completions.create(
                model=settings.groq_model,
                messages=[
                    {
                        "role": "system",
                        "content": SUPPORT_SYSTEM_INSTRUCTIONS,
                    },
                    {
                        "role": "user",
                        "content": message,
                    },
                ],
                temperature=0.3,
                max_tokens=settings.llm_max_output_tokens,
            )

        except Exception as error:
            self._raise_service_error(error)

        text = (
            response.choices[0].message.content or ""
        ).strip()

        if not text:
            text = (
                "Tôi chưa thể tạo câu trả lời. "
                "Vui lòng thử lại."
            )

        return LLMTextResponse(
            response_id=response.id,
            text=text,
            model=response.model,
        )

    async def plan_with_tools(
        self,
        message: str,
    ) -> LLMPlanningResponse:
        try:
            response = await groq_client.chat.completions.create(
                model=settings.groq_model,
                messages=[
                    {
                        "role": "system",
                        "content": SUPPORT_SYSTEM_INSTRUCTIONS,
                    },
                    {
                        "role": "user",
                        "content": message,
                    },
                ],
                tools=OPENAI_TOOL_DEFINITIONS,
                tool_choice="auto",
                temperature=0.1,
                max_tokens=settings.llm_max_output_tokens,
            )

        except Exception as error:
            self._raise_service_error(error)

        assistant_message = response.choices[0].message
        raw_tool_calls = assistant_message.tool_calls or []

        tool_calls: list[LLMToolCall] = []

        for tool_call in raw_tool_calls:
            try:
                arguments: dict[str, Any] = json.loads(
                    tool_call.function.arguments
                )
            except json.JSONDecodeError:
                arguments = {}

            tool_calls.append(
                LLMToolCall(
                    call_id=(
                        tool_call.id
                        or str(uuid.uuid4())
                    ),
                    tool_name=tool_call.function.name,
                    arguments=arguments,
                )
            )

        if len(tool_calls) == 1:
            response_type = "tool_call"
        elif len(tool_calls) > 1:
            response_type = "multiple_tool_calls"
        else:
            response_type = "message"

        return LLMPlanningResponse(
            response_id=response.id,
            type=response_type,
            text=assistant_message.content or None,
            tool_calls=tool_calls,
            model=response.model,
        )

    def _raise_service_error(
        self,
        error: Exception,
    ) -> NoReturn:
        logger.error(
            "Groq request failed type=%s error=%s",
            type(error).__name__,
            str(error),
        )

        if isinstance(error, APITimeoutError):
            raise LLMServiceError(
                message="The AI service timed out.",
                error_code="LLM_TIMEOUT",
                status_code=504,
            ) from error

        if isinstance(error, AuthenticationError):
            raise LLMServiceError(
                message="The Groq API key is invalid.",
                error_code="LLM_AUTHENTICATION_ERROR",
                status_code=502,
            ) from error

        if isinstance(error, RateLimitError):
            raise LLMServiceError(
                message=(
                    "The Groq rate limit was reached. "
                    "Please retry later."
                ),
                error_code="LLM_RATE_LIMITED",
                status_code=429,
            ) from error

        if isinstance(error, BadRequestError):
            raise LLMServiceError(
                message=(
                    "Groq rejected the request. "
                    "Check the model and tool schema."
                ),
                error_code="LLM_BAD_REQUEST",
                status_code=400,
            ) from error

        if isinstance(error, APIConnectionError):
            raise LLMServiceError(
                message="Could not connect to Groq.",
                error_code="LLM_CONNECTION_ERROR",
                status_code=503,
            ) from error

        if isinstance(error, APIStatusError):
            raise LLMServiceError(
                message="Groq returned an API error.",
                error_code="LLM_API_ERROR",
                status_code=502,
            ) from error

        raise LLMServiceError(
            message="An unexpected AI service error occurred.",
            error_code="LLM_UNEXPECTED_ERROR",
            status_code=500,
        ) from error


llm_service = LLMService()