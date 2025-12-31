from database import SessionLocal, engine
from sqlalchemy import text

db = SessionLocal()

# Add search_keywords column if it doesn't exist
try:
    db.execute(text("ALTER TABLE user_profile ADD COLUMN search_keywords TEXT"))
    db.commit()
    print("✅ Added search_keywords column to user_profile")
except Exception as e:
    if "duplicate column" in str(e).lower() or "already exists" in str(e).lower():
        print("⚠️ search_keywords column already exists")
    else:
        print(f"Error: {e}")
    db.rollback()

db.close()
