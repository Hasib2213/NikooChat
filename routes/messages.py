from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db, Conversation, Message, User
from models.schemas import MessageCreate, MessageResponse
from dependencies import get_current_user
from services.ai_services import get_ai_response
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/conversations", tags=["messages"])

@router.post("/{conv_id}/messages", response_model=MessageResponse)
def send_message(
    conv_id: int,
    msg: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a message in a conversation and get AI response"""
    try:
        # Verify conversation exists and belongs to current user
        conv = db.query(Conversation).filter(
            Conversation.id == conv_id,
            Conversation.user_id == current_user.id
        ).first()
        
        if not conv:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        # Validate message content
        if not msg.content or not msg.content.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Message content cannot be empty"
            )
        
        # Save user message
        user_msg = Message(
            conversation_id=conv_id,
            sender="user",
            content=msg.content.strip()
        )
        db.add(user_msg)
        db.commit()
        
        # Update conversation title if it's the first message
        if conv.title == "New Conversation":
            conv.title = msg.content[:50] + ("..." if len(msg.content) > 50 else "")
            db.commit()
        
        # Get conversation history and get AI response
        history = db.query(Message).filter(
            Message.conversation_id == conv_id
        ).order_by(Message.id).all()
        
        ai_reply = get_ai_response(history)
        
        # Save AI response
        ai_msg = Message(
            conversation_id=conv_id,
            sender="ai",
            content=ai_reply
        )
        db.add(ai_msg)
        db.commit()
        
        logger.info(f"Message exchanged in conversation {conv_id} by user {current_user.id}")
        return {"sender": "ai", "content": ai_reply}
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error sending message in conversation {conv_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process message"
        )

@router.get("/{conv_id}/messages")
def get_messages(
    conv_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all messages in a conversation"""
    try:
        # Verify conversation exists and belongs to current user
        conv = db.query(Conversation).filter(
            Conversation.id == conv_id,
            Conversation.user_id == current_user.id
        ).first()
        
        if not conv:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        msgs = db.query(Message).filter(
            Message.conversation_id == conv_id
        ).order_by(Message.id).all()
        
        logger.debug(f"Retrieved {len(msgs)} messages from conversation {conv_id}")
        return [
            {"sender": m.sender, "content": m.content, "id": m.id}
            for m in msgs
        ]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving messages from conversation {conv_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve messages"
        )