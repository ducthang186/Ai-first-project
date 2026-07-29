from fastapi import APIRouter

from app.api.routes.chat import router as chat_router
from app.api.routes.customers import router as customer_router


api_router = APIRouter()

api_router.include_router(chat_router)
api_router.include_router(customer_router)