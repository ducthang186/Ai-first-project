from typing import Any, Literal

from pydantic import BaseModel, Field


class LLMRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=5000,
        examples=[
            "Xin chào, cửa hàng có hỗ trợ đổi trả không?"
        ],
    )


class LLMTextResponse(BaseModel):
    response_id: str
    type: Literal["message"] = "message"
    text: str
    model: str


class LLMToolCall(BaseModel):
    call_id: str
    tool_name: str
    arguments: dict[str, Any]


class LLMPlanningResponse(BaseModel):
    response_id: str
    type: Literal[
        "message",
        "tool_call",
        "multiple_tool_calls",
    ]
    text: str | None = None
    tool_calls: list[LLMToolCall] = Field(
        default_factory=list
    )
    model: str