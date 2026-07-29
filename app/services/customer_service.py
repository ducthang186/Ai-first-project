from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.customer import Customer
from app.schemas.customer import CustomerCreate


class CustomerService:
    async def create_customer(
        self,
        db: AsyncSession,
        customer_data: CustomerCreate,
    ) -> Customer:
        customer = Customer(
            customer_code=customer_data.customer_code,
            full_name=customer_data.full_name,
            email=customer_data.email,
        )

        db.add(customer)

        await db.commit()
        await db.refresh(customer)

        return customer

    async def get_customers(
        self,
        db: AsyncSession,
    ) -> list[Customer]:
        statement = select(Customer).order_by(Customer.id)

        result = await db.execute(statement)

        return list(result.scalars().all())

    async def get_customer_by_id(
        self,
        db: AsyncSession,
        customer_id: int,
    ) -> Customer | None:
        statement = select(Customer).where(
            Customer.id == customer_id
        )

        result = await db.execute(statement)

        return result.scalar_one_or_none()


customer_service = CustomerService()