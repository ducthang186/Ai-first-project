import json
import logging
from typing import Any

from openai import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    RateLimitError,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.groq_client import groq_client
from app.core.config import settings
from app.core.exceptions import AgentServiceError
from app.prompts.support import SUPPORT_SYSTEM_INSTRUCTIONS
from app.schemas.agent import (
    AgentChatResponse,
    AgentToolExecution,
)
from app.services.tool_service import tool_service
from app.tools.definitions import GROQ_TOOL_DEFINITIONS
from app.utils.serialization import to_json_string


logger = logging.getLogger(__name__)


class AgentService:
    MAX_ITERATIONS = 5

    async def run(
        self,
        message: str,
        session: AsyncSession,
    ) -> AgentChatResponse:
        messages: list[dict[str, Any]] = [
            {
                "role": "system",
                "content": SUPPORT_SYSTEM_INSTRUCTIONS,
            },
            {
                "role": "user",
                "content": message,
            },
        ]

        tool_executions: list[AgentToolExecution] = []

        executed_call_signatures: set[str] = set()

        for iteration in range(
            1,
            self.MAX_ITERATIONS + 1,
        ):
            completion = await self._create_completion(
                messages=messages,
            )

            if not completion.choices:
                raise AgentServiceError(
                    message=(
                        "The AI service returned no response choices."
                    ),
                    error_code="AGENT_EMPTY_RESPONSE",
                    status_code=502,
                )

            assistant_message = (
                completion.choices[0].message
            )

            raw_tool_calls = (
                assistant_message.tool_calls or []
            )

            if not raw_tool_calls:
                final_text = (
                    assistant_message.content or ""
                ).strip()

                if not final_text:
                    raise AgentServiceError(
                        message=(
                            "The AI agent returned an empty response."
                        ),
                        error_code="AGENT_EMPTY_MESSAGE",
                        status_code=502,
                    )

                logger.info(
                    "Agent completed iterations=%s tools_used=%s",
                    iteration,
                    len(tool_executions),
                )

                return AgentChatResponse(
                    message=final_text,
                    model=completion.model,
                    iterations=iteration,
                    tools_used=tool_executions,
                )

            messages.append(
                {
                    "role": "assistant",
                    "content": assistant_message.content,
                    "tool_calls": [
                        tool_call.model_dump(
                            exclude_none=True
                        )
                        for tool_call in raw_tool_calls
                    ],
                }
            )

            for tool_call in raw_tool_calls:
                tool_name = tool_call.function.name

                arguments = self._parse_arguments(
                    raw_arguments=(
                        tool_call.function.arguments
                    ),
                    tool_name=tool_name,
                )

                call_signature = (
                    self._build_call_signature(
                        tool_name=tool_name,
                        arguments=arguments,
                    )
                )

                if (
                    call_signature
                    in executed_call_signatures
                ):
                    tool_result = {
                        "success": False,
                        "tool_name": tool_name,
                        "message": (
                            "This exact tool call was already "
                            "executed during the current request."
                        ),
                        "data": None,
                        "error_code": (
                            "DUPLICATE_TOOL_CALL"
                        ),
                    }

                    success = False
                    error_code = "DUPLICATE_TOOL_CALL"

                else:
                    executed_call_signatures.add(
                        call_signature
                    )

                    result = await tool_service.execute(
                        tool_name=tool_name,
                        arguments=arguments,
                        session=session,
                    )

                    tool_result = result.model_dump(
                        mode="json"
                    )

                    success = result.success
                    error_code = result.error_code

                tool_executions.append(
                    AgentToolExecution(
                        tool_name=tool_name,
                        arguments=arguments,
                        success=success,
                        error_code=error_code,
                    )
                )

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_name,
                        "content": to_json_string(
                            tool_result
                        ),
                    }
                )

        raise AgentServiceError(
            message=(
                "The AI agent exceeded the maximum "
                "number of tool-calling iterations."
            ),
            error_code="AGENT_MAX_ITERATIONS_EXCEEDED",
            status_code=500,
        )

    async def _create_completion(
        self,
        messages: list[dict[str, Any]],
    ) -> Any:
        try:
            return await (
                groq_client.chat.completions.create(
                    model=settings.groq_model,
                    messages=messages,
                    tools=GROQ_TOOL_DEFINITIONS,
                    tool_choice="auto",
                    temperature=0.1,
                    max_tokens=(
                        settings.llm_max_output_tokens
                    ),
                )
            )

        except Exception as error:
            self._raise_provider_error(error)

    def _parse_arguments(
        self,
        raw_arguments: str,
        tool_name: str,
    ) -> dict[str, Any]:
        try:
            parsed = json.loads(raw_arguments)

        except json.JSONDecodeError as error:
            logger.warning(
                "Invalid tool JSON tool_name=%s",
                tool_name,
            )

            raise AgentServiceError(
                message=(
                    "The AI generated invalid tool arguments."
                ),
                error_code="AGENT_INVALID_TOOL_JSON",
                status_code=502,
            ) from error

        if not isinstance(parsed, dict):
            raise AgentServiceError(
                message=(
                    "The AI generated tool arguments "
                    "in an invalid format."
                ),
                error_code="AGENT_INVALID_TOOL_ARGUMENTS",
                status_code=502,
            )

        return parsed

    def _build_call_signature(
        self,
        tool_name: str,
        arguments: dict[str, Any],
    ) -> str:
        normalized_arguments = json.dumps(
            arguments,
            sort_keys=True,
            ensure_ascii=False,
            default=str,
        )

        return (
            f"{tool_name}:{normalized_arguments}"
        )

    def _raise_provider_error(
        self,
        error: Exception,
    ) -> None:
        logger.error(
            "Groq agent request failed type=%s error=%s",
            type(error).__name__,
            str(error),
        )

        if isinstance(error, APITimeoutError):
            raise AgentServiceError(
                message="The AI service timed out.",
                error_code="LLM_TIMEOUT",
                status_code=504,
            ) from error

        if isinstance(error, AuthenticationError):
            raise AgentServiceError(
                message="The Groq API key is invalid.",
                error_code="LLM_AUTHENTICATION_ERROR",
                status_code=502,
            ) from error

        if isinstance(error, RateLimitError):
            raise AgentServiceError(
                message=(
                    "The AI service rate limit was reached."
                ),
                error_code="LLM_RATE_LIMITED",
                status_code=429,
            ) from error

        if isinstance(error, BadRequestError):
            raise AgentServiceError(
                message=(
                    "The AI service rejected the agent request."
                ),
                error_code="LLM_BAD_REQUEST",
                status_code=400,
            ) from error

        if isinstance(error, APIConnectionError):
            raise AgentServiceError(
                message=(
                    "Could not connect to the AI service."
                ),
                error_code="LLM_CONNECTION_ERROR",
                status_code=503,
            ) from error

        if isinstance(error, APIStatusError):
            raise AgentServiceError(
                message=(
                    "The AI provider returned an API error."
                ),
                error_code="LLM_API_ERROR",
                status_code=502,
            ) from error

        raise AgentServiceError(
            message=(
                "An unexpected AI agent error occurred."
            ),
            error_code="AGENT_UNEXPECTED_ERROR",
            status_code=500,
        ) from error


agent_service = AgentService()