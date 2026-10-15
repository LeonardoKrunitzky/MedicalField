import os
from datetime import datetime, timedelta, timezone
from jose import jwt
from dotenv import load_dotenv

load_dotenv()

def create_access_token(data: dict) -> str:
    """
    Generates a JSON Web Token (JWT) for user login using python-jose.

    Args:
        data (dict): A dictionary containing the payload information.

    Returns:
        str: The encoded JWT as a string.
    """
    to_encode = data.copy()

    # Busca as variáveis de ambiente e converte os minutos para inteiro
    expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))
    secret_key = os.getenv("JWT_SECRET_KEY", "")

    expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm="HS256")

    return encoded_jwt