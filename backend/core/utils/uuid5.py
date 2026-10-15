import json
import os
import uuid
from pydantic import BaseModel


def generate_uuid5_from_payload(payload: BaseModel) -> uuid.UUID:
    """
    Generate a deterministic UUIDv5 from a Pydantic model payload.

    Extracts the namespace from the UUID_NAMESPACE environment variable,
    validates that the payload is an instance of BaseModel, and serializes
    the model data deterministically.

    Args:
        payload (BaseModel): The Pydantic model instance to serialize.

    Returns:
        uuid.UUID: The deterministic version 5 UUID.

    Raises:
        TypeError: If the payload is not an instance of Pydantic BaseModel.
        ValueError: If UUID_NAMESPACE is missing or invalid.
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

    data = (
        payload.model_dump(mode="json")
        if hasattr(payload, "model_dump")
        else json.loads(payload.json())
    )

    serialized_payload = json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":"),
    )
    return uuid.uuid5(namespace, serialized_payload)