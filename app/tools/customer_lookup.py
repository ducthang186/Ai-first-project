from typing import Any

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.customer import Customer
from app.schemas.tool import ToolResult
from app.tools.base import BaseTool


class CustomerLookupTool(BaseTool):
    name = "customer_lookup"

    description = (
        "Look up a customer by customer code or email address."
    )

    async def execute(
        self,
        db: AsyncSession,
        arguments: dict[str, Any],
    ) -> ToolResult:
        customer_code = arguments.get("customer_code")
        email = arguments.get("email")

        if not customer_code and not email:
            return ToolResult(
                success=False,
                tool_name=self.name,
                message=(
                    "customer_code or email is required"
                ),
                error_code="MISSING_CUSTOMER_IDENTIFIER",
            )

        conditions = []

        if customer_code:
            conditions.append(
                Customer.customer_code == customer_code.strip()
            )

        if email:
            conditions.append(
                Customer.email == email.strip().lower()
            )

        statement = select(Customer).where(
            or_(*conditions)
        )

        result = await db.execute(statement)

        customer = result.scalar_one_or_none()

        if customer is None:
            return ToolResult(
                success=False,
                tool_name=self.name,
                message="Customer not found",
                error_code="CUSTOMER_NOT_FOUND",
            )

        return ToolResult(
            success=True,
            tool_name=self.name,
            message="Customer found",
            data={
                "id": customer.id,
                "customer_code": customer.customer_code,
                "full_name": customer.full_name,
                "email": customer.email,
                "created_at": customer.created_at.isoformat(),
            },
        )


customer_lookup_tool = CustomerLookupTool()