import json
import os
import uuid
from typing import Any
from pydantic import BaseModel


def _extract_ids(data: Any) -> Any:
    """
    Percorre dicionários e listas recursivamente, mantendo apenas
    chaves que sejam 'id' ou terminem com '_id'.
    """
    if isinstance(data, dict):
        extracted = {}
        for key, value in data.items():
            if key == "id" or key.endswith("_id") or key.endswith("_at"):
                extracted[key] = value
            elif isinstance(value, (dict, list)):
                nested = _extract_ids(value)
                if nested:
                    extracted[key] = nested
        return extracted

    if isinstance(data, list):
        extracted_list = [_extract_ids(item) for item in data]
        return [item for item in extracted_list if item]

    return None


def generate_uuid5(
    payload: BaseModel, 
    extra_id: str | uuid.UUID | None = None
) -> uuid.UUID:
    """
    Gera um UUIDv5 determinístico utilizando apenas os campos de ID ('id' e '*_id')
    presentes no payload Pydantic (e um extra_id opcional para tabelas filhas).
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
        payload.model_dump(mode="json")
        if hasattr(payload, "model_dump")
        else json.loads(payload.json())
    )

    # Filtra apenas 'id' e '*_id' (incluindo os medication_id dentro de medications)
    id_data = _extract_ids(raw_data)

    # Fallback: se o DTO não tiver nenhum '_id' (ex: CreatePatientDTO que só tem name e document),
    # usa os dados normais do payload para não gerar o mesmo UUID para todos os pacientes
    if not id_data:
        id_data = raw_data

    # Se for uma entidade filha (ex: medicação de um atendimento), vincula ao ID pai
    if extra_id is not None:
        id_data["_parent_id"] = str(extra_id)

    serialized_payload = json.dumps(
        id_data,
        sort_keys=True,
        separators=(",", ":"),
    )

    return uuid.uuid5(namespace, serialized_payload)