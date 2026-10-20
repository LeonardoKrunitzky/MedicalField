import json
import os
import uuid
from typing import Any
from pydantic import BaseModel


def _extract_ids(data: Any, includes_data: bool = False) -> Any:
    """
    Recursively traverses dictionaries and lists, keeping only
    keys that are 'id', end with '_id', or end with '_at' if includes_data is True.
    """
    if isinstance(data, dict):
        extracted = {}
        for key, value in data.items():
            is_valid = key != "professional_id" and (
                key == "id"
                or key.endswith("_id")
                or (includes_data and key.endswith("_at"))
            )
            if is_valid:
                extracted[key] = value
            elif isinstance(value, (dict, list)):
                nested = _extract_ids(value, includes_data)
                if nested:

                    extracted[key] = nested
        return extracted

    if isinstance(data, list):
        extracted_list = [_extract_ids(item, includes_data) for item in data]
        return [item for item in extracted_list if item]

    return None


def generate_uuid5(payload: BaseModel, includes_data: bool = False) -> uuid.UUID:
    """
    Generates a deterministic UUIDv5 using only ID fields ('id' and '*_id')
    present in the Pydantic payload (and optional extra_id for child tables),
    including '*_at' fields if includes_data is True.
    """
    if not isinstance(payload, BaseModel):
        raise TypeError(
            f"Expected payload to be a Pydantic BaseModel, got {type(payload).__name__}."
        )

    namespace_env = os.getenv("UUID_NAMESPACE")
    if not namespace_env:
        raise ValueError("Environment variable 'UUID_NAMESPACE' is not set.")

    try:
        namespace = uuid.UUID(namespace_env)
    except ValueError as err:
        raise ValueError(f"Invalid UUID in 'UUID_NAMESPACE': {namespace_env}") from err

    raw_data = (
        payload.model_dump(mode="json", exclude_none=True)
        if hasattr(payload, "model_dump")
        else json.loads(payload.json(exclude_none=True))
    )

    id_data = _extract_ids(raw_data, includes_data)

    if not id_data:
        id_data = raw_data

    serialized_payload = json.dumps(
        id_data,
        sort_keys=True,
        separators=(",", ":"),
    )

    return uuid.uuid5(namespace, serialized_payload)
