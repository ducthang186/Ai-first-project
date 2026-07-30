from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AgentServiceError
from app.db.session import get_db
from app.schemas.agent import (
    AgentChatRequest,
    AgentChatResponse,
)
from app.services.agent_service import agent_service


router = APIRouter(
    prefix="/agent",
    tags=["AI Agent"],
)


@router.post(
    "/chat",
    response_model=AgentChatResponse,
)
async def chat_with_agent(
    request: AgentChatRequest,
    session: AsyncSession = Depends(get_db),
) -> AgentChatResponse:
    try:
        return await agent_service.run(
            message=request.message,
            session=session,
        )

    except AgentServiceError as error:
        raise HTTPException(
            status_code=error.status_code,
            detail={
                "message": error.message,
                "error_code": error.error_code,
            },
        ) from error