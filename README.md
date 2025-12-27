# Nikoo Chatbot - Configuration Guide

## 🚀 System is Live and Working!

### Features Implemented:
✅ **AI Assistant** - Groq powered responses  
✅ **Chat History** - All messages saved in database  
✅ **Custom Prompts** - Easy to customize app information  
✅ **Multi-language** - Supports Bengali and English  
✅ **No Authentication** - Public access  

---

## 📝 How to Customize App Information

Edit the `APP_INFO` variable in `services/ai_services.py`:

```python
APP_INFO = """
আমাদের অ্যাপ একটি Mobile App Support Chatbot যা ব্যবহারকারীদের সাহায্য করে।

অ্যাপের বৈশিষ্ট্য:
- রিয়েল-টাইম চ্যাট সাপোর্ট
- AI-চালিত সমস্যা সমাধান
- ২৪/৭ উপলব্ধতা
- একাধিক ভাষা সমর্থন

যোগাযোগের জন্য: support@app.com
"""
```

**কাস্টমাইজ করুন:**
- আপনার অ্যাপের বৈশিষ্ট্য যোগ করুন
- সাপোর্ট ইমেইল বা ফোন নাম্বার দিন
- FAQ সমূহ যুক্ত করুন
- নির্দিষ্ট নিয়ম বা শর্তাবলী যোগ করুন

---

## 🔌 API Endpoints

### Create Conversation
```
POST /conversations/
Response: conversation_id (integer)
```

### List Conversations
```
GET /conversations/
Response: {"conversations": [{"id": 1, "title": "..."}]}
```

### Send Message (with AI Response)
```
POST /conversations/{conv_id}/messages
Body: {"content": "Your message"}
Response: {"sender": "ai", "content": "AI response"}
```

### Get Chat History
```
GET /conversations/{conv_id}/messages
Response: [{"sender": "user", "content": "..."}, {"sender": "ai", "content": "..."}]
```

### Delete Conversation
```
DELETE /conversations/{conv_id}
Response: {"msg": "Conversation deleted"}
```

---

## 📊 Database Schema

### users table
- id (int) - User ID
- username (string) - Username
- hashed_password (string) - Password hash

### conversations table
- id (int) - Conversation ID
- user_id (int) - Foreign key to users
- title (string) - Conversation title
- created_at (timestamp) - Created time

### messages table
- id (int) - Message ID
- conversation_id (int) - Foreign key to conversations
- sender (string) - "user" or "ai"
- content (text) - Message content
- created_at (timestamp) - Created time

---

## 🛠️ Server Status

✅ Running on: `http://127.0.0.1:8000`  
✅ Documentation: `http://127.0.0.1:8000/docs`  
✅ Database: PostgreSQL (localhost:5432)  
✅ AI Model: llama-3.3-70b-versatile (Groq)  

---

## 📝 Example Requests

### Create a new conversation
```bash
curl -X POST http://127.0.0.1:8000/conversations/
```

### Send a message
```bash
curl -X POST http://127.0.0.1:8000/conversations/1/messages \
  -H "Content-Type: application/json" \
  -d '{"content": "আপনার প্রশ্ন এখানে"}'
```

### Get conversation history
```bash
curl http://127.0.0.1:8000/conversations/1/messages
```

---

## 💡 Tips

1. **Customize the AI personality** - Edit the SYSTEM_PROMPT in `services/ai_services.py`
2. **Add more app features** - Update APP_INFO with your app details
3. **Change language** - Modify the prompt to support more languages
4. **Add new endpoints** - Extend the routes for additional functionality

---

**Last Updated:** December 27, 2025  
**Status:** Production Ready ✅
