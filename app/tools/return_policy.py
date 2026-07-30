from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.tool import ToolResult
from app.tools.base import BaseTool


class ReturnPolicyTool(BaseTool):
    name = "return_policy"

    description = (
        "Provide the store return and refund policy."
    )

    async def execute(
        self,
        db: AsyncSession,
        arguments: dict[str, Any],
    ) -> ToolResult:
        product_category = arguments.get(
            "product_category"
        )

        return ToolResult(
            success=True,
            tool_name=self.name,
            message="Return policy found",
            data={
                "return_window_days": 30,
                "requires_receipt": True,
                "requires_original_condition": True,
                "requires_original_packaging": True,
                "excluded_items": [
                    "personalized items",
                    "gift cards",
                    "opened hygiene products",
                ],
                "refund_processing_days": {
                    "minimum": 5,
                    "maximum": 10,
                },
                "product_category": product_category,
                "policy_version": "2026-01",
            },
        )


return_policy_tool = ReturnPolicyTool()