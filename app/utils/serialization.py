import json
from typing import Any

from fastapi.encoders import jsonable_encoder


def to_json_string(value: Any) -> str:
    encoded = jsonable_encoder(value)

    return json.dumps(
        encoded,
        ensure_ascii=False,
        separators=(",", ":"),
    )