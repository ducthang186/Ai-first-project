from app.tools.registry import get_tool, list_tools


def test_list_tools() -> None:
    tools = list_tools()

    tool_names = {
        tool["name"]
        for tool in tools
    }

    assert "customer_lookup" in tool_names
    assert "order_lookup" in tool_names
    assert "inventory_lookup" in tool_names
    assert "return_policy" in tool_names
    assert "human_escalation" in tool_names


def test_get_existing_tool() -> None:
    tool = get_tool("order_lookup")

    assert tool is not None
    assert tool.name == "order_lookup"


def test_get_unknown_tool() -> None:
    tool = get_tool("unknown_tool")

    assert tool is None