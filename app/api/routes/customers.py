from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.customer import (
    CustomerCreate,
    CustomerResponse,
)
from app.services.customer_service import customer_service


router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


@router.post(
    "",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_customer(
    customer_data: CustomerCreate,
    db: AsyncSession = Depends(get_db),
) -> CustomerResponse:
    try:
        return await customer_service.create_customer(
            db=db,
            customer_data=customer_data,
        )
    except IntegrityError as error:
        await db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Customer code or email already exists",
        ) from error


@router.get(
    "",
    response_model=list[CustomerResponse],
)
async def get_customers(
    db: AsyncSession = Depends(get_db),
) -> list[CustomerResponse]:
    return await customer_service.get_customers(db)


@router.get(
    "/{customer_id}",
    response_model=CustomerResponse,
)
async def get_customer(
    customer_id: int,
    db: AsyncSession = Depends(get_db),
) -> CustomerResponse:
    customer = await customer_service.get_customer_by_id(
        db=db,
        customer_id=customer_id,
    )

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    return customer