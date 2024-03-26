from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

import httpx

import redis

from app.utils.security import verify_token
from app.utils.openai import openai_client
from app.utils.pinecone import pinecone_client
from app.config import app_config
from app.models.user import User

bearer_scheme = HTTPBearer()

redis_client = redis.Redis(host=app_config.redis_host, port=6379)


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
                f"{app_config.clerk_api_endpoint}/{user_id}",
                headers={"Authorization": f"Bearer {app_config.clerk_secret_key}"},
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


def get_openai_client():
    return openai_client


def get_pinecone_client():
    return pinecone_client
