import os
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> dict:
    """
    Validates the provided Access Token from the request using python-jose.

    Args:
        credentials (HTTPAuthorizationCredentials): The credentials containing the JWT token.

    Returns:
        dict: The decoded payload from the token.

    Raises:
        HTTPException: If the token is expired or invalid.
    """
    token = str(credentials.credentials)
    secret_key = os.getenv("JWT_SECRET_KEY", "")

    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado. Faça login novamente.")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido.")