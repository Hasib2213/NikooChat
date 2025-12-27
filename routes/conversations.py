from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, Conversation, Message
from models.schemas import ConversationList
from dependencies import get_session_id

router = APIRouter(prefix="/conversations", tags=["conversations"])

@router.post("/", response_model=int)
def create_conversation(session_id: str = Depends(get_session_id), db: Session = Depends(get_db)):
    conv = Conversation(
        user_id=1,
        title="New Conversation"  # এটা যোগ করো!
    )
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return conv.id

@router.get("/", response_model=ConversationList)
def list_conversations(session_id: str = Depends(get_session_id), db: Session = Depends(get_db)):
    convs = db.query(Conversation).filter(Conversation.user_id == 1).all()
    return {"conversations": [{"id": c.id, "title": c.title} for c in convs]}

@router.delete("/{conv_id}")
def delete_conversation(conv_id: int, session_id: str = Depends(get_session_id), db: Session = Depends(get_db)):
    conv = db.query(Conversation).filter(Conversation.id == conv_id, Conversation.user_id == 1).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    db.query(Message).filter(Message.conversation_id == conv_id).delete()
    db.delete(conv)
    db.commit()
    return {"msg": "Conversation deleted"}