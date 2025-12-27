from fastapi import FastAPI
from routes import conversations, messages

app = FastAPI(title="Mobile App AI Chatbot Backend")

app.include_router(conversations.router)
app.include_router(messages.router)

@app.get("/")
def home():
    return {"message": "Welcome to the App Support Chatbot API!"}