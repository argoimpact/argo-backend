from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from app.dependencies import get_current_user
from app.models.user import User
from app.models.chat import ChatMessage, ChatHistory
from app.schemas.chat import ChatMessageCreate
from typing import List

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.websocket("/ws")
async def chat_websocket(
    websocket: WebSocket, current_user: User = Depends(get_current_user)
):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            message = ChatMessageCreate(**data)
            db_message = await ChatMessage.create(
                **message.dict(), user_id=current_user.id
            )
            await websocket.send_json(db_message.dict())
    except WebSocketDisconnect:
        pass


@router.get("/history", response_model=List[ChatMessage])
async def get_chat_history(current_user: User = Depends(get_current_user)):
    chat_history = await ChatHistory.get_history(user_id=current_user.id)
    return chat_history
