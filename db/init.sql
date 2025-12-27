-- PostgreSQL Database Initialization Script
-- This script runs automatically when the PostgreSQL container is first created

-- Create database if it doesn't exist (handled by POSTGRES_DB env var, but keeping for reference)
-- The database is created automatically by PostgreSQL based on POSTGRES_DB environment variable

-- Create extensions if needed (e.g., for JSONB operations)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Note: Tables will be created by Flask-Migrate/Alembic migrations
-- This script is mainly for any pre-migration setup or custom extensions

