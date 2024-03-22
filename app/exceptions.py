from fastapi import HTTPException, status


class CredentialsException(HTTPException):
    def __init__(self, detail: str):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = f"Could not validate credentials: {detail}"
        self.headers = {"WWW-Authenticate": "Bearer"}
