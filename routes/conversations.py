from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db, Conversation, Message, User
from models.schemas import ConversationList
from dependencies import get_current_user, get_current_user_id
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/conversations", tags=["conversations"])

@router.post("/", response_model=int)
def create_conversation(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new conversation for the authenticated user"""
    try:
        conv = Conversation(
            user_id=current_user.id,
            title="New Conversation"
        )
        db.add(conv)
        db.commit()
        db.refresh(conv)
        logger.info(f"Conversation created: {conv.id} for user: {current_user.id}")
        return conv.id
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating conversation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create conversation"
        )

@router.get("/", response_model=ConversationList)
def list_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all conversations for the authenticated user"""
    try:
        convs = db.query(Conversation).filter(
            Conversation.user_id == current_user.id
        ).all()
        
        conversations_with_count = []
        for c in convs:
            msg_count = db.query(Message).filter(
                Message.conversation_id == c.id
            ).count()
            conversations_with_count.append({
                "id": c.id, 
                "title": c.title,
                "message_count": msg_count
            })
        
        logger.debug(f"Retrieved {len(conversations_with_count)} conversations for user: {current_user.id}")
        return {"conversations": conversations_with_count}
    except Exception as e:
        logger.error(f"Error listing conversations: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve conversations"
        )

@router.delete("/{conv_id}")
def delete_conversation(
    conv_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a conversation (only if owned by current user)"""
    try:
        conv = db.query(Conversation).filter(
            Conversation.id == conv_id,
            Conversation.user_id == current_user.id
        ).first()
        
        if not conv:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        # Delete all messages in the conversation
        db.query(Message).filter(Message.conversation_id == conv_id).delete()
        db.delete(conv)
        db.commit()
        
        logger.info(f"Conversation deleted: {conv_id} by user: {current_user.id}")
        return {"msg": "Conversation deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting conversation {conv_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete conversation"
        )