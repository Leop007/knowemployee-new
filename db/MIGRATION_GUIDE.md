# SQLite to PostgreSQL Migration Guide

This guide explains how to migrate existing data from SQLite to PostgreSQL.

## Prerequisites

1. ✅ PostgreSQL database is set up and running
2. ✅ All tables are created in PostgreSQL (run `flask db upgrade` if needed)
3. ✅ SQLite database exists at `instance/service.db`
4. ✅ Both databases are accessible

## Migration Steps

### Option 1: Interactive Migration (Recommended)

1. **Make sure containers are running:**
   ```bash
   docker-compose -f docker-compose.dev.yml up -d
   ```

2. **Run the migration script:**
   ```bash
   docker exec -it knowemployee-app-dev python migrate_sqlite_to_postgres.py
   ```

3. **Follow the prompts:**
   - The script will show you what data will be migrated
   - Type `yes` to confirm and proceed
   - The script will migrate all tables in the correct order

### Option 2: Non-Interactive Migration

If you want to skip the confirmation prompt (useful for automation):

```bash
docker exec -e AUTO_MIGRATE=true knowemployee-app-dev python migrate_sqlite_to_postgres.py
```

## What Gets Migrated

The script migrates data from these tables:
- `user` - User accounts and company information
- `testing` - Testing tokens
- `testing_result` - Feedback results
- `quiz_token` - Quiz configurations
- `quiz_results` - Quiz responses
- `gpt_pricer` - GPT pricing tracking

## Migration Process

1. **Analysis Phase:**
   - Connects to both databases
   - Counts records in each SQLite table
   - Verifies PostgreSQL tables exist

2. **Migration Phase:**
   - Migrates tables in dependency order
   - Skips records that already exist (by ID)
   - Preserves all relationships

3. **Verification Phase:**
   - Compares record counts
   - Reports any discrepancies

## Safety Features

- ✅ **Idempotent**: Can be run multiple times safely
- ✅ **Skip duplicates**: Won't create duplicate records
- ✅ **Transaction-based**: Rolls back on errors
- ✅ **Verification**: Checks data after migration

## Troubleshooting

### Error: "SQLite database not found"
- Make sure `instance/service.db` exists
- Check that the file is accessible in the container

### Error: "Missing tables in PostgreSQL"
- Run `flask db upgrade` first to create all tables
- Verify PostgreSQL connection is working

### Error: "Duplicate key" or constraint violations
- The script should skip duplicates automatically
- If you see this, there might be data integrity issues
- Check the error message for details

### Partial Migration
- The script migrates tables one at a time
- If it fails partway through, you can run it again
- It will skip records that already exist

## After Migration

1. **Verify the data:**
   ```bash
   # Check record counts
   docker exec -it knowemployee-postgres-dev psql -U knowemployee -d knowemployee_db -c "SELECT 'user' as table, COUNT(*) FROM \"user\" UNION ALL SELECT 'testing_result', COUNT(*) FROM testing_result;"
   ```

2. **Test the application:**
   - Log in with existing accounts
   - Verify feedback data is accessible
   - Check that all features work correctly

3. **Backup the SQLite database** (optional but recommended):
   ```bash
   cp instance/service.db instance/service.db.backup
   ```

4. **Once verified, you can remove SQLite** (optional):
   - The old SQLite database is no longer needed
   - Keep a backup just in case

## Notes

- The migration preserves all data including:
  - Encrypted voice transcriptions
  - JSON data in text columns
  - Timestamps and relationships
  - All user accounts and settings

- Data types are automatically converted where needed
- The migration is safe to run multiple times

