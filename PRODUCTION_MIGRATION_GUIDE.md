# Production Migration Guide: SQLite to PostgreSQL

## Overview

This guide will help you safely migrate your production environment from SQLite to PostgreSQL. The migration process includes:
1. Committing and merging code changes
2. Setting up PostgreSQL in production
3. Migrating data from SQLite to PostgreSQL
4. Verifying the migration
5. Rolling back plan (if needed)

## ⚠️ IMPORTANT: Pre-Migration Checklist

Before starting, ensure you have:
- [ ] **Full backup of production SQLite database** (`service.db`)
- [ ] **Backup of production .env file**
- [ ] **Maintenance window scheduled** (recommend 1-2 hours)
- [ ] **Access to production server**
- [ ] **PostgreSQL credentials ready**
- [ ] **Tested migration script in staging/dev environment**

---

## Step 1: Commit and Merge to Main

### 1.1 Review Changes
```bash
git status
git diff
```

### 1.2 Stage All Changes
```bash
# Add modified files
git add .

# Review what will be committed
git status
```

### 1.3 Commit Changes
```bash
git commit -m "Add OAuth login (Google/Microsoft), UI improvements, and PostgreSQL support

- Added Google and Microsoft OAuth login integration
- Improved language selector positioning
- Added PostgreSQL database support with SQLite fallback
- UI/UX improvements for login and registration pages
- Updated styling and responsive design"
```

### 1.4 Switch to Main and Merge
```bash
# Switch to main branch
git checkout main

# Pull latest changes
git pull origin main

# Merge db-postgres branch
git merge db-postgres

# Push to remote
git push origin main
```

### 1.5 Tag the Release (Optional but Recommended)
```bash
git tag -a v1.0.0 -m "Release: OAuth integration and PostgreSQL support"
git push origin v1.0.0
```

---

## Step 2: Prepare Production Environment

### 2.1 Backup Current Production Database

**CRITICAL: Do this first!**

```bash
# On production server, backup SQLite database
cd /path/to/your/production/app
cp service.db service.db.backup.$(date +%Y%m%d_%H%M%S)

# Also backup .env file
cp .env .env.backup.$(date +%Y%m%d_%H%M%S)

# Verify backup exists
ls -lh service.db.backup.*
```

### 2.2 Pull Latest Code to Production

```bash
# On production server
cd /path/to/your/production/app
git pull origin main

# Verify you're on the right commit
git log -1
```

### 2.3 Update Production .env File

Add PostgreSQL environment variables to your production `.env` file:

```bash
# Edit .env file
nano .env  # or use your preferred editor
```

Add these variables:
```env
# PostgreSQL Configuration
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_USER=knowemployee_prod
POSTGRES_PASSWORD=<STRONG_PASSWORD_HERE>
POSTGRES_DB=knowemployee_prod_db

# Keep existing variables (don't remove them)
# FLASK_ENV=production
# SECRET_KEY=...
# etc.
```

**Important:** 
- Use a **strong, unique password** for production
- **DO NOT** remove existing variables
- The app will use PostgreSQL if these vars are set, otherwise fallback to SQLite

---

## Step 3: Set Up PostgreSQL in Production

### 3.1 Start PostgreSQL Container

The `docker-compose.yml` already includes PostgreSQL configuration. Start it:

```bash
# Start PostgreSQL container (app will still use SQLite until migration)
docker-compose up -d postgres

# Wait for PostgreSQL to be ready
docker-compose ps postgres

# Check logs to ensure it started correctly
docker-compose logs postgres
```

### 3.2 Verify PostgreSQL is Running

```bash
# Test connection
docker exec -it knowemployee-postgres psql -U knowemployee_prod -d knowemployee_prod_db -c "SELECT version();"
```

### 3.3 Initialize Database Schema

```bash
# Run migrations to create tables in PostgreSQL
docker exec -it knowemployee-app flask db upgrade

# Verify tables were created
docker exec -it knowemployee-postgres psql -U knowemployee_prod -d knowemployee_prod_db -c "\dt"
```

---

## Step 4: Migrate Data from SQLite to PostgreSQL

### 4.1 Copy Migration Script to Production

The migration script `migrate_sqlite_to_postgres.py` should already be in your codebase. Verify it exists:

```bash
ls -la migrate_sqlite_to_postgres.py
```

### 4.2 Run Migration Script

**⚠️ MAINTENANCE MODE: Put your app in maintenance mode before running migration**

```bash
# Option 1: Stop the app temporarily
docker-compose stop knowemployee

# Option 2: Or put up a maintenance page in nginx

# Run the migration script
docker exec -it knowemployee-app python migrate_sqlite_to_postgres.py

# The script will:
# 1. Connect to SQLite database
# 2. Read all data
# 3. Write to PostgreSQL
# 4. Verify data integrity
```

### 4.3 Verify Migration Success

```bash
# Check row counts match
docker exec -it knowemployee-postgres psql -U knowemployee_prod -d knowemployee_prod_db -c "SELECT COUNT(*) FROM \"user\";"
docker exec -it knowemployee-postgres psql -U knowemployee_prod -d knowemployee_prod_db -c "SELECT COUNT(*) FROM testing;"

# Compare with SQLite (if you have sqlite3 installed)
sqlite3 service.db "SELECT COUNT(*) FROM user;"
sqlite3 service.db "SELECT COUNT(*) FROM testing;"
```

### 4.4 Test Application with PostgreSQL

```bash
# Restart the app (it should now use PostgreSQL)
docker-compose restart knowemployee

# Check logs to verify it's using PostgreSQL
docker-compose logs knowemployee | grep -i "Using PostgreSQL database"

# Test login and key functionality
# - Login with existing user
# - Create a new survey
# - Submit feedback
# - Check dashboard
```

---

## Step 5: Final Verification

### 5.1 Verify Database Connection

Check application logs:
```bash
docker-compose logs knowemployee | tail -50
```

You should see: `Using PostgreSQL database: postgres:5432/knowemployee_prod_db`

### 5.2 Test Critical Functionality

- [ ] User login works
- [ ] User registration works
- [ ] Dashboard loads correctly
- [ ] Surveys can be created
- [ ] Feedback can be submitted
- [ ] Data appears correctly

### 5.3 Monitor for Issues

```bash
# Watch logs for errors
docker-compose logs -f knowemployee

# Monitor for 15-30 minutes after migration
```

---

## Step 6: Post-Migration Cleanup (After Verification)

**⚠️ Only do this after confirming everything works for 24-48 hours**

### 6.1 Archive SQLite Database

```bash
# Move SQLite database to archive (don't delete yet!)
mkdir -p backups/sqlite_archive
mv service.db backups/sqlite_archive/service.db.$(date +%Y%m%d)
mv service.db.backup.* backups/sqlite_archive/
```

### 6.2 Update Documentation

Update any documentation that references SQLite.

---

## Rollback Plan (If Something Goes Wrong)

### Quick Rollback Steps

1. **Stop the application:**
   ```bash
   docker-compose stop knowemployee
   ```

2. **Remove PostgreSQL environment variables from .env:**
   ```bash
   # Comment out or remove PostgreSQL vars
   # POSTGRES_HOST=postgres
   # POSTGRES_PORT=5432
   # etc.
   ```

3. **Restore SQLite database:**
   ```bash
   cp service.db.backup.YYYYMMDD_HHMMSS service.db
   ```

4. **Restart application:**
   ```bash
   docker-compose start knowemployee
   ```

5. **Verify application works:**
   ```bash
   docker-compose logs knowemployee
   ```

---

## Troubleshooting

### Issue: Migration script fails

**Solution:**
- Check SQLite database is accessible
- Verify PostgreSQL connection credentials
- Check disk space
- Review migration script logs

### Issue: Application can't connect to PostgreSQL

**Solution:**
- Verify environment variables are set correctly
- Check PostgreSQL container is running: `docker-compose ps postgres`
- Test connection manually: `docker exec -it knowemployee-postgres psql -U knowemployee_prod -d knowemployee_prod_db`
- Check network connectivity: `docker network ls`

### Issue: Data mismatch after migration

**Solution:**
- Compare row counts between SQLite and PostgreSQL
- Check for data type mismatches
- Review migration script for any skipped tables
- Consider re-running migration (after backing up PostgreSQL)

### Issue: Application errors after migration

**Solution:**
- Check application logs: `docker-compose logs knowemployee`
- Verify database schema matches: `docker exec -it knowemployee-postgres psql -U knowemployee_prod -d knowemployee_prod_db -c "\d"`
- Check for missing indexes or constraints
- Rollback if critical issues found

---

## Support and Questions

If you encounter issues during migration:
1. Check the logs first
2. Review this guide
3. Check `db/MIGRATION_GUIDE.md` for additional details
4. Review `migrate_sqlite_to_postgres.py` script

---

## Timeline Estimate

- **Preparation:** 15-30 minutes
- **Code deployment:** 5-10 minutes
- **PostgreSQL setup:** 10-15 minutes
- **Data migration:** 5-30 minutes (depends on data size)
- **Verification:** 15-30 minutes
- **Total:** ~1-2 hours (with buffer)

---

## Success Criteria

Migration is successful when:
- ✅ Application starts without errors
- ✅ All existing users can log in
- ✅ All existing data is accessible
- ✅ New data can be created
- ✅ No errors in application logs
- ✅ Performance is acceptable

Good luck with your migration! 🚀

