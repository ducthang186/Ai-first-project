from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.tool import ToolResult


class BaseTool(ABC):
    name: str
    description: str

    @abstractmethod
    async def execute(
        self,
        db: AsyncSession,
        arguments: dict[str, Any],
    ) -> ToolResult:
        raise NotImplementedError