"""
Database initialization script
Run this to create all tables before starting the application
"""

from database import init_db

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Database initialization complete!")
    print("\nYou can now run the application with:")
    print("  python app.py")
    print("\nOr with uvicorn:")
    print("  uvicorn app:app --reload")
