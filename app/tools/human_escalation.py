from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.support_ticket import (
    SupportTicket,
    TicketPriority,
)
from app.schemas.tool import ToolResult
from app.tools.base import BaseTool


class HumanEscalationTool(BaseTool):
    name = "human_escalation"

    description = (
        "Create a support ticket when the issue requires "
        "a human support agent."
    )

    async def execute(
        self,
        db: AsyncSession,
        arguments: dict[str, Any],
    ) -> ToolResult:
        subject = arguments.get("subject")
        description = arguments.get("description")

        customer_id = arguments.get("customer_id")
        order_id = arguments.get("order_id")

        priority_value = arguments.get(
            "priority",
            TicketPriority.NORMAL.value,
        )

        if not subject:
            return ToolResult(
                success=False,
                tool_name=self.name,
                message="subject is required",
                error_code="MISSING_SUBJECT",
            )

        if not description:
            return ToolResult(
                success=False,
                tool_name=self.name,
                message="description is required",
                error_code="MISSING_DESCRIPTION",
            )

        try:
            priority = TicketPriority(priority_value)
        except ValueError:
            return ToolResult(
                success=False,
                tool_name=self.name,
                message="Invalid ticket priority",
                data={
                    "allowed_priorities": [
                        item.value
                        for item in TicketPriority
                    ]
                },
                error_code="INVALID_PRIORITY",
            )

        ticket = SupportTicket(
            customer_id=customer_id,
            order_id=order_id,
            subject=subject.strip(),
            description=description.strip(),
            priority=priority,
        )

        db.add(ticket)

        try:
            await db.commit()
            await db.refresh(ticket)
        except Exception:
            await db.rollback()
            raise

        return ToolResult(
            success=True,
            tool_name=self.name,
            message="Support ticket created",
            data={
                "ticket_id": ticket.id,
                "status": ticket.status.value,
                "priority": ticket.priority.value,
                "subject": ticket.subject,
                "created_at": ticket.created_at.isoformat(),
            },
        )


human_escalation_tool = HumanEscalationTool()