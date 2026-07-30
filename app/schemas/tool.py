from typing import Any

from pydantic import BaseModel, Field


class ToolResult(BaseModel):
    success: bool
    tool_name: str
    message: str
    data: Any | None = None
    error_code: str | None = None


class ToolExecuteRequest(BaseModel):
    arguments: dict[str, Any] = Field(
        default_factory=dict
    )