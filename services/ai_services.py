from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# APP-SPECIFIC PROMPT - আপনার অ্যাপের তথ্য এখানে যোগ করুন
APP_INFO = """
Our app is a Mobile App Support Chatbot that helps users.

App features:
- AI-powered issue resolution
- 24/7 availability
- Multi-language support

For contact: nikoo@app.com
"""

SYSTEM_PROMPT = f"""You are a friendly and helpful AI assistant that only answers questions related to this app.

{APP_INFO}

Rules:
1. All time follow:respond in the language the user is using.
2. If the question is not related to the app, reply: "I can only help with questions about this app."
3. Always respond in Bengali if the user asks in Bengali
4. Keep answers short and clear
5. Provide support team contact information when necessary
6. Do not share any personal opinions or unrelated information
7. Don't say you are AI assistant or model, say helpful assistant
8. Only answer questions related to the app 
"""

def get_ai_response(messages_history: list) -> str:
    try:
        # Groq ফরম্যাটে মেসেজ লিস্ট তৈরি
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        for msg in messages_history:
            role = "user" if msg.sender == "user" else "assistant"
            messages.append({"role": role, "content": msg.content})
        
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",   # Currently available model
            temperature=0.5,
            max_tokens=500
        )
        
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        # Fallback response if API fails
        return f"Sorry, I encountered an error: {str(e)}"