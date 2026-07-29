from fastapi import APIRouter

from app.api.routes.chat import router as chat_router
from app.api.routes.customers import router as customer_router
from app.api.routes.llm import router as llm_router
from app.api.routes.tools import router as tools_router


api_router = APIRouter()

api_router.include_router(chat_router)
api_router.include_router(customer_router)
api_router.include_router(tools_router)
api_router.include_router(llm_router)