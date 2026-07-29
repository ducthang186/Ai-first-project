from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.tool import (
    ToolExecuteRequest,
    ToolResult,
)
from app.services.tool_service import tool_service


router = APIRouter(
    prefix="/tools",
    tags=["Tools"],
)


@router.get("")
async def get_tools() -> list[dict[str, str]]:
    return tool_service.get_available_tools()


@router.post(
    "/{tool_name}/execute",
    response_model=ToolResult,
)
async def execute_tool(
    tool_name: str,
    request: ToolExecuteRequest,
    db: AsyncSession = Depends(get_db),
) -> ToolResult:
    return await tool_service.execute_tool(
        db=db,
        tool_name=tool_name,
        arguments=request.arguments,
    )