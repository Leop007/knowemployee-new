#!/usr/bin/env python3
"""
Initialize PostgreSQL database by creating all tables from models.
This script should be run once when setting up a fresh PostgreSQL database.
"""
import sys
import os

# Add the current directory to the path so we can import server
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import app and db, and all models to ensure they're registered
from server import app, db, User, Testing, TestingResult, QuizToken, QuizResults, GPTPricer

def init_database():
    """Create all tables from models and stamp the database with current migration head."""
    with app.app_context():
        print("Creating all tables from models...")
        db.create_all()
        print("✓ All tables created successfully")
        
        # Stamp the database with the current migration head
        # This tells Alembic that all migrations have been applied
        from flask_migrate import stamp
        try:
            print("Stamping database with current migration head...")
            stamp()
            print("✓ Database stamped successfully")
            print("\nDatabase initialization complete!")
            print("You can now use the application normally.")
        except Exception as e:
            print(f"Note: Could not stamp database: {e}")
            print("You may need to run 'flask db stamp head' manually")

if __name__ == '__main__':
    init_database()

