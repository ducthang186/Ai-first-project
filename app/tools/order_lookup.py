from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order
from app.schemas.tool import ToolResult
from app.tools.base import BaseTool


class OrderLookupTool(BaseTool):
    name = "order_lookup"

    async def execute(
        self,
        session: AsyncSession,
        order_code: str,
    ) -> ToolResult:
        normalized_order_code = order_code.strip().upper()

        order = await session.scalar(
            select(Order).where(
                Order.order_code == normalized_order_code
            )
        )

        if order is None:
            return ToolResult(
                success=False,
                tool_name=self.name,
                message="Order not found.",
                data={
                    "order_code": normalized_order_code,
                },
                error_code="ORDER_NOT_FOUND",
            )

        status = (
            order.status.value
            if hasattr(order.status, "value")
            else str(order.status)
        )

        return ToolResult(
            success=True,
            tool_name=self.name,
            message="Order found successfully.",
            data={
                "id": order.id,
                "order_code": order.order_code,
                "customer_id": order.customer_id,
                "status": status,
                "total_amount": str(order.total_amount),
                "shipping_address": order.shipping_address,
            },
            error_code=None,
        )

order_lookup_tool = OrderLookupTool()