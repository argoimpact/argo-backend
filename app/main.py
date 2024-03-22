from fastapi import FastAPI, UploadFile
from dotenv import load_dotenv
from app.routers import hello_world, rfp

load_dotenv()

app = FastAPI()

app.include_router(
    hello_world.router, prefix="/hello-world", tags=["placeholder router"]
)
app.include_router(rfp.router, prefix="/rfp", tags=["rfp"])


@app.get("/")
async def read_root():
    return {"Hello": "World!"}
