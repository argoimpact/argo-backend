from fastapi import FastAPI, UploadFile
from dotenv import load_dotenv
from app.routers import hello_world

load_dotenv()

app = FastAPI()

app.include_router(
    hello_world.router, prefix="/hello-world", tags=["placeholder router"]
)


@app.get("/")
async def read_root():
    return {"Hello": "World!"}
