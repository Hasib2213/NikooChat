# 🚀 Deployment Guide - Production Grade Chatbot

## Pre-Deployment Checklist

### 1. Environment Setup
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created with all required variables
- [ ] `tenacity` package installed for retry logic
- [ ] Virtual environment activated

### 2. Database Preparation
- [ ] PostgreSQL running and accessible
- [ ] Database created and user permissions set
- [ ] `python create_tables.py` executed successfully
- [ ] Tables verified in database

### 3. API Keys & Credentials
- [ ] Groq API key obtained and verified
- [ ] SECRET_KEY generated securely (min 32 chars)
- [ ] Database credentials tested
- [ ] All credentials in `.env` file (not in code)

### 4. Security Review
- [ ] Password hashing enabled (Bcrypt)
- [ ] JWT token expiration set (24 hours)
- [ ] CORS origins configured for production
- [ ] No debug mode in production
- [ ] Error messages don't expose sensitive data

### 5. Code Quality
- [ ] Error handling implemented
- [ ] Logging configured
- [ ] Input validation enabled
- [ ] Retry logic with exponential backoff

---

## Deployment Options

### Option 1: Local Development
```bash
# 1. Activate virtual environment
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 2. Create .env file with variables

# 3. Initialize database
python create_tables.py

# 4. Run development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Option 2: Production with Gunicorn
```bash
# Install gunicorn
pip install gunicorn

# Run with multiple workers
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```

**Configuration:**
- Workers: 4 (adjust based on CPU cores)
- Worker class: UvicornWorker
- Bind: 0.0.0.0:8000

### Option 3: Docker Deployment

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Build & Run:**
```bash
# Build image
docker build -t nikoo-chatbot:latest .

# Run container
docker run -p 8000:8000 \
  --env-file .env \
  -e DATABASE_URL=postgresql://... \
  nikoo-chatbot:latest
```

### Option 4: Docker Compose
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: nikoo_chatbot
      POSTGRES_USER: chatbot_user
      POSTGRES_PASSWORD: secure_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  chatbot:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://chatbot_user:secure_password@postgres:5432/nikoo_chatbot
      SECRET_KEY: ${SECRET_KEY}
      GROQ_API_KEY: ${GROQ_API_KEY}
    depends_on:
      - postgres
    volumes:
      - ./logs:/app/logs

volumes:
  postgres_data:
```

Run with:
```bash
docker-compose up -d
```

---

## Environment Variables Configuration

### Production `.env` Template
```env
# 🔐 Security (Generate using: python -c "import secrets; print(secrets.token_urlsafe(32))")
SECRET_KEY=<generate-a-random-string>

# 🤖 AI Service (Get from https://console.groq.com)
GROQ_API_KEY=<your-groq-api-key>

# 📊 Database (PostgreSQL)
DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<database>

# 🌐 CORS (Comma-separated origins)
ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com

# 🚀 Server (Optional)
# LOG_LEVEL=INFO
# WORKERS=4
```

---

## Database Backup & Recovery

### PostgreSQL Backup
```bash
# Full database backup
pg_dump -U username nikoo_chatbot > backup_$(date +%Y%m%d).sql

# Compressed backup
pg_dump -U username nikoo_chatbot | gzip > backup_$(date +%Y%m%d).sql.gz

# Scheduled daily backup (cron)
0 2 * * * pg_dump -U username nikoo_chatbot | gzip > /backups/backup_$(date +\%Y\%m\%d).sql.gz
```

### Restore from Backup
```bash
# Restore from backup
psql -U username nikoo_chatbot < backup_20250101.sql

# Restore from compressed backup
gunzip -c backup_20250101.sql.gz | psql -U username nikoo_chatbot
```

---

## Monitoring & Health Checks

### Health Check Endpoint
```bash
# Test server health
curl http://localhost:8000/health

# Expected response:
{
  "status": "ok",
  "service": "Mobile App AI Chatbot"
}
```

### Server Logs Monitoring
```bash
# Follow logs in real-time (if using gunicorn)
tail -f gunicorn.log

# Check for errors
grep ERROR gunicorn.log

# Monitor specific endpoint
grep "/conversations" access.log
```

### Database Health Check
```bash
# Test database connection
python -c "from database import SessionLocal; db = SessionLocal(); print('✅ Database connected'); db.close()"
```

### Groq API Status
```bash
# Test API connectivity
python -c "from groq import Groq; import os; c = Groq(api_key=os.getenv('GROQ_API_KEY')); print('✅ Groq API connected')"
```

---

## Performance Optimization

### 1. Database Optimization
```sql
-- Create indexes for faster queries
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_users_username ON users(username);

-- Vacuum database
VACUUM ANALYZE;
```

### 2. API Optimization
- Enable gzip compression
- Cache frequently accessed data
- Implement rate limiting
- Use connection pooling (SQLAlchemy default)

### 3. Worker Configuration
```bash
# For CPU-bound tasks
workers = (2 * CPU_count) + 1

# For I/O-bound tasks
workers = CPU_count * 2 to 4

# Check CPU count in Python
python -c "import multiprocessing; print(multiprocessing.cpu_count())"
```

---

## Error Handling & Troubleshooting

### Common Production Issues

#### 1. "Connection refused" Error
```
Cause: Database not running or incorrect credentials
Solution:
- Check PostgreSQL is running: pg_isready -h localhost
- Verify DATABASE_URL in .env
- Check database user permissions
```

#### 2. "Invalid token" Errors
```
Cause: JWT token expired or invalid
Solution:
- Token expires after 24 hours - client must re-login
- Check SECRET_KEY is consistent across deployments
- Verify Bearer token format in headers
```

#### 3. "Groq API Error"
```
Cause: API rate limit or invalid key
Solution:
- Check GROQ_API_KEY is valid
- Monitor API rate limits
- Retry logic automatically handles transient errors
- Check Groq API status: https://status.groq.com
```

#### 4. "Memory Error"
```
Cause: Large messages or many conversations
Solution:
- Increase worker memory limits
- Implement pagination for conversation lists
- Archive old messages
- Monitor memory usage
```

---

## Security Hardening

### 1. HTTPS/SSL
```bash
# Using Let's Encrypt (Certbot)
certbot certonly --standalone -d yourdomain.com

# Configure in reverse proxy (nginx)
ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
```

### 2. Rate Limiting
Add to `main.py`:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/conversations/{conv_id}/messages")
@limiter.limit("30/minute")
async def send_message(...):
    ...
```

### 3. Input Validation
- Already implemented in schemas.py
- Min/max length constraints
- Type validation

### 4. SQL Injection Prevention
- Using SQLAlchemy ORM (parameterized queries)
- No raw SQL queries in code

### 5. Authentication Security
- JWT tokens with expiration
- Bcrypt password hashing
- No sensitive data in error messages

---

## Monitoring Stack (Optional)

### Prometheus + Grafana
```python
# Add to main.py
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)

# Access metrics: http://localhost:8000/metrics
```

### ELK Stack (Elasticsearch, Logstash, Kibana)
```python
# Add logging to stdout for container systems
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
```

---

## CI/CD Integration

### GitHub Actions Example
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python -m pytest tests/

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: docker build -t nikoo-chatbot:latest .
      - run: docker push your-registry/nikoo-chatbot:latest
      - run: kubectl set image deployment/chatbot chatbot=your-registry/nikoo-chatbot:latest
```

---

## Version History

**v1.0.0** - Initial Production Release
- JWT authentication
- Per-user conversations
- Groq AI integration
- Comprehensive error handling
- Production-ready logging

---

## Support & Resources

- **Documentation**: See README_PRODUCTION.md
- **API Docs**: http://localhost:8000/docs (Swagger)
- **Support Email**: nikoo@app.com
- **Issues**: Create GitHub issue or contact support

---

**Last Updated**: December 30, 2025  
**Status**: Production Ready ✅
