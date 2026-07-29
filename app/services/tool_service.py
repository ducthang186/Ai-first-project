import logging
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.tool import ToolResult
from app.tools.registry import get_tool, list_tools


logger = logging.getLogger(__name__)


class ToolService:
    def get_available_tools(
        self,
    ) -> list[dict[str, str]]:
        return list_tools()

    async def execute_tool(
        self,
        db: AsyncSession,
        tool_name: str,
        arguments: dict[str, Any],
    ) -> ToolResult:
        tool = get_tool(tool_name)

        if tool is None:
            return ToolResult(
                success=False,
                tool_name=tool_name,
                message="Tool not found",
                data={
                    "available_tools": [
                        item["name"]
                        for item in list_tools()
                    ]
                },
                error_code="TOOL_NOT_FOUND",
            )

        logger.info(
            "Executing tool name=%s",
            tool_name,
        )

        try:
            result = await tool.execute(
                db=db,
                arguments=arguments,
            )

            logger.info(
                "Tool completed name=%s success=%s",
                tool_name,
                result.success,
            )

            return result

        except Exception:
            logger.exception(
                "Tool execution failed name=%s",
                tool_name,
            )

            return ToolResult(
                success=False,
                tool_name=tool_name,
                message=(
                    "An unexpected error occurred "
                    "while executing the tool"
                ),
                error_code="TOOL_EXECUTION_ERROR",
            )


tool_service = ToolService()