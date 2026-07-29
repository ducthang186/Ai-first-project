from typing import Any

from pydantic import BaseModel, Field


class ToolResult(BaseModel):
    success: bool

    tool_name: str = Field(
        min_length=1,
        max_length=100,
    )

    message: str = Field(
        min_length=1,
        max_length=500,
    )

    data: dict[str, Any] | list[Any] | None = None

    error_code: str | None = None


class ToolExecuteRequest(BaseModel):
    arguments: dict[str, Any] = Field(
        default_factory=dict
    )