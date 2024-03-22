from dotenv import load_dotenv
from jose import JWTError, jwt
import os

from app.exceptions import CredentialsException

load_dotenv()

CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", default="HS256")


def verify_token(token: str) -> str:
    credentials_exception = CredentialsException("trying to get current user")
    try:
        payload = jwt.decode(
            token.credentials, CLERK_SECRET_KEY, algorithms=[ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return user_id
