from typing import Any


GROQ_TOOL_DEFINITIONS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "customer_lookup",
            "description": (
                "Look up a customer by exact customer code or email. "
                "Use this when verified customer information is needed."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_code": {
                        "type": "string",
                        "description": (
                            "Exact customer code, for example CUS-001."
                        ),
                    },
                    "email": {
                        "type": "string",
                        "description": (
                            "Exact customer email address."
                        ),
                    },
                },
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "order_lookup",
            "description": (
                "Look up an order's status, customer, total and items "
                "using an exact order code."
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
                "Check product information and stock quantity "
                "using an exact SKU."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "sku": {
                        "type": "string",
                        "description": (
                            "Exact product SKU, for example SKU-001."
                        ),
                    }
                },
                "required": ["sku"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "return_policy",
            "description": (
                "Retrieve the store's return and refund policy. "
                "Use this for questions about return windows, "
                "refund processing, receipts, exclusions or "
                "product-condition requirements."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "product_category": {
                        "type": "string",
                        "description": (
                            "Optional product category mentioned "
                            "by the customer."
                        ),
                    }
                },
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "human_escalation",
            "description": (
                "Create a support ticket for a human agent. "
                "Use only when the customer explicitly asks for "
                "human assistance or automated support is insufficient."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "integer",
                        "description": (
                            "Verified internal customer ID. "
                            "Do not invent this value."
                        ),
                    },
                    "order_id": {
                        "type": "integer",
                        "description": (
                            "Verified internal order ID. "
                            "Do not invent this value."
                        ),
                    },
                    "subject": {
                        "type": "string",
                        "description": (
                            "Short factual ticket subject."
                        ),
                    },
                    "description": {
                        "type": "string",
                        "description": (
                            "Factual description of the customer's issue."
                        ),
                    },
                    "priority": {
                        "type": "string",
                        "enum": [
                            "low",
                            "normal",
                            "high",
                            "urgent",
                        ],
                        "description": "Support-ticket priority.",
                    },
                },
                "required": [
                    "subject",
                    "description",
                    "priority",
                ],
                "additionalProperties": False,
            },
        },
    },
]