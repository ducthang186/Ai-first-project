from typing import Any, Literal

from pydantic import BaseModel, Field


class AgentChatRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=5000,
        examples=[
            "Kiểm tra giúp tôi đơn hàng ORD-001."
        ],
    )


class AgentToolExecution(BaseModel):
    tool_name: str
    arguments: dict[str, Any]
    success: bool
    error_code: str | None = None


class AgentChatResponse(BaseModel):
    type: Literal["message"] = "message"

    message: str

    model: str

    iterations: int = Field(
        ge=1,
    )

    tools_used: list[AgentToolExecution] = Field(
        default_factory=list,
    )