import uuid

from redis import Redis
from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_current_user
from app.exceptions import InvalidFileUploadException
from app.models.user import User
from app.models.rfp import RFP
from app.schemas.rfp import RFPCreate, RFPUpdate, RFPResponse
from app.config import REDIS_HOST

router = APIRouter(dependencies=[Depends(get_current_user)])
redis_client = Redis(host=REDIS_HOST, port=6379)


@router.post("/upload", response_model=RFP, status_code=status.HTTP_201_CREATED)
async def create_rfp(
    rfp: RFPCreate = Depends(), current_user: User = Depends(get_current_user)
):
    """Upload an RFP file to the server.
    Accepts pdf files

    * caches the file in Redis, based on a unique file_id

    Returns the RFP object with the file_id
    """
    if rfp.file.content_type != "application/pdf":
        raise InvalidFileUploadException(content_type=rfp.file.content_type)

    # Generate a unique identifier for the file
    file_id = str(uuid.uuid4())

    # Store the file data in Redis
    file_data = await rfp.file.read()
    redis_client.set(file_id, file_data, ex=3600)  # expire in 1 hour

    # maybe save the persistent rfp thing in there
    rfp_response = RFPResponse(
        file_id=file_id,
        user_id=current_user.id,
        description=rfp.description,
        title=rfp.title,
    )
    return rfp_response


@router.get("/{rfp_id}", response_model=RFP)
async def get_rfp(rfp_id: str, current_user: User = Depends(get_current_user)):
    # Logic to retrieve a specific RFP
    # Example:
    # db_rfp = await RFP.get(id=rfp_id, user_id=current_user.id)
    # if not db_rfp:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RFP not found")
    # return db_rfp
    pass


@router.put("/{rfp_id}", response_model=RFP)
async def update_rfp(
    rfp_id: str, rfp: RFPUpdate, current_user: User = Depends(get_current_user)
):
    # Logic to update an existing RFP
    # Example:
    # db_rfp = await RFP.get(id=rfp_id, user_id=current_user.id)
    # if not db_rfp:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RFP not found")
    # updated_rfp = await RFP.update(db_rfp, **rfp.dict())
    # return updated_rfp
    pass


@router.delete("/{rfp_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rfp(rfp_id: str, current_user: User = Depends(get_current_user)):
    # Logic to delete an RFP
    # Example:
    # db_rfp = await RFP.get(id=rfp_id, user_id=current_user.id)
    # if not db_rfp:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RFP not found")
    # await RFP.delete(db_rfp)
    pass
