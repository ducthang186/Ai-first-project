from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CustomerCreate(BaseModel):
    customer_code: str = Field(
        min_length=1,
        max_length=50,
    )

    full_name: str = Field(
        min_length=1,
        max_length=255,
    )

    email: EmailStr


class CustomerResponse(BaseModel):
    id: int
    customer_code: str
    full_name: str
    email: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )