from fastapi import APIRouter, HTTPException

from app.schemas.llm import (
    LLMPlanningResponse,
    LLMRequest,
    LLMTextResponse,
)
from app.core.exceptions import LLMServiceError
from app.services.llm_service import llm_service


router = APIRouter(
    prefix="/llm",
    tags=["LLM"],
)


@router.post(
    "/respond",
    response_model=LLMTextResponse,
)
async def generate_response(
    request: LLMRequest,
) -> LLMTextResponse:
    try:
        return await llm_service.generate_text(
            message=request.message,
        )

    except LLMServiceError as error:
        raise HTTPException(
            status_code=error.status_code,
            detail={
                "message": error.message,
                "error_code": error.error_code,
            },
        ) from error


@router.post(
    "/plan",
    response_model=LLMPlanningResponse,
)
async def plan_response(
    request: LLMRequest,
) -> LLMPlanningResponse:
    try:
        return await llm_service.plan_with_tools(
            message=request.message,
        )

    except LLMServiceError as error:
        raise HTTPException(
            status_code=error.status_code,
            detail={
                "message": error.message,
                "error_code": error.error_code,
            },
        ) from error