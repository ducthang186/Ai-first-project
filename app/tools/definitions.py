OPENAI_TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "order_lookup",
            "description": (
                "Look up an order's status, customer and "
                "items using an exact order code."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "order_code": {
                        "type": "string",
                        "description": (
                            "Exact order code, for example ORD-001."
                        ),
                    }
                },
                "required": ["order_code"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "inventory_lookup",
            "description": (
                "Check inventory using an exact product SKU."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "sku": {
                        "type": "string",
                        "description": (
                            "Exact SKU, for example SKU-001."
                        ),
                    }
                },
                "required": ["sku"],
                "additionalProperties": False,
            },
        },
    },
]