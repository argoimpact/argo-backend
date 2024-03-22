from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import JWTError, jwt

import httpx

import redis

from utils.security import ALGORITHM, CLERK_SECRET_KEY, CLERK_API_KEY, verify_token
from config import CLERK_API_ENDPOINT, REDIS_HOST
from models.user import User

bearer_scheme = HTTPBearer()

redis_client = redis.Redis(host=REDIS_HOST, port=6379)


async def get_current_user(token: str = Depends(bearer_scheme)):
    user_id = verify_token(token)

    # Returned cached user if available
    user_data = redis_client.get(user_id)
    if user_data:
        user = User(**user_data)
        return user

    # Fetch user data from Clerk API
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{CLERK_API_ENDPOINT}/{user_id}",
                headers={"Authorization": f"Bearer {CLERK_API_KEY}"},
            )
            response.raise_for_status()
            user_data = response.json()
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving user data from Clerk API: {str(e)}",
        )

    user = User(id=user_data["id"], email=user_data["email"])
    redis_client.set(user.id, user.dict())

    return user
