# 🤖 Mobile App AI Chatbot - Production Grade Backend

> Advanced AI-powered chatbot backend for mobile app support with JWT authentication, per-user conversations, and enterprise-grade error handling.

## ✨ Features

### 🔐 Authentication & Security
- ✅ **JWT Token Authentication** - Secure Bearer token authentication
- ✅ **Per-User Conversations** - Each user has isolated conversations
- ✅ **Password Hashing** - Bcrypt-based secure password storage
- ✅ **Token Validation** - Automatic token verification on all protected endpoints

### 💬 Chat Features
- ✅ **AI Responses** - Groq-powered LLM integration (llama-3.3-70b)
- ✅ **Conversation History** - Persistent message storage in PostgreSQL
- ✅ **Multi-language Support** - Bengali and English responses
- ✅ **Auto Title Generation** - First message becomes conversation title

### 🏢 Production Features
- ✅ **Comprehensive Error Handling** - Proper HTTP status codes & error messages
- ✅ **Structured Logging** - Debug, info, warning, and error logs
- ✅ **CORS Configuration** - Secure cross-origin requests
- ✅ **Health Check Endpoint** - Monitoring support
- ✅ **Input Validation** - Pydantic schema validation
- ✅ **Retry Logic** - Exponential backoff for API failures
- ✅ **Environment Validation** - Startup checks for required configs

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL database
- Groq API key
- FastAPI & dependencies

### Installation

1. **Clone/Setup Repository**
   ```bash
   cd c:\hasibul\Nikoo_chatbot
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Environment Variables** (`.env` file)
   ```env
   SECRET_KEY=your-super-secret-key-here
   GROQ_API_KEY=your-groq-api-key
   DATABASE_URL=postgresql://user:password@localhost:5432/nikoo_chatbot
   ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
   ```

5. **Initialize Database**
   ```bash
   python create_tables.py
   ```

6. **Run Server**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

Server running at: `http://localhost:8000`  
API Docs at: `http://localhost:8000/docs`

---

## 📋 API Endpoints

### Authentication Endpoints

#### 1. Register User
```
POST /auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "password": "secure_password_123"
}

Response:
{
  "msg": "User created successfully"
}
```

#### 2. Login (Get Token)
```
POST /auth/token
Content-Type: application/x-www-form-urlencoded

username=john_doe&password=secure_password_123

Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### Conversation Endpoints (Protected - Requires Bearer Token)

#### 3. Create Conversation
```
POST /conversations/
Authorization: Bearer YOUR_ACCESS_TOKEN

Response:
123  (conversation_id)
```

#### 4. List All User Conversations
```
GET /conversations/
Authorization: Bearer YOUR_ACCESS_TOKEN

Response:
{
  "conversations": [
    {
      "id": 1,
      "title": "How to use wallet...",
      "message_count": 5
    },
    {
      "id": 2,
      "title": "CAP feature guide...",
      "message_count": 3
    }
  ]
}
```

#### 5. Delete Conversation
```
DELETE /conversations/{conv_id}
Authorization: Bearer YOUR_ACCESS_TOKEN

Response:
{
  "msg": "Conversation deleted successfully"
}
```

### Message Endpoints (Protected - Requires Bearer Token)

#### 6. Send Message & Get AI Response
```
POST /conversations/{conv_id}/messages
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

{
  "content": "How do I withdraw money from my wallet?"
}

Response:
{
  "sender": "ai",
  "content": "To withdraw (payout):\n1. Go to Wallet → Request Payout\n2. Enter amount (minimum $10)..."
}
```

#### 7. Get Conversation Messages
```
GET /conversations/{conv_id}/messages
Authorization: Bearer YOUR_ACCESS_TOKEN

Response:
[
  {
    "id": 1,
    "sender": "user",
    "content": "How do I withdraw money?"
  },
  {
    "id": 2,
    "sender": "ai",
    "content": "To withdraw (payout):\n1. Go to Wallet..."
  }
]
```

### Utility Endpoints

#### 8. Health Check
```
GET /health

Response:
{
  "status": "ok",
  "service": "Mobile App AI Chatbot"
}
```

---

## 🔒 Authentication Flow

```
┌─────────────┐
│  1. Register│
│ /auth/register
└─────┬───────┘
      │
      ▼
┌─────────────┐
│  2. Login   │
│ /auth/token │ → Get Bearer Token
└─────┬───────┘
      │
      ▼
┌─────────────────────────┐
│ 3. Protected Endpoints  │
│ GET /conversations/     │ + Authorization: Bearer token
│ POST /conversations/... │
└─────────────────────────┘
```

### Authorization Header Example
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huX2RvZSIsImV4cCI6MTcwNDMwMzI5Nn0.abc...
```

---

## 🏗️ Project Structure

```
nikoo_chatbot/
├── main.py                    # FastAPI app setup, CORS, error handlers
├── app.py                     # Alternative entry point
├── create_tables.py           # Database initialization
├── database.py                # SQLAlchemy models & connection
├── dependencies.py            # JWT verification, get_current_user
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (create this)
│
├── routes/
│   ├── auth.py               # Login/register endpoints
│   ├── conversations.py       # Create/list/delete conversations
│   └── messages.py            # Send messages, get AI responses
│
├── services/
│   └── ai_services.py         # Groq API integration, error handling
│
├── models/
│   └── schemas.py             # Pydantic models for validation
│
└── utils/
    └── security.py            # JWT encoding/decoding, password hashing
```

---

## 📊 Database Schema

### users
```sql
id              INT PRIMARY KEY
username        VARCHAR UNIQUE
hashed_password VARCHAR
```

### conversations
```sql
id      INT PRIMARY KEY
user_id INT FOREIGN KEY (users.id)
title   VARCHAR
```

### messages
```sql
id                INT PRIMARY KEY
conversation_id   INT FOREIGN KEY (conversations.id)
sender            VARCHAR ('user' or 'ai')
content           TEXT
```

---

## 🛡️ Security Features

### 1. **JWT Token-Based Auth**
- Tokens expire after 24 hours
- User ID extracted from JWT payload
- All protected endpoints require valid token

### 2. **Per-User Data Isolation**
- Users can only access their own conversations
- Database queries filter by user_id
- Authorization checked on every request

### 3. **Password Security**
- Bcrypt hashing with auto-salt
- Never stored in plain text
- Verified during login

### 4. **Error Handling**
- No sensitive data in error messages
- Proper HTTP status codes
- Detailed logging for debugging

---

## 🚨 Error Handling

| Error | Status | Message |
|-------|--------|---------|
| Missing/Invalid Token | 401 | Invalid authentication credentials |
| User Not Found | 401 | User not found |
| Conversation Not Found | 404 | Conversation not found |
| Empty Message | 400 | Message content cannot be empty |
| Server Error | 500 | Failed to process request |

---

## 📝 How to Customize AI Prompts

Edit `APP_INFO` and `SYSTEM_PROMPT` in `services/ai_services.py`:

```python
APP_INFO = """
Our app features:
- Your feature 1
- Your feature 2
- Contact: support@yourapp.com
"""

SYSTEM_PROMPT = f"""You are a helpful assistant for our app.
{APP_INFO}

Rules:
1. Answer only about the app
2. Be friendly and helpful
3. ...
"""
```

---

## 📊 Monitoring & Logs

Server logs include:
- Request/response information
- Authentication events
- Database operations
- API errors with stack traces
- Startup/shutdown events

View logs in console when running with:
```bash
uvicorn main:app --reload
```

---

## 🚀 Deployment Checklist

- [ ] Environment variables properly set
- [ ] Database credentials secured
- [ ] Groq API key configured
- [ ] SECRET_KEY is random & secure (min 32 chars)
- [ ] CORS allowed origins updated for production
- [ ] Database backups configured
- [ ] Error logs monitored
- [ ] Rate limiting configured (if needed)
- [ ] HTTPS/SSL enabled in production
- [ ] Health check endpoint monitored

---

## 🔧 Troubleshooting

### "Missing required environment variable"
- Create `.env` file with all required variables

### "Invalid token"
- Token may have expired (24 hour limit)
- Re-login to get new token

### "Connection refused"
- Ensure PostgreSQL is running
- Check DATABASE_URL is correct

### "Groq API Error"
- Verify GROQ_API_KEY is valid
- Check API rate limits
- Retry automatically happens (exponential backoff)

---

## 📞 Support

Contact: **nikoo@app.com**

---

## 📄 Version

**v1.0.0** - Production Release  
Last Updated: December 30, 2025
