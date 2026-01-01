# create_tables.py
from database import Base, engine, SessionLocal, User
from utils.security import get_password_hash

Base.metadata.create_all(bind=engine)
print("✓ Tables created successfully!")

# Create default test user for development
db = SessionLocal()
try:
    existing_user = db.query(User).filter(User.id == 1).first()
    if not existing_user:
        test_user = User(
            id=1, 
            username="test_user", 
            hashed_password=get_password_hash("dev_password")
        )
        db.add(test_user)
        db.commit()
        print("✓ Default test user created (id=1, username=test_user)")
    else:
        print(f"✓ User already exists: {existing_user.username}")
finally:
    db.close()