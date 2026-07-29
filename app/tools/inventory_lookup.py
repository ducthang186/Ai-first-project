from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product
from app.schemas.tool import ToolResult
from app.tools.base import BaseTool


class InventoryLookupTool(BaseTool):
    name = "inventory_lookup"

    description = (
        "Check product availability and stock quantity by SKU."
    )

    async def execute(
        self,
        db: AsyncSession,
        arguments: dict[str, Any],
    ) -> ToolResult:
        sku = arguments.get("sku")

        if not sku:
            return ToolResult(
                success=False,
                tool_name=self.name,
                message="sku is required",
                error_code="MISSING_SKU",
            )

        statement = select(Product).where(
            Product.sku == sku.strip()
        )

        result = await db.execute(statement)

        product = result.scalar_one_or_none()

        if product is None:
            return ToolResult(
                success=False,
                tool_name=self.name,
                message="Product not found",
                error_code="PRODUCT_NOT_FOUND",
            )

        is_available = (
            product.is_active
            and product.stock_quantity > 0
        )

        return ToolResult(
            success=True,
            tool_name=self.name,
            message="Inventory information found",
            data={
                "product_id": product.id,
                "sku": product.sku,
                "name": product.name,
                "price": str(product.price),
                "stock_quantity": product.stock_quantity,
                "is_active": product.is_active,
                "is_available": is_available,
            },
        )


inventory_lookup_tool = InventoryLookupTool()