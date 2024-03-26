import logging

from fastapi import FastAPI, UploadFile

from app.config import setup_logging
from app.routers import hello_world, rfp, chat

setup_logging()

app = FastAPI()

app.include_router(
    hello_world.router, prefix="/hello-world", tags=["placeholder router"]
)
app.include_router(rfp.router, prefix="/rfp", tags=["rfp"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])


@app.get("/")
async def read_root():
    return {"Hello": "World!"}
