import logging

from app.schemas.chat import ChatRequest, ChatResponse

logger = logging.getLogger(__name__)

class ChatService:
    def process_message(self, request: ChatRequest) -> ChatResponse:
        cleaned_message = request.message.strip()

        if not cleaned_message:
            logger.warning(
                "Empty message received from customer_id=%s",
                request.customer_id,
            )
            raise ValueError("Message cannot be empty")

        logger.info(
            "Processing message for customer_id=%s",
            request.customer_id,
        )

        reply = f"Tôi đã nhận được câu hỏi: {cleaned_message}"

        return ChatResponse(
            customer_id=request.customer_id,
            reply=reply,
        )


chat_service = ChatService()