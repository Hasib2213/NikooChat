import streamlit as st
import requests
import json
from datetime import datetime

# Configuration
API_BASE_URL = "http://localhost:8000"
SESSION_ID = "streamlit-session"

st.set_page_config(
    page_title="Nikoo Chatbot",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .chat-message {
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 0.5rem;
        display: flex;
        gap: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
        justify-content: flex-end;
    }
    .ai-message {
        background-color: #f5f5f5;
        justify-content: flex-start;
    }
    .message-content {
        max-width: 70%;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
    }
    .user-content {
        background-color: #2196F3;
        color: white;
    }
    .ai-content {
        background-color: white;
        border: 1px solid #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True)

def get_headers():
    """Get headers with session ID"""
    return {
        "Content-Type": "application/json",
        "X-Session-ID": SESSION_ID
    }

def fetch_conversations():
    """Fetch all conversations"""
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/conversations/",
            headers=get_headers()
        )
        if response.status_code == 200:
            return response.json().get("conversations", [])
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching conversations: {str(e)}")
    return []

def create_conversation():
    """Create a new conversation"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/conversations/",
            headers=get_headers()
        )
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error creating conversation: {str(e)}")
    return None

def delete_conversation(conv_id):
    """Delete a conversation"""
    try:
        response = requests.delete(
            f"{API_BASE_URL}/api/conversations/{conv_id}",
            headers=get_headers()
        )
        if response.status_code == 200:
            return True
    except requests.exceptions.RequestException as e:
        st.error(f"Error deleting conversation: {str(e)}")
    return False

def fetch_messages(conv_id):
    """Fetch messages for a conversation"""
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/conversations/{conv_id}/messages",
            headers=get_headers()
        )
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching messages: {str(e)}")
    return []

def send_message(conv_id, message_content):
    """Send a message and get AI response"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/conversations/{conv_id}/messages",
            json={"content": message_content},
            headers=get_headers()
        )
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error sending message: {str(e)}")
    return None

def display_messages(messages):
    """Display messages in chat format"""
    for msg in messages:
        if msg.get("sender") == "user":
            st.markdown(f"""
                <div class="chat-message user-message">
                    <div class="message-content user-content">
                        {msg.get("content", "")}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="chat-message ai-message">
                    <div class="message-content ai-content">
                        {msg.get("content", "")}
                    </div>
                </div>
                """, unsafe_allow_html=True)

# Initialize session state
if "current_conversation" not in st.session_state:
    st.session_state.current_conversation = None
if "conversations_list" not in st.session_state:
    st.session_state.conversations_list = []

# Sidebar
with st.sidebar:
    st.title("📚 Conversations")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("➕ New Conversation", use_container_width=True):
            new_conv_id = create_conversation()
            if new_conv_id:
                st.session_state.current_conversation = new_conv_id
                st.rerun()
    
    st.divider()
    
    # Refresh conversations
    st.session_state.conversations_list = fetch_conversations()
    
    if st.session_state.conversations_list:
        for conv in st.session_state.conversations_list:
            col1, col2, col3 = st.columns([4, 0.5, 1])
            with col1:
                msg_count = conv.get("message_count", 0)
                if st.button(
                    f"💬 {conv['title'][:25]}... ({msg_count})",
                    key=f"conv_{conv['id']}",
                    use_container_width=True
                ):
                    st.session_state.current_conversation = conv["id"]
                    st.rerun()
            with col2:
                st.caption(f"📊 {msg_count}")
            with col3:
                if st.button(
                    "🗑️",
                    key=f"del_{conv['id']}",
                    help="Delete conversation"
                ):
                    if delete_conversation(conv["id"]):
                        if st.session_state.current_conversation == conv["id"]:
                            st.session_state.current_conversation = None
                        st.rerun()
    else:
        st.info("No conversations yet. Start a new one!")

# Main chat area
st.title("💬AI Chatbot")

if st.session_state.current_conversation is None:
    st.info("👈 Select a conversation from the sidebar or create a new one to start chatting!")
else:
    conv_id = st.session_state.current_conversation
    
    # Get current conversation title
    current_conv = next(
        (c for c in st.session_state.conversations_list if c["id"] == conv_id),
        None
    )
    
    if current_conv:
        st.subheader(f"📝 {current_conv['title']}")
    
    # Display messages
    messages = fetch_messages(conv_id)
    if messages:
        display_messages(messages)
    else:
        # Show initial greeting when conversation is empty
        st.markdown(f"""
            <div class="chat-message ai-message">
                <div class="message-content ai-content">
                    Hello! Welcome to your app. I'm here to help you. Get started. What's your name?
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Input area
    st.divider()
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_input(
            "Your message:",
            placeholder="Type your message here...",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.button("Send", use_container_width=True, type="primary")
    
    if send_button and user_input.strip():
        # Show loading state
        with st.spinner("Thinking..."):
            response = send_message(conv_id, user_input)
        
        if response:
            st.rerun()
        else:
            st.error("Failed to send message. Please try again.")
