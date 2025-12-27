# create_tables.py
from database import Base, engine, SessionLocal, User

Base.metadata.create_all(bind=engine)
print("✓ Tables created successfully!")

# Create a default anonymous user for the public chatbot
db = SessionLocal()
try:
    existing_user = db.query(User).filter(User.id == 1).first()
    if not existing_user:
        anonymous_user = User(id=1, username="anonymous", hashed_password="")
        db.add(anonymous_user)
        db.commit()
        print("✓ Default anonymous user created (id=1)")
    else:
        print("✓ Anonymous user already exists")
finally:
    db.close()