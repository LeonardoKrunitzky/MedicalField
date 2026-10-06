import os
import bcrypt


def _get_pepper() -> str:
    """
    Retrieve the application pepper from the environment variable.

    Returns:
        str: The pepper string configured in the environment.

    Raises:
        ValueError: If UUID_NAMESPACE is not set.
    """
    pepper = os.getenv("UUID_NAMESPACE")
    if not pepper:
        raise ValueError("Environment variable 'UUID_NAMESPACE' is not set.")
    return pepper


def hash_password(password: str) -> str:
    """
    Hash a plain-text password using bcrypt with an application pepper.

    Args:
        password (str): The raw password to hash.

    Returns:
        str: The resulting bcrypt hash string.
    """
    pepper = _get_pepper()
    payload = f"{password}{pepper}".encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(payload, salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain-text password against a stored bcrypt hash.

    Args:
        plain_password (str): The candidate raw password to verify.
        hashed_password (str): The stored bcrypt hash string.

    Returns:
        bool: True if the credentials match, False otherwise.
    """
    pepper = _get_pepper()
    payload = f"{plain_password}{pepper}".encode("utf-8")
    return bcrypt.checkpw(payload, hashed_password.encode("utf-8"))