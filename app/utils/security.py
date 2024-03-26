from jose import JWTError, jwt

from app.exceptions import CredentialsException
from app.config import app_config


def verify_token(token: str) -> str:
    credentials_exception = CredentialsException("trying to get current user")
    try:
        payload = jwt.decode(
            token.credentials,
            app_config.clerk_secret_key,
            algorithms=[app_config.jwt_algorithm],
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return user_id
