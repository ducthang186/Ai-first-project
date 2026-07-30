from app.tools.base import BaseTool
from app.tools.customer_lookup import customer_lookup_tool
from app.tools.human_escalation import human_escalation_tool
from app.tools.inventory_lookup import inventory_lookup_tool
from app.tools.order_lookup import order_lookup_tool
from app.tools.return_policy import return_policy_tool


TOOLS: dict[str, BaseTool] = {
    customer_lookup_tool.name: customer_lookup_tool,
    order_lookup_tool.name: order_lookup_tool,
    inventory_lookup_tool.name: inventory_lookup_tool,
    return_policy_tool.name: return_policy_tool,
    human_escalation_tool.name: human_escalation_tool,
}


def get_tool(tool_name: str) -> BaseTool | None:
    return TOOLS.get(tool_name)


def list_tools() -> list[dict[str, str]]:
    return [
        {
            "name": tool.name,
            "description": tool.description,
        }
        for tool in TOOLS.values()
    ]