import os
from database import SQLALCHEMY_DATABASE_URL, engine
import models
import seed_data

DB_PATH = None
# SQLALCHEMY_DATABASE_URL expected in format sqlite:///./student_grading.db
if SQLALCHEMY_DATABASE_URL.startswith("sqlite:///"):
    DB_PATH = SQLALCHEMY_DATABASE_URL.replace("sqlite:///", "")

if __name__ == '__main__':
    if DB_PATH and os.path.exists(DB_PATH):
        print(f"Removing existing database file: {DB_PATH}")
        os.remove(DB_PATH)
    else:
        print("No existing database file found; creating new one.")

    # Recreate schema
    print("Creating database schema...")
    models.Base.metadata.create_all(bind=engine)
    print("Schema created.")

    # Optional: seed sample data
    try:
        seed_data.seed_database()
    except Exception as e:
        print(f"Seeding failed: {e}")
    print("Done.")
