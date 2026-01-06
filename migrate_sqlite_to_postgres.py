#!/usr/bin/env python3
"""
Migrate data from SQLite to PostgreSQL database.

This script:
1. Connects to the existing SQLite database
2. Reads all data from all tables
3. Connects to PostgreSQL database
4. Inserts the data preserving all relationships

Usage:
    python migrate_sqlite_to_postgres.py
    or
    docker exec -it knowemployee-app-dev python migrate_sqlite_to_postgres.py
"""
import sys
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import json

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import models and app
from server import (
    app, db, 
    User, Testing, TestingResult, QuizToken, QuizResults, GPTPricer
)

def get_sqlite_engine():
    """Create SQLite engine for reading data."""
    # Try multiple possible paths
    possible_paths = [
        os.path.join('instance', 'service.db'),  # Local development
        os.path.join('/know', 'instance', 'service.db'),  # Docker container
        'instance/service.db',
        '/know/instance/service.db'
    ]
    
    sqlite_path = None
    for path in possible_paths:
        if os.path.exists(path):
            sqlite_path = path
            break
    
    if not sqlite_path:
        raise FileNotFoundError(
            f"SQLite database not found. Tried: {', '.join(possible_paths)}"
        )
    
    # Use absolute path for SQLite connection
    abs_path = os.path.abspath(sqlite_path)
    return create_engine(f'sqlite:///{abs_path}', echo=False)

def get_postgres_engine():
    """Create PostgreSQL engine from app config."""
    return db.engine

def migrate_table(sqlite_session, postgres_session, model_class, table_name):
    """
    Migrate data from SQLite to PostgreSQL for a given model.
    
    Args:
        sqlite_session: SQLAlchemy session for SQLite
        postgres_session: SQLAlchemy session for PostgreSQL
        model_class: SQLAlchemy model class
        table_name: Name of the table
    """
    print(f"\nMigrating {table_name}...")
    
    # Get all records from SQLite
    sqlite_records = sqlite_session.query(model_class).all()
    
    if not sqlite_records:
        print(f"  No records found in {table_name}")
        return 0
    
    print(f"  Found {len(sqlite_records)} records")
    
    migrated_count = 0
    skipped_count = 0
    
    for record in sqlite_records:
        try:
            # Convert SQLite record to dict, excluding SQLAlchemy internal attributes
            record_dict = {}
            for column in model_class.__table__.columns:
                value = getattr(record, column.name)
                
                # Handle None values
                if value is None:
                    record_dict[column.name] = None
                    continue
                
                # Handle data type conversions based on PostgreSQL column type
                column_type = str(column.type)
                
                # Handle string length limits (PostgreSQL is stricter than SQLite)
                if 'VARCHAR' in column_type or 'String' in column_type:
                    # Extract length limit if present
                    max_length = None
                    if '(' in column_type:
                        try:
                            max_length = int(column_type.split('(')[1].split(')')[0])
                        except:
                            pass
                    
                    str_value = str(value) if value is not None else ''
                    if max_length and len(str_value) > max_length:
                        # For password field, we might need to increase the limit
                        # For now, truncate with warning
                        if column.name == 'password':
                            print(f"  Warning: {table_name} id={record.id} password too long ({len(str_value)} > {max_length})")
                            print(f"    Consider increasing password field size in model. Truncating...")
                        else:
                            print(f"  Warning: {table_name} id={record.id} column {column.name} value too long ({len(str_value)} > {max_length}), truncating")
                        record_dict[column.name] = str_value[:max_length]
                    else:
                        record_dict[column.name] = str_value
                
                # Handle integer columns - convert boolean to int if needed
                elif 'INTEGER' in column_type or 'Integer' in column_type:
                    if isinstance(value, bool):
                        record_dict[column.name] = 1 if value else 0
                    elif isinstance(value, (int, float)):
                        record_dict[column.name] = int(value)
                    else:
                        try:
                            record_dict[column.name] = int(value) if value else 0
                        except:
                            record_dict[column.name] = 0
                
                # Handle boolean columns
                elif 'BOOLEAN' in column_type or 'Boolean' in column_type:
                    if isinstance(value, bool):
                        record_dict[column.name] = value
                    elif isinstance(value, (int, float)):
                        record_dict[column.name] = bool(value)
                    elif isinstance(value, str):
                        record_dict[column.name] = value.lower() in ('true', '1', 'yes', 'on')
                    else:
                        record_dict[column.name] = bool(value)
                
                # Handle datetime
                elif hasattr(value, 'isoformat'):
                    record_dict[column.name] = value
                
                # Handle other types
                elif isinstance(value, (int, float, str)):
                    record_dict[column.name] = value
                else:
                    record_dict[column.name] = str(value)
            
            # Check if record already exists in PostgreSQL (by primary key)
            existing = postgres_session.query(model_class).filter_by(id=record.id).first()
            if existing:
                print(f"  Skipping {table_name} id={record.id} (already exists)")
                skipped_count += 1
                continue
            
            # Create new record in PostgreSQL
            new_record = model_class(**record_dict)
            postgres_session.add(new_record)
            migrated_count += 1
            
        except Exception as e:
            print(f"  Error migrating {table_name} id={record.id}: {e}")
            postgres_session.rollback()
            continue
    
    try:
        postgres_session.commit()
        print(f"  ✓ Migrated {migrated_count} records, skipped {skipped_count}")
        return migrated_count
    except Exception as e:
        print(f"  ✗ Error committing {table_name}: {e}")
        postgres_session.rollback()
        return 0

def migrate_all_data():
    """Migrate all data from SQLite to PostgreSQL."""
    
    print("=" * 60)
    print("SQLite to PostgreSQL Migration Script")
    print("=" * 60)
    
    # Check if SQLite database exists (try multiple paths)
    possible_paths = [
        os.path.join('instance', 'service.db'),
        os.path.join('/know', 'instance', 'service.db'),
        'instance/service.db',
        '/know/instance/service.db'
    ]
    
    sqlite_path = None
    for path in possible_paths:
        if os.path.exists(path):
            sqlite_path = path
            break
    
    if not sqlite_path:
        print(f"Error: SQLite database not found. Tried: {', '.join(possible_paths)}")
        return False
    
    print(f"   Found SQLite database at: {sqlite_path}")
    
    # Create engines
    print("\n1. Connecting to databases...")
    sqlite_engine = get_sqlite_engine()
    postgres_engine = get_postgres_engine()
    
    # Create sessions
    SQLiteSession = sessionmaker(bind=sqlite_engine)
    sqlite_session = SQLiteSession()
    
    with app.app_context():
        postgres_session = db.session
        
        print("   ✓ Connected to SQLite")
        print("   ✓ Connected to PostgreSQL")
        
        # Verify PostgreSQL tables exist
        print("\n2. Verifying PostgreSQL tables...")
        inspector = db.inspect(db.engine)
        required_tables = ['user', 'testing', 'testing_result', 'quiz_token', 'quiz_results', 'gpt_pricer']
        existing_tables = inspector.get_table_names()
        
        missing_tables = [t for t in required_tables if t not in existing_tables]
        if missing_tables:
            print(f"   ✗ Missing tables: {missing_tables}")
            print("   Please run 'flask db upgrade' first to create tables")
            return False
        
        print("   ✓ All required tables exist")
        
        # Get record counts from SQLite
        print("\n3. Analyzing SQLite database...")
        sqlite_counts = {}
        for model_class, table_name in [
            (User, 'user'),
            (Testing, 'testing'),
            (TestingResult, 'testing_result'),
            (QuizToken, 'quiz_token'),
            (QuizResults, 'quiz_results'),
            (GPTPricer, 'gpt_pricer')
        ]:
            count = sqlite_session.query(model_class).count()
            sqlite_counts[table_name] = count
            if count > 0:
                print(f"   {table_name}: {count} records")
        
        total_records = sum(sqlite_counts.values())
        if total_records == 0:
            print("\n   No data found in SQLite database. Nothing to migrate.")
            return True
        
        print(f"\n   Total records to migrate: {total_records}")
        
        # Ask for confirmation (skip in non-interactive mode)
        print("\n4. Ready to migrate data...")
        if os.getenv('AUTO_MIGRATE', '').lower() != 'true':
            try:
                response = input("   Do you want to proceed? (yes/no): ").strip().lower()
                if response not in ['yes', 'y']:
                    print("   Migration cancelled.")
                    return False
            except EOFError:
                # Non-interactive mode (e.g., in Docker)
                print("   Non-interactive mode detected. Use AUTO_MIGRATE=true to skip confirmation.")
                print("   Migration cancelled for safety.")
                return False
        else:
            print("   AUTO_MIGRATE=true detected. Proceeding automatically...")
        
        # Migrate tables in order (respecting dependencies)
        print("\n5. Migrating data...")
        total_migrated = 0
        
        # Order matters: migrate tables without foreign keys first
        migration_order = [
            (User, 'user'),
            (Testing, 'testing'),
            (QuizToken, 'quiz_token'),
            (TestingResult, 'testing_result'),
            (QuizResults, 'quiz_results'),
            (GPTPricer, 'gpt_pricer'),
        ]
        
        for model_class, table_name in migration_order:
            if sqlite_counts.get(table_name, 0) > 0:
                count = migrate_table(sqlite_session, postgres_session, model_class, table_name)
                total_migrated += count
        
        print("\n" + "=" * 60)
        print(f"Migration complete!")
        print(f"Total records migrated: {total_migrated}")
        print("=" * 60)
        
        # Verify migration
        print("\n6. Verifying migration...")
        for model_class, table_name in migration_order:
            postgres_count = postgres_session.query(model_class).count()
            sqlite_count = sqlite_counts.get(table_name, 0)
            status = "✓" if postgres_count >= sqlite_count else "✗"
            print(f"   {status} {table_name}: {postgres_count} records (SQLite had {sqlite_count})")
        
        sqlite_session.close()
        return True

if __name__ == '__main__':
    with app.app_context():
        try:
            success = migrate_all_data()
            if success:
                print("\n✓ Migration completed successfully!")
                sys.exit(0)
            else:
                print("\n✗ Migration failed or was cancelled.")
                sys.exit(1)
        except Exception as e:
            print(f"\n✗ Error during migration: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

