import logging

from fastapi import FastAPI, UploadFile

from app.config import setup_logging
from app.routers import hello_world, rfp, chat, embeddings

setup_logging()

app = FastAPI()

app.include_router(
    hello_world.router, prefix="/hello-world", tags=["placeholder router"]
)
app.include_router(rfp.router, prefix="/rfp", tags=["rfp"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(embeddings.router, prefix="/embeddings", tags=["Embeddings"])


@app.get("/")
async def read_root():
    return {"Hello": "World!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)