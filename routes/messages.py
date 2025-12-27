from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, Conversation, Message
from models.schemas import MessageCreate, MessageResponse
from dependencies import get_session_id
from services.ai_services import get_ai_response  # Groq

router = APIRouter(prefix="/conversations", tags=["messages"])

@router.post("/{conv_id}/messages", response_model=MessageResponse)
def send_message(conv_id: int, msg: MessageCreate, session_id: str = Depends(get_session_id), db: Session = Depends(get_db)):
    conv = db.query(Conversation).filter(Conversation.id == conv_id, Conversation.user_id == 1).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # ইউজার মেসেজ সেভ
    user_msg = Message(conversation_id=conv_id, sender="user", content=msg.content)
    db.add(user_msg)
    db.commit()

    # টাইটেল সেট (প্রথম মেসেজ হলে)
    if conv.title == "New Conversation":
        conv.title = msg.content[:50] + ("..." if len(msg.content) > 50 else "")
        db.commit()

    # হিস্ট্রি + Groq থেকে উত্তর
    history = db.query(Message).filter(Message.conversation_id == conv_id).order_by(Message.id).all()
    ai_reply = get_ai_response(history)

    # AI মেসেজ সেভ
    ai_msg = Message(conversation_id=conv_id, sender="ai", content=ai_reply)
    db.add(ai_msg)
    db.commit()

    return {"sender": "ai", "content": ai_reply}

@router.get("/{conv_id}/messages")
def get_messages(conv_id: int, session_id: str = Depends(get_session_id), db: Session = Depends(get_db)):
    conv = db.query(Conversation).filter(Conversation.id == conv_id, Conversation.user_id == 1).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    msgs = db.query(Message).filter(Message.conversation_id == conv_id).order_by(Message.id).all()
    return [{"sender": m.sender, "content": m.content} for m in msgs]