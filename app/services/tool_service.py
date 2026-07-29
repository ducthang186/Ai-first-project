import logging
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.tool import ToolResult
from app.tools.registry import get_tool


logger = logging.getLogger(__name__)


class ToolService:
    async def execute(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        session: AsyncSession,
    ) -> ToolResult:
        tool = get_tool(tool_name)

        if tool is None:
            return ToolResult(
                success=False,
                tool_name=tool_name,
                message="The requested tool does not exist.",
                data=None,
                error_code="TOOL_NOT_FOUND",
            )

        try:
            return await tool.execute(
                session=session,
                **arguments,
            )

        except TypeError as error:
            logger.exception(
                "Invalid tool arguments tool_name=%s",
                tool_name,
            )

            return ToolResult(
                success=False,
                tool_name=tool_name,
                message=str(error),
                data={
                    "received_arguments": list(arguments.keys()),
                },
                error_code="INVALID_TOOL_ARGUMENTS",
            )

        except Exception:
            logger.exception(
                "Tool execution failed tool_name=%s",
                tool_name,
            )

            await session.rollback()

            return ToolResult(
                success=False,
                tool_name=tool_name,
                message="Tool execution failed.",
                data=None,
                error_code="TOOL_EXECUTION_ERROR",
            )


tool_service = ToolService()