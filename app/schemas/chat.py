from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    customer_id: str = Field(
        ...,
        min_length=1,
        max_length=100,
        examples=["cus_001"],
    )

    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        examples=["Đơn hàng của tôi đang ở đâu?"],
    )
class ChatResponse(BaseModel):
    customer_id: str
    reply: str