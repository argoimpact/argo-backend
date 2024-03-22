from fastapi import APIRouter

router = APIRouter()


@router.get("/hello-world")
async def hello_world():
    return {"message": "Hello World!"}
