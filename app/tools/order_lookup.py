from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.order import Order
from app.schemas.tool import ToolResult
from app.tools.base import BaseTool
from app.models.order_item import OrderItem

class OrderLookupTool(BaseTool):
    name = "order_lookup"

    description = (
        "Look up order status and order items by order code."
    )

    async def execute(
        self,
        db: AsyncSession,
        arguments: dict[str, Any],
    ) -> ToolResult:
        order_code = arguments.get("order_code")

        if not order_code:
            return ToolResult(
                success=False,
                tool_name=self.name,
                message="order_code is required",
                error_code="MISSING_ORDER_CODE",
            )

        statement = (
            select(Order)
            .options(
                selectinload(Order.customer),
                selectinload(Order.items).selectinload(
                    OrderItem.product
                ),
            )
            .where(
                Order.order_code == order_code.strip()
            )
        )

        result = await db.execute(statement)

        order = result.scalar_one_or_none()

        if order is None:
            return ToolResult(
                success=False,
                tool_name=self.name,
                message="Order not found",
                error_code="ORDER_NOT_FOUND",
            )

        items = []

        for item in order.items:
            items.append(
                {
                    "product_id": item.product_id,
                    "sku": item.product.sku,
                    "product_name": item.product.name,
                    "quantity": item.quantity,
                    "unit_price": str(item.unit_price),
                }
            )

        return ToolResult(
            success=True,
            tool_name=self.name,
            message="Order found",
            data={
                "id": order.id,
                "order_code": order.order_code,
                "status": order.status.value,
                "total_amount": str(order.total_amount),
                "shipping_address": order.shipping_address,
                "customer": {
                    "id": order.customer.id,
                    "customer_code": (
                        order.customer.customer_code
                    ),
                    "full_name": order.customer.full_name,
                    "email": order.customer.email,
                },
                "items": items,
                "created_at": order.created_at.isoformat(),
                "updated_at": order.updated_at.isoformat(),
            },
        )


order_lookup_tool = OrderLookupTool()